from config.constants import LOCALWORDS
from db.select import Select
import random

class ParentContent:
    def __init__(self) -> None:
        self.select = Select()

    # If there is and And in material name, translate the and to local language
    def set_and_in_material_name(self, translated_material : str, language : str) -> str:
        translated_material : str = translated_material
        
        if ',' in translated_material:
            # Search for the last occurrence of substring in string
            pos = translated_material.rfind(',')
            if pos > -1:
                # Replace last occurrences of substring ',' in string with 'and'                
                translated_material = translated_material[:pos] + ' ' + LOCALWORDS[language]['and'] + ' ' + translated_material[pos + len(','): ]
        
        return translated_material
    
    # Setting an addjective from material (db/csv/attributes/addjective.csv)
    def give_addjective_from_material(self, material : str, product_type : str, language : str) -> str:
        mat_addjective : str = ''
        # Adjective according material
        addjectives = self.select.addjectives(language = language)        

        for type_key in addjectives:            
            if product_type.lower() == type_key:
                # If material has text                
                try:
                    # Picking random addjective from material
                    mat_addjective = random.choice(addjectives[product_type.lower()][material])
                # If there's not material text, use a default
                except (KeyError):
                    mat_addjective = random.choice(addjectives[product_type.lower()]['default'])
                    # print(mat_addjective)        
        return mat_addjective
