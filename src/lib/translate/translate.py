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
            product_material = products[product]['materials']['material'].lower()                        
            translated_materials = []
            # If product has a material
            if(product_material):
                # Splitting with , (Multiple materials)
                product_material_split = product_material.split(',')
                product_material_split = [mat.strip() for mat in product_material_split]                
                # Loop through database
                for i in materials:                                
                    # If DB material exists in product_material_split list
                    if materials[i]['material'].lower() in product_material_split:                        
                        # If there is a translated version
                        if(materials[i][language]):                            
                            translated_materials.append(materials[i][language])
                        # Give user message if translated verison is missing
                        else:
                            print(materials[i]['material'] + ' needs translation')
                                                
                # Give products string value                
                products[product]['materials']['translated'] =  str(' ' + LOCALWORDS[language]['and'] + ' ').join(translated_materials)

        return products
    

    def product_types(self, products:dict, language:str) -> dict:
        product_types = self.select.product_types(language = language)
        for product in products:            
            for i in product_types:                                                                        
                # If what is in select 
                if(product_types[i]['product_type'].lower() == products[product]['product_types']['product_type']):
                    if(product_types[i][language]):
                        products[product]['product_types']['translate'] = product_types[i][language]                    
                    else:
                        raise ValueError(product_types[i]['product_types']['product_type'] + ' needs translation')            
        return products    