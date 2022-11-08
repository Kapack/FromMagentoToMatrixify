from db.select import Select
import random
import re
from utils.helper import getModelName

class Content:
    def __init__(self) -> None:
        self.select = Select()

    """
    Creates name from attributes and database
    
    [ADDJECTIVE] [MODEL] [MATERIAL] [PRODUCTTYPE]
    
    """
    def createName(self, products:dict) -> dict:
        productname : str = ''
        addjectives = self.select.addjectives()        

        for product in products:
            # Default product name, so name wont be empty
            productname = products[product]['name']                                 
            
            # Choosing on model name
            if (products[product]['model']) and (products[product]['model'].lower() != 'n/a'):                        
                model = products[product]['model']
            else:                                                                                                                    
                model = getModelName(product = products[product])
            # Translated product type
            translate_product_type = products[product]['product_types']['translate']
            # Material
            material = products[product]['materials']['translated']

            if products[product]['parent'] == True:
                if products[product]['product_types']['product_type'] == 'Watch Band':                    
                    # Remove Other material
                    if 'other' in material.lower():
                        material = material.lower().replace('other', '')                        
                    
                    addjective = random.choice(addjectives)
                    productname = addjective.capitalize() + ' ' +  model +  ' ' + material + ' ' +  translate_product_type
                
                if products[product]['product_types']['product_type'] == 'Screen Protecter':
                    # print(material)
                    # print(model + ' ' + translate_product_type)
                    # print(products[product]['product_types']['translate'])
                    #'product_types' : {'product_type' : key['m2_type'], 'translate' : ''},
                    # 'product_types' : {'product_type' : key['m2_type'], 'translate' : ''},
                    pass
                    # productname = 'asdasd'
                
                if products[product]['product_types']['product_type'] == 'Charger':
                    pass
                
                if products[product]['product_types']['product_type'] == 'Cable':
                    pass
                
                if products[product]['product_types']['product_type'] == 'Stand':
                    pass                

                if products[product]['product_types']['product_type'] == 'Stylus Pen':
                    pass
                
                
                products[product]['name'] = productname


        return products

    def createDescription(self, products:dict) -> dict:
        # Select from database        
        introTexts = self.select.watchband_intro_texts()
        materialTexts = self.select.watchband_material_texts()
        endingTexts = self.select.watchband_ending_texts() 
        sizes = self.select.sizes()

        for product in products:                      
            description = []
            introTxt : str = ''
            materialTxt : str = ''
            sizeTxt : str = ''
            endingTxt : str = ''

            if products[product]['parent'] == True:    
                if products[product]['product_types']['product_type'] == 'Watch Band':                    
                    # Append random Intro Text
                    introTxt = random.choice(introTexts)
                    if '[DEVICE]' in introTxt:                         
                        model = getModelName(product = products[product])
                        introTxt = materialTxt.replace('[DEVICE]', introTxt)

                    # Append all material, Material Text
                    materialListTexts = []                    
                    for i in materialTexts:
                        if(products[product]['materials']['material'] == materialTexts[i]['material_text']):                            
                            materialListTexts.append(materialTexts[i]['material_text_dk'])                    
                            
                    # If any texts got append to materialListTexts, pick one random
                    if(materialListTexts):
                        materialTxt = random.choice(materialListTexts)
                        if '[DEVICE]' in materialTxt:
                            model = getModelName(product = products[product])
                            materialTxt = materialTxt.replace('[DEVICE]', model)                            

                    # Check if original text contains anything about sizes
                    sizesFound = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] in products[product]['description'].lower() ) ])
                    if (sizesFound):
                        # Get sizes
                        sizeTxt = self.sizeText(product = products[product])
      
                    # Append Ending Text
                    endingTxt = random.choice(endingTexts)                    

                # Building our description
                description = introTxt + ' ' + materialTxt + ('<br/><br/><b>Mål:</b><br/>' + sizeTxt if sizeTxt else '') + '<br/><b><i>' + endingTxt + '</i></b>'
         
                # insert into products descriptions
                products[product]['description'] = description

        return products
    
    def sizeText(self, product:dict):
        sizes = self.select.sizes()
        sizeTxt = ''

        # Split description
        orgDescSplit = product['description'].lower().replace('\n', " ").split(' ')
        # Removing empty from a list
        orgDescSplit = list(filter(None, orgDescSplit))   
        # Loop trough with index and element, so we can get previous and next
        for index, curr_el in enumerate(orgDescSplit):                            
            # In try so we wont get out of range error
            try:
                curr_el = str(curr_el).lower()
                prev_el = str(orgDescSplit[index - 1]).lower()
                next_el = str(orgDescSplit[index + 1]).lower()
                prevAndCurrent = prev_el + ' ' + curr_el
                                            
                for size in sizes: 
                    # if current element is size                                   
                    if(curr_el == sizes[size]['size'] or prevAndCurrent == sizes[size]['size']):
                        # Get previous and current word                        
                        # Check if prevAndCurrent exists as a value (eg. Strap length:)
                        prevAndCurrentSizeFound = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] == prevAndCurrent ) ])
                        if(prevAndCurrentSizeFound):                            
                            # Get translation
                            word = ([sizes[size]['dk'] for size in sizes if(sizes[size]['size'] == prevAndCurrent)])
                            if('inch' in next_el):
                                next_el = self.convertInchToCm(next_el)
                            # Append to txt
                            sizeTxt += word[0].capitalize() + ' ' + next_el + '<br/>'                                            
                            
                        else:
                            # If Previous and Current word does not exists, it's a single word (Eg. Length:)
                            word = ([sizes[size]['dk'] for size in sizes if(sizes[size]['size'] == curr_el)])                            
                            # Calculate size if next_el has inch
                            if('inch' in next_el):
                                next_el = self.convertInchToCm(next_el)                                                            
                            # Append to txt
                            sizeTxt += word[0].capitalize() + ' ' + next_el + '<br/>'
            except:
                pass 

        return sizeTxt
    
    def convertInchToCm(self, next_el:str) -> str:

        # Remove everything that isn't numbers
        splitNext_el = re.split('[^0-9.,]', next_el)
        # Remove empty
        splitNext_el = list(filter(None, splitNext_el))        
        for i, ele in enumerate(splitNext_el):
            # cast to float
            next_el_float = float(splitNext_el[i])
            # Convert inches to cm and round
            next_el_float = round(next_el_float * 2.54, 2)
            # cast to string and prepend cm
            splitNext_el[i] = str(next_el_float) + ' cm'

        # cast back to string
        next_el = ' - '.join(splitNext_el)

        return next_el
