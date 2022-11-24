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
        product_name : str = ''        
        original_description : str = ''
        product_description : str = ''

        # addjectives = self.select.addjectives()

        for product in products:
            # Default product name, so name wont be empty
            product_name = products[product]['name']
            original_description = products[product]['description']

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
                    product_name = WatchBand().name(model = model, material = translated_material, product_type = translate_product_type)
                    product_description = WatchBand().description(model = model, material = translated_material, original_description = original_description)

                if products[product]['product_types']['product_type'] == 'Screen Protecter':                                                                            
                    product_name = ScreenProtector().name(model = model, material = translated_material, product_type = translate_product_type)
                    product_description = ScreenProtector().description(original_description = original_description)
            
            # Setting attr
            products[product]['name'] = product_name
            products[product]['description'] = product_description

        return products