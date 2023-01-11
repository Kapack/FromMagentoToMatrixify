from db.select import SelectCollection

class ProductCategories:
    def __init__(self, language : str) -> None:
        self.language = language

    def create(self, products : dict) -> tuple:
        # For creating new collections      
        missing_collections : list[str] = []

        for product in products:  
            current_product : dict = products[product]          
            current_product_categories : list[str]        
            product_categories : list[str] = []   
            product_metafield : list[str] = []             
            append_db_collections : list[dict] = []
            
            current_product_categories = products[product]['categories']['category'].split(',')
            for category in current_product_categories:                                   
                category_split = category.split('/')
                # Remove unwanted categories
                remove_unwanted = self.remove_unwanted_categores(category_split = category_split, current_product = current_product)
                category_split = remove_unwanted[0]
                current_product = remove_unwanted[1]
                            
                for i, product_category_name in enumerate(category_split):                    
                    # If there's a / in the category name (Eg. Model 2 / 2s)
                    if('\\' in product_category_name):
                        # Combine the two elements
                        product_category_name = product_category_name + category_split[i + 1]
                        # Remove what is after slash so we don't search for 2s
                        category_split.remove(category_split[i + 1])                
                    # If alternative name, give "org." name
                    product_category_name = self.is_alternative_name(product_category_name = product_category_name)                    
                    in_db = self.is_product_category_name_in_database(product_category_name = product_category_name)
                    
                    # If existing:
                    if in_db[0]:
                        append_db_collections.append(in_db[0])
                    
                    # If missing collection
                    if in_db[1]:
                        missing_collections.append(in_db[1])

            # Appending all found collections (To categores and metafield)
            for collection in append_db_collections:
                # Append brand and model
                product_categories.append(collection['name'])                
                # Append Series / Parent
                if collection['belongs_to']:
                    product_categories.append(collection['belongs_to'])                    

                # Append to metafield
                if collection['relationship_type'].lower() == 'child':
                    product_metafield.append(collection['name'])
                                                    
            # Make sure we have manufacturer as first element in categories                        
            if current_product['manufacturer']:                                  
                product_categories.insert(0, current_product['manufacturer'])      
            
            # Remove duplicates                        
            product_categories = list(dict.fromkeys(product_categories))                
            missing_collections = list(dict.fromkeys(missing_collections))  
            product_metafield = list(dict.fromkeys(product_metafield))  
            
            # Asigning categories / Tags            
            current_product['categories']['category'] = product_categories            
            # Asigning metafield
            current_product['categories']['metafield_compatible_with'] = ', '.join(product_metafield)

        return products, missing_collections
    
    def remove_unwanted_categores(self, category_split : list, current_product : dict) -> list:
        unwanted = ['Lux-Case', 'Smartwatch', 'Audio']
        for item in unwanted:
            if item in category_split:                        
                category_split.remove(item)
            # Removes Lux-case as manufacturer                    
            if item.lower() == current_product['manufacturer'].lower():
                current_product['manufacturer'] = ''
        
        return [category_split, current_product]

    def is_alternative_name(self, product_category_name : str) -> str:
        all_alt_names_in_db : list[dict] = []
        collections = SelectCollection().collections(language = self.language)        
        # Getting all alternative names in DB
        for collection in collections:
            # If collection has alternative names 
            if collection['alternative_names']:
                # Only append if it not already exists (Avoid duplicates)
                if collection not in all_alt_names_in_db:
                    all_alt_names_in_db.append(collection)
                
        # Checking if product_category_name is an alternative name. If true, give org. name
        for item in all_alt_names_in_db:            
            for alt_name in item['alternative_names']:
                if product_category_name.lower() == alt_name.lower():
                    product_category_name = item['name']
        
        return product_category_name

    def is_product_category_name_in_database(self, product_category_name : str) -> tuple:
        product_category_name : str = product_category_name
        existing_db_collections : dict = {}
        missing_collection : str = ''

        collections = SelectCollection().collections(language=self.language)
        
        # Check if product_category_name is in DB, get the object. Returns a list with one item
        db_collection = [collection for collection in collections if str(collection['name']).lower() == product_category_name.lower()]

        if db_collection:
            # If parent, check if there is a child with 1
            if db_collection[0]['relationship_type'].lower() == 'parent':
                if_child_category = [collection for collection in collections if str(collection['name']).lower() == product_category_name.lower() + ' 1']
                if if_child_category:
                    product_category_name = product_category_name + ' 1'                                

            # Append all categories objects found
            existing_db_collections = db_collection[0]
        
        # Append missing categories: If category name is missing in db and not empty           
        elif (product_category_name):
            missing_collection = product_category_name

        return existing_db_collections, missing_collection