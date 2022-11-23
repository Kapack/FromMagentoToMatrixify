class ScreenProtector():
    
    def name(self, model : str, material : str, product_type : str) -> str:
        productname = model + ' ' + material + ' ' + product_type
        
        return productname
    
    def description(self, original_description : str) -> str:

        return original_description

