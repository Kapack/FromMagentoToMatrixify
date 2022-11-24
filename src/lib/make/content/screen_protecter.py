from db.select import SelectScreenProtector

class ScreenProtector():
    
    def name(self, model : str, material : str, product_type : str) -> str:
        product_name = model + ' ' + material + ' ' + product_type
        
        return product_name
    
    def description(self, original_description : str) -> str:
        select = SelectScreenProtector()
        description : str = ''
        intro_texts : str = ''
        
        # intro_texts = select.intro_text()
        # print(intro_texts)







        return original_description

