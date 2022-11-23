from db.select import Select
from utils.helper import getModelName
from lib.make.content.screen_protecter import ScreenProtector
from lib.make.content.watch_band import WatchBand


class Content:
    def __init__(self) -> None:
        self.select = Select()

    """
    Creates name from attributes and database
    
    [ADDJECTIVE] [MODEL] [MATERIAL] [PRODUCTTYPE]
    
    """
    def create(self, products:dict) -> dict:
        productName : str = ''
        productDescription : str = ''
        # addjectives = self.select.addjectives()

        for product in products:
            # Default product name, so name wont be empty
            productName = products[product]['name']
            # Choosing on model name
            if (products[product]['model']) and (products[product]['model'].lower() != 'n/a'):                        
                model = products[product]['model']
            else:                                                                                                                    
                model = getModelName(product = products[product])
            # Translated product type
            translate_product_type = products[product]['product_types']['translate']
            # Material
            translated_material = products[product]['materials']['translated']
            # Remove Other material
            if 'other' in translated_material.lower():
                translated_material = translated_material.lower().replace('other', '') 
            
            # Only make content for parent products 
            if products[product]['parent'] == True:
                # Pick correct content
                if products[product]['product_types']['product_type'] == 'Watch Band':
                    productName = WatchBand().name(model = model, material = translated_material, product_type = translate_product_type)
                    productDescription = WatchBand().description(model = model, material = translated_material, original_description = products[product]['description'])

                if products[product]['product_types']['product_type'] == 'Screen Protecter':                                                                            
                    productName = ScreenProtector().name(model = model, material = translated_material, product_type = translate_product_type)
                    productDescription = ScreenProtector().description(original_description = products[product]['description'])
            
            # Setting attr
            products[product]['name'] = productName
            products[product]['description'] = productDescription

        return products