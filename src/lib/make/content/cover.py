from db.select import SelectCover
import random

class Cover:
    def name(self, model : str, translated_material : str, product_type : str) -> str:
        product_name = model +  ' ' + translated_material + ' ' +  product_type        
        return product_name        
        
    def description(self, model : str, material : str, language : str) -> str:
        select = SelectCover()
        description : str = ''
        intro_txt : str = ''
        material_txt : str = ''

        # Select from database        
        intro_texts = select.intro_text(language = language)
        material_texts = select.material_texts(language = language)
                
        # Append random Intro Text
        intro_txt = random.choice(intro_texts)
        if '[DEVICE]' in intro_txt:                                     
            intro_txt = intro_txt.replace('[DEVICE]', model)
                
        # If product has material
        if material:            
            material_list_texts = []                    
            for i in material_texts:                
                if(material == material_texts[i]['material_text']):                            
                    material_list_texts.append(material_texts[i][language])
            # Pick one random text
            if material_list_texts:
                material_txt = random.choice(material_list_texts)

                if '[DEVICE]' in material_txt:
                    material_txt = material_txt.replace('[DEVICE]', model) 


        # Building Description
        description = intro_txt + ' ' + material_txt

        return description