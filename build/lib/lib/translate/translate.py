from db.select import Select
from config.constants import LOCALWORDS

"""
We translate into key translated_
"""
class Translate:
    def __init__(self) -> None:
        self.select = Select()
        
    def translate_attributes(self, products:dict, language:str) -> dict:
        products : dict

        products = self.material(products, language)
        products = self.product_types(products, language)            
        return products
    
    def material(self, products:dict, language:str) -> dict:      
        materials = self.select.materials(language = language)

        for product in products:
            product_materials = products[product]['materials']['material']
            translated_materials = []
                        
            # If product has a material
            if(product_materials):

                # Loop through database
                for i in materials:                                
                    # If DB material exists in product_material_list
                    db_material = materials[i]['material'].lower()
                    if db_material in product_materials:
                        # Getting index in the last, so we preserve same order
                        product_materials_index = product_materials.index(db_material)                       
                        # If there is a translated version
                        if(materials[i][language]):
                            translated_mat = materials[i][language]         
                            translated_materials.insert(product_materials_index, translated_mat)
                        # Give user message if translated verison is missing
                        else:
                            print(materials[i]['material'] + ' needs translation')
                                                
                # Give products string value                                )
                products[product]['materials']['translated'] =  translated_materials
        
        return products
    
    def product_types(self, products:dict, language:str) -> dict:
        product_types = self.select.product_types(language = language)
        for product in products:   
            translate_product_types = []         
            
            for i in product_types:                
                for product_type in products[product]['product_types']['product_type']:                                        
                    # If product_type from db is in product product_type
                    if(product_types[i]['product_type'].lower() == product_type.lower()):                        
                        # If translated
                        if(product_types[i][language]):                             
                            translate_product_types.append(product_types[i][language])                            
                            products[product]['product_types']['translate'] = translate_product_types

                        else:
                            raise ValueError(product_types[i]['product_types']['product_type'] + ' needs translation')                    
                        
        return products    