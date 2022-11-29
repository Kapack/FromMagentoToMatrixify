from db.select import SelectScreenProtector
import random

class ScreenProtector():
    
    def name(self, model : str, material : str, product_type : str) -> str:
        product_name = model + ' ' + material + ' ' + product_type
        
        return product_name
    
    def description(self, model : str) -> str:
        select = SelectScreenProtector()
        description : str = ''
        intro_texts : str = ''
        # Select from database        
        intro_texts = select.intro_text()
        
        # Append random Intro Text
        intro_txt = random.choice(intro_texts)
        if '[DEVICE]' in intro_txt:                                     
            intro_txt = intro_txt.replace('[DEVICE]', model)
        
        # Building Description
        description = intro_txt

        return description