from utils.helper import convertListToString
from config.constants import BGCOLORS
from db.select import Select
from lib.make.collection.collection import CreateCollection

class Make:
    def __init__(self) -> None:
        self.select = Select()
    
    """
    Creates handle 
    So shopify knows parent/child relationshop    
    """
    def handle(self, products:dict) -> dict:
        handle : str
        for i in products:
            # Split sku by -
            skuSplit = products[i]['sku'].split('-')
            # Some skus are missing the last - 1
            if(len(skuSplit) >= 4):
                # remove last element
                skuSplit.pop()
            # create back to a string
            handle = ('-').join(skuSplit)                
            # Insert Handle
            products[i]['handle'] = handle
        
        return products
    
    """
    If the previous item doesn't have the same handle, we assume it's the parent
    """
    def checkIfParent(self, products:dict) -> dict:
        previousHandle: str
        currentHandle: str

        for i, product in enumerate(products):
            # If it's the first product in out list
            if (i == 0):
                products[i]['parent'] = True
            else:
                previousHandle = products[i - 1]['handle']                
                currentHandle = products[i]['handle']
                if previousHandle != currentHandle:
                    products[i]['parent'] = True                    
        
        return products

    def createOptionOne(self, products:dict) -> dict:
        for product in products:
            """
            Series as Option 1
            """
            try:
                splitSku = products[product]['sku'].split('-')                
                serieNumber = splitSku.pop()
                if serieNumber.startswith('00', 0, 2):
                    serieNumber = serieNumber.replace('00', '')                                                    
                products[product]['options']['option1_value'] = serieNumber                
            except:
                print(BGCOLORS['WARNING'] + ' missing - in sku ' + BGCOLORS['ENDC'])
        return products   

    """
        We will creating category names from the magento file
        We return two lists: One for the products and the other for missing collections.
        belongsTo refers to the parent
    """
    def createCategories(self, products:dict) -> list:                
        # Collections in DB
        collections = self.select.collections()  
        # For creating new collections      
        missingCollections : list[str] = []

        for product in products:            
            currentProductCategories : list[str]        
            productCategories : list[str] = []   
            productMetafield : list[str] = []             
            appendDbCollections : list[dict] = []
 
            currentProductCategories = products[product]['categories']['category'].split(',')
            for category in currentProductCategories:                                
                categorySplit = category.split('/')
                # Remove unwanted categories
                unwanted = ['Lux-Case', 'Smartwatch']
                for item in unwanted:
                    if item in categorySplit:                        
                        categorySplit.remove(item)
                    # Removes Lux-case as manufacturer                    
                    if item.lower() == products[product]['manufacturer'].lower():
                        products[product]['manufacturer'] = ''
                    
                for i, category in enumerate(categorySplit):                                                                                 
                    # If there's a / in the category name (Eg. Model 2 / 2s)
                    if('\\' in category):
                        # Combine the two elements
                        category = category + categorySplit[i + 1]
                        # Remove what is after slash so we don't search for 2s
                        categorySplit.remove(categorySplit[i + 1])                                                
                    # Check if category(name) is in DB, get the object. Returns a list with one item
                    dbCollection = [collection for collection in collections if str(collection['name']).lower() == category.lower()]                                                
                    if dbCollection:
                        # Append all categories objects found                      
                        appendDbCollections.append(dbCollection[0])

                    # Append missing categories: If category name is missing in db and not empty           
                    elif (category):
                        missingCollections.append(category)

            # Appending all found collections (To categores and metafiled)
            for collection in appendDbCollections:
                # Append brand and model
                productCategories.append(collection['name'])                
                # Append Series
                if collection['belongs_to']:
                    productCategories.append(collection['belongs_to'])

                # Append to metafield
                if collection['relationship_type'].lower() == 'child':
                    productMetafield.append(collection['name'])
                            
                        
            # Make sure we have manufacturer as first element in categories                        
            if products[product]['manufacturer']:                                  
                productCategories.insert(0, products[product]['manufacturer'])      
            
            # Remove duplicates                        
            productCategories = list(dict.fromkeys(productCategories))               
            missingCollections = list(dict.fromkeys(missingCollections))  
            productMetafield = list(dict.fromkeys(productMetafield))  
            
            # Asigning categories / Tags
            products[product]['categories']['category'] = productCategories
            # Asigning metafield
            products[product]['categories']['metafield_compatible_with'] = ', '.join(productMetafield)

        return [products, missingCollections]
    
    """
    Clean up so it's correct format for import file
    """
    def cleanAndFormat(self, products:dict) -> dict:        
        for product in products:
            # Make sure we don't have double spaces in name
            products[product]['name'] = " ".join(products[product]['name'].split())
             
            # Adding default size
            if (products[product]['product_types']['product_type'] == 'Watch Band' and products[product]['size'] == ''):
                products[product]['size'] = 'One-size'
            
            # Cast categories into string            
            products[product]['categories']['category'] = convertListToString(theList = products[product]['categories']['category'])  

        return products