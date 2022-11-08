import re
from config.colors import HEXCOLORS

class Metafield:
    
    """
        We use string colors for Google Shopping
        Hex is for shopify metafield
    """
    # Converts colors into Hexcode
    def colors(self, products:dict) -> dict:        
        for product in products:            
            color : str
            hexColors : list
            hexcode : str = ''           
            strColor : str = ''           
            # color = products[product]['color']            
            color = products[product]['colors']['color']            

            # If color is not empty
            if color:
                if '/' in color:
                    splitColor = color.split('/')
                    hexColors = []

                    for col in splitColor:
                        hexColors.append(HEXCOLORS[col.upper()]['hex'])                                         
                    
                    # convert to string
                    hexcode = ', '.join(hexColors)           
                    # Set string color to multicolor
                    strColor = HEXCOLORS['MULTICOLOR']['dk']      
                    
                else:
                    hexcode = HEXCOLORS[color.upper()]['hex']
                    strColor = HEXCOLORS[color.upper()]['dk'].capitalize()
            
                # Assign hexcode to metafield
                products[product]['colors']['hex'] = hexcode
                products[product]['colors']['string'] = strColor
                
        return products    
    
    def compatibleWith(self, products:dict) -> dict:
        for product in products:            
            if products[product]['parent'] == True:                                                                  
                products[product]['metafield_compatible_with'] = ', '.join(products[product]['categories'])
        return products
    
    def material(self, products:dict) -> dict:
        for product in products:
            if products[product]['parent'] == True:
                # Split material
                materialSplit = products[product]['materials']['translated'].split(',')
                products[product]['materials']['metafield'] = ', '.join(materialSplit)                              
        return products
    
    def size(self, products:dict) -> dict:        
        size : str
        nameSplit : list
        lastElement : str

        for product in products:
            if '- ' in products[product]['name']:
                # Get everything from last dash
                nameSplit = products[product]['name'].split('- ')
                # The last element in splitted string
                lastElement = nameSplit[-1].lower()                

                """
                Getting sizes
                If size is in the name
                """                                
                if ' size' in lastElement:
                    # Get everythin after size
                    afterSize = lastElement.lower().split(' size', 1)[1]
                    # Remove special chars
                    size = re.sub("[^A-Za-z0-9]","", afterSize).upper()
                    # Assign Size
                    products[product]['size'] = size

                    # Remove size + afterSize from last element
                    lastElement = lastElement.replace(' size' + afterSize, '')
        
        return products