from utils.helper import convert_list_to_string
from config.constants import BGCOLORS
from db.select import SelectCollection

class Make:
    """
    Creates handle 
    So shopify knows parent/child relationshop    
    """
    def handle(self, products:dict) -> dict:
        handle : str
        for i in products:
            # Split sku by -
            sku_split = products[i]['sku'].split('-')
            # Some skus are missing the last - 1
            if(len(sku_split) >= 4):
                # remove last element
                sku_split.pop()
            # create back to a string
            handle = ('-').join(sku_split)                
            # Insert Handle
            products[i]['handle'] = handle
        
        return products
    
    """
    If the previous item doesn't have the same handle, we assume it's the parent
    """
    def check_if_parent(self, products:dict) -> dict:
        previous_handle: str
        current_handle: str

        for i, product in enumerate(products):
            # If it's the first product in out list
            if (i == 0):
                products[i]['parent'] = True
            else:
                previous_handle = products[i - 1]['handle']                
                current_handle = products[i]['handle']
                if previous_handle != current_handle:
                    products[i]['parent'] = True                    
        
        return products

    def create_option_one(self, products:dict) -> dict:
        for product in products:
            """
            Series as Option 1
            """
            try:
                split_sku = products[product]['sku'].split('-')                
                serie_number = split_sku.pop()
                if serie_number.startswith('00', 0, 2):
                    serie_number = serie_number.replace('00', '')                                                    
                products[product]['options']['option1_value'] = serie_number                
            except:
                print(BGCOLORS['WARNING'] + ' missing - in sku ' + BGCOLORS['ENDC'])
        return products   

    """
        We will creating category names from the magento file
        We return two lists: One for the products and the other for missing collections.
        belongsTo refers to the parent
    """
    def create_categories(self, products:dict) -> list:                
        # Collections in DB        
        collections = SelectCollection().collections()
        # For creating new collections      
        missing_collections : list[str] = []

        for product in products:            
            current_product_categories : list[str]        
            product_categories : list[str] = []   
            product_metafield : list[str] = []             
            append_db_collections : list[dict] = []
 
            current_product_categories = products[product]['categories']['category'].split(',')
            for category in current_product_categories:                                
                category_split = category.split('/')
                # Remove unwanted categories
                unwanted = ['Lux-Case', 'Smartwatch']
                for item in unwanted:
                    if item in category_split:                        
                        category_split.remove(item)
                    # Removes Lux-case as manufacturer                    
                    if item.lower() == products[product]['manufacturer'].lower():
                        products[product]['manufacturer'] = ''
                    
                for i, category in enumerate(category_split):                                                                                 
                    # If there's a / in the category name (Eg. Model 2 / 2s)
                    if('\\' in category):
                        # Combine the two elements
                        category = category + category_split[i + 1]
                        # Remove what is after slash so we don't search for 2s
                        category_split.remove(category_split[i + 1])                                                
                    # Check if category(name) is in DB, get the object. Returns a list with one item
                    db_collection = [collection for collection in collections if str(collection['name']).lower() == category.lower()]                                                
                    if db_collection:
                        # Append all categories objects found                      
                        append_db_collections.append(db_collection[0])

                    # Append missing categories: If category name is missing in db and not empty           
                    elif (category):
                        missing_collections.append(category)

            # Appending all found collections (To categores and metafiled)
            for collection in append_db_collections:
                # Append brand and model
                product_categories.append(collection['name'])                
                # Append Series
                if collection['belongs_to']:
                    product_categories.append(collection['belongs_to'])

                # Append to metafield
                if collection['relationship_type'].lower() == 'child':
                    product_metafield.append(collection['name'])
                                                    
            # Make sure we have manufacturer as first element in categories                        
            if products[product]['manufacturer']:                                  
                product_categories.insert(0, products[product]['manufacturer'])      
            
            # Remove duplicates                        
            product_categories = list(dict.fromkeys(product_categories))               
            missing_collections = list(dict.fromkeys(missing_collections))  
            product_metafield = list(dict.fromkeys(product_metafield))  
            
            # Asigning categories / Tags
            products[product]['categories']['category'] = product_categories
            # Asigning metafield
            products[product]['categories']['metafield_compatible_with'] = ', '.join(product_metafield)

        return [products, missing_collections]
    
    """
    Clean up so it's correct format for import file
    """
    def clean_and_format(self, products:dict) -> dict:        
        for product in products:
            # Make sure we don't have double spaces in name
            products[product]['name'] = " ".join(products[product]['name'].split())
             
            # Adding default size
            if (products[product]['product_types']['product_type'] == 'watch band' and products[product]['size'] == ''):
                products[product]['size'] = 'One-size'
            
            # Cast categories into string            
            products[product]['categories']['category'] = convert_list_to_string(the_list = products[product]['categories']['category'])  

        return products