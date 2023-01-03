from db.select import SelectCover
from lib.make.content.parent_content import ParentContent
from config.constants import LOCALWORDS

import random

class Cover(ParentContent):
    def __init__(self, language : str, model : str, material : str) -> None:
        self.language = language
        self.model = model
        self.material = material
        super().__init__()

    def name(self, translated_material : str, product_types : list) -> str:       
        translated_product_type = product_types['translate']
        product_types = product_types['product_type']

        # Adjective according material
        mat_addjective = self.give_addjective_from_material(material = self.material, product_type = product_types, language = self.language)
        # If there's multiple materials, replace last , with And (In local language)
        translated_material = self.set_and_in_material_name(translated_material = translated_material, language = self.language)
        # Building product name                
        product_name = mat_addjective.capitalize() + ' ' + self.model +  ' ' + translated_material + ' ' +  translated_product_type
        return product_name
    
    def name_with_screen_protector(self, product_types : list, translated_material : list) -> str:
        translated_product_type = product_types['translate']
        product_types = product_types['product_type']

        mat_addjective = self.give_addjective_from_material(material = self.material, product_type = product_types, language = self.language)
        # Building name
        first_product_type = str(' ' + LOCALWORDS[self.language]['and'] + ' ').join(translated_material) + ' ' + translated_product_type[0]                
        second_product_type = translated_product_type[1]

        # Using in tempered glass, if it's there
        if 'tempered glass' in self.material[-1]:
            first_product_type = str(' ' + LOCALWORDS[self.language]['and'] + ' ').join(translated_material[:-1]) + ' ' + translated_product_type[0]
            second_product_type = translated_product_type[1] + ' ' + LOCALWORDS[self.language]['in'] + ' ' + translated_material[-1]        
                
        product_name = mat_addjective.capitalize() + ' ' + self.model + ' ' + first_product_type + ' ' + LOCALWORDS[self.language]['with'] + ' ' + second_product_type

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