from db.select import Select
from utils.helper import get_model_name
# from lib.make.content.screen_protecter import ScreenProtector
from lib.make.content.watch_band import WatchBand
from lib.make.content.cover import Cover


class Content:
    def __init__(self) -> None:
        self.select = Select()        

    """
    Creates name from attributes and database
    
    [ADDJECTIVE] [MODEL] [MATERIAL] [PRODUCTTYPE]
    
    """
    def create(self, products:dict, language : str) -> dict:        
        product_name : str = ''        
        original_description : str = ''
        product_description : str = ''
        product_type : str = ''
        translated_product_type : str = ''
        material : str = ''
        translated_material : str = ''

        for product in products:
            # Default product name, so name wont be empty
            product_name = products[product]['name']
            original_description = products[product]['description']

            # # Choosing on model name
            # if (products[product]['model']) and (products[product]['model'].lower() != 'n/a'):                        
            #     model = products[product]['model']
            # else:                                                                                                                    
            model = get_model_name(product = products[product])

            # Product type
            product_type = products[product]['product_types']['product_type']
            translated_product_type = products[product]['product_types']['translate']            
            # Material
            material = products[product]['materials']['material']
            translated_material = products[product]['materials']['translated']
            # Remove Other material
            if 'other' in translated_material.lower():
                translated_material = translated_material.lower().replace('other', '')                
            
            # Only make content for parent products 
            if products[product]['parent'] == True:
                # Pick correct content
                product_description = ''
                if product_type == 'watch band':
                    product_name = WatchBand(model = model, language = language, material = material).name(translated_material = translated_material, product_type = product_type, translated_product_type = translated_product_type)
                    product_description = WatchBand(model = model, language = language, material = material).description(original_description = original_description)

                if product_type == 'cover':                                      
                    product_name = Cover(model = model, language = language, material = material).name(translated_material = translated_material, product_type = product_type, translated_product_type = translated_product_type)
                    product_description = Cover(model = model, language = language, material = material).description()

                # if products[product]['product_types']['product_type'] == 'screen protecter':                                                                            
                #     product_name = ScreenProtector().name(model = model, material = translated_material, product_type = translate_product_type)
                #     product_description = ScreenProtector().description(model = model)    
            
                # Setting attr.
                products[product]['name'] = product_name
                products[product]['description'] = product_description

        return products