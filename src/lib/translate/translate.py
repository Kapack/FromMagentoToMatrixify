from db.select import Select
import re

"""
We translate into key translated_
"""
class Translate:
    def __init__(self) -> None:
        self.select = Select()
        
    def translateAttributes(self, products:dict) -> dict:
        products : dict

        products = self.material(products)
        products = self.productTypes(products)            
        return products
    
    def material(self, products:dict) -> dict:
        regex = re.compile('[@_!#$%^&*()<>?/\|,}{~: ]')        
        materials = self.select.materials()
        
        for product in products:            
            # If there is material
            if(products[product]['material']):
                # Split with words ( Remember that words like "Genuine Leather" is splitted into twp)
                materialSplit = re.split(r'(\W+)', products[product]['material'])                
                
                for i in range(len(materialSplit)):
                    # If "word" is not a special char
                    if(regex.search(materialSplit[i]) == None):
                        # Find translated version in db
                        # print(materialSplit[i])
                        for material in materials:
                            if(materialSplit[i].lower() == materials[material]['material'].lower()):
                                # If there is a translated version
                                if(materials[material]['dk']):
                                    # Replace in the index from the splitted string
                                    materialSplit[i] = materials[material]['dk']
                                # Give user message if translated verison is missing
                                else:
                                   print(materials[material]['material'] + ' needs translation')

                # Make list a string again
                translated_materials =  ''.join(materialSplit)
                products[product]['translated_material'] = translated_materials    

        return products
    

    def productTypes(self, products:dict) -> dict:
        product_types = self.select.product_types()
        for product in products:            
            for i in product_types:                                
                if(product_types[i]['product_type'] == products[product]['product_type']):
                    if(product_types[i]['dk']):
                        products[product]['translated_product_type'] = product_types[i]['dk']                    
                    else:
                        raise ValueError(product_types[i]['product_type'] + ' needs translation')            
        return products    