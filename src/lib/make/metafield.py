import re
from config.colors import HEXCOLORS

class Metafield:
    
    """
        We use string colors for Google Shopping
        Hex is for shopify metafield
    """
    # Converts colors into Hexcode
    def colors(self, products:dict, language:str) -> dict:        
        for product in products:            
            color : str
            hex_colors : list
            hex_code : str = ''           
            str_color : str = ''           
            color = products[product]['colors']['color']

            # If color is not empty
            if color:
                if color.lower() == 'silver/grey':
                    color = 'grey'                                                   

                # Split multiple colors
                if '/' in color and color.lower() != 'silver/grey':
                    split_color = color.split('/')
                    hex_colors = []

                    for col in split_color:
                        hex_colors.append(HEXCOLORS[col.upper()]['hex'])                                         
                    
                    # convert to string
                    hex_code = ', '.join(hex_colors)           
                    # Set string color to multicolor
                    str_color = HEXCOLORS['MULTICOLOR'][language]      
                    
                else:
                    hex_code = HEXCOLORS[color.upper()]['hex']
                    str_color = HEXCOLORS[color.upper()][language]
            
                # Assign hex_code to metafield
                products[product]['colors']['hex'] = hex_code
                # products[product]['colors']['string'] = strColor.capitalize()
                products[product]['options']['option2_value'] = str_color.capitalize()
                
        return products    
    
    def compatibleWith(self, products:dict) -> dict:
        pass
        """
        look in make.createCategories
        """

        # for product in products:            
        #     if products[product]['parent'] == True:                       
        #         products[product]['categories']['metafield_compatible_with'] = ', '.join(products[product]['categories']['metafield_compatible_with'])
        return products
    
    def material(self, products:dict) -> dict:
        for product in products:
            if products[product]['parent'] == True:
                # Split material
                material_split = products[product]['materials']['translated'].split(',')
                products[product]['materials']['metafield'] = ', '.join(material_split)                              
        return products
    
    def size(self, products:dict) -> dict:        
        size : str
        name_split : list
        last_element : str

        for product in products:
            if '- ' in products[product]['name']:
                # Get everything from last dash
                name_split = products[product]['name'].split('- ')
                # The last element in splitted string
                last_element = name_split[-1].lower()                

                """
                Getting sizes
                If size is in the name
                """                                
                if ' size' in last_element:
                    # Get everythin after size
                    after_size = last_element.lower().split(' size', 1)[1]
                    # Remove special chars
                    size = re.sub("[^A-Za-z0-9]","", after_size).upper()
                    # Assign Size
                    products[product]['size'] = size

                    # Remove size + after_size from last element
                    last_element = last_element.replace(' size' + after_size, '')
        
        return products