from utils.helper import convert_list_to_string
from config.constants import BGCOLORS
from lib.make.product_categories import ProductCategories
class Make:
    def __init__(self, language : str) -> None:
        self.language = language
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
        products = ProductCategories(language = self.language).create(products = products)                                
        return products
    
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