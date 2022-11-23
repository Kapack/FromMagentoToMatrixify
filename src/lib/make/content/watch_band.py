from db.select import Select
import random
import re

class WatchBand():
    def __init__(self) -> None:
        self.select = Select()

    def name(self, model : str, material : str, product_type : str) -> str:
        addjectives = self.select.addjectives()
        # Addjective
        addjective = random.choice(addjectives)
        # Building productname
        productname = addjective.capitalize() + ' ' +  model +  ' ' + material + ' ' +  product_type
        
        return productname
    
    def description(self, model : str, material : str, original_description : str) -> str:
        description : str = ''
        introTxt : str = ''
        materialTxt : str = ''
        sizeTxt : str = ''
        endingTxt : str = ''

        # Select from database        
        introTexts = self.select.watchband_intro_texts()
        materialTexts = self.select.watchband_material_texts()
        endingTexts = self.select.watchband_ending_texts() 
        sizes = self.select.sizes()
        
        # Append random Intro Text
        introTxt = random.choice(introTexts)
        if '[DEVICE]' in introTxt:                                     
            introTxt = introTxt.replace('[DEVICE]', model)
        
        # Append all material, Material Text
        materialListTexts = []                    
        for i in materialTexts:
            if(material == materialTexts[i]['material_text']):                            
                materialListTexts.append(materialTexts[i]['material_text_dk'])    
        
        # If any texts got append to materialListTexts, pick one random
        if(materialListTexts):
            materialTxt = random.choice(materialListTexts)
            if '[DEVICE]' in materialTxt:
                materialTxt = materialTxt.replace('[DEVICE]', model) 
                              
        # Check if original text contains anything about sizes
        sizesFound = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] in original_description.lower() ) ])
        if (sizesFound):
            # Get sizes
            sizeTxt = self.sizeText(productDescription = original_description)

        # Append Ending Text
        endingTxt = random.choice(endingTexts)                    

        # Building our description
        description = introTxt + ' ' + materialTxt + ('<br/><br/><b>Mål:</b><br/>' + sizeTxt if sizeTxt else '') + '<br/><b><i>' + endingTxt + '</i></b>'        
        
        return description
    
    def sizeText(self, productDescription : str):        
        sizes = self.select.sizes()
        sizeTxt = ''

        # Split description
        orgDescSplit = productDescription.lower().replace('\n', " ").split(' ')
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
        print(next_el)
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