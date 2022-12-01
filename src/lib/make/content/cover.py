from db.select import SelectCover
from lib.make.content.parent_content import ParentContent
import random

class Cover(ParentContent):
    def __init__(self, language : str, model : str, material : str) -> None:
        self.language = language
        self.model = model
        self.material = material
        super().__init__()

    def name(self, translated_material : str, product_type : str, translated_product_type : str) -> str:        
        # Adjective according material
        mat_addjective = self.give_addjective_from_material(material = self.material, product_type = product_type, language = self.language)
        # If there's multiple materials, replace last , with And (In local language)
        translated_material = self.set_and_in_material_name(translated_material = translated_material, language = self.language)
        # Building product name                
        product_name = mat_addjective.capitalize() + ' ' + self.model +  ' ' + translated_material + ' ' +  translated_product_type
        return product_name
        
    def description(self) -> str:
        select = SelectCover()
        description : str = ''
        intro_txt : str = ''
        material_txt : str = ''
        ending_txt : str = ''

        # Select from database        
        intro_texts = select.intro_text(language = self.language)
        material_texts = select.material_texts(language = self.language)
        ending_texts = select.ending_texts(language = self.language)
                
        # Append random Intro Text
        intro_txt = random.choice(intro_texts)
        if '[DEVICE]' in intro_txt:                                     
            intro_txt = intro_txt.replace('[DEVICE]', self.model)
                
        # If product has material
        if self.material:            
            material_list_texts = []                    
            for i in material_texts:                
                if(self.material == material_texts[i]['material_text']):                            
                    material_list_texts.append(material_texts[i][self.language])
            # Pick one random text
            if material_list_texts:
                material_txt = random.choice(material_list_texts)

                if '[DEVICE]' in material_txt:
                    material_txt = material_txt.replace('[DEVICE]', self.model) 
        
        # Pick random ending text
        ending_txt = random.choice(ending_texts)

        # Building Description
        description = intro_txt + ' ' + material_txt + ' ' + ending_txt

        return description