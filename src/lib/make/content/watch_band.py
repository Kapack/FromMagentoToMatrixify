from lib.make.content.parent_content import ParentContent
from db.select import SelectWatchBand
import random
import re

class WatchBand(ParentContent):
    def __init__(self, model : str, language : str, material : str) -> None:
        self.model = model
        self.language = language
        self.material = material
        super().__init__()

    def name(self, translated_material : str, product_type : str, translated_product_type : str) -> str:
        # Adjective according material        
        mat_addjective = self.give_addjective_from_material(material = self.material, product_type = product_type, language = self.language)
        # Building productname
        product_name = mat_addjective.capitalize() + ' ' +  self.model +  ' ' + translated_material + ' ' +  translated_product_type
        return product_name
    
    def description(self, original_description : str) -> str:
        select = SelectWatchBand()
        description : str = ''
        intro_txt : str = ''
        material_txt : str = ''
        size_txt : str = ''
        ending_txt : str = ''

        # Select from database        
        intro_texts = select.watchband_intro_texts()
        material_texts = select.watchband_material_texts()
        ending_texts = select.watchband_ending_texts() 
        sizes = select.sizes(language = self.language)
        
        # Append random Intro Text
        intro_txt = random.choice(intro_texts)
        if '[DEVICE]' in intro_txt:                                     
            intro_txt = intro_txt.replace('[DEVICE]', self.model)
        
        # Append all material, Material Text
        material_list_texts = []                    
        for i in material_texts:
            if(self.material == material_texts[i]['material_text']):                            
                material_list_texts.append(material_texts[i][self.language])
        
        # If any texts got append to material_list_texts, pick one random
        if(material_list_texts):
            material_txt = random.choice(material_list_texts)
            if '[DEVICE]' in material_txt:
                material_txt = material_txt.replace('[DEVICE]', self.model) 
                              
        # Check if original text contains anything about sizes
        sizes_found = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] in original_description.lower() ) ])
        if (sizes_found):
            # Get sizes
            size_txt = self.size_text(productDescription = original_description)

        # Append Ending Text
        ending_txt = random.choice(ending_texts)

        # Building our description
        description = intro_txt + ' ' + material_txt + ('<br/><br/><b>Mål:</b><br/>' + size_txt if size_txt else '') + '<br/><b><i>' + ending_txt + '</i></b>'        
        
        return description
    
    def size_text(self, productDescription : str):        
        sizes = self.select.sizes(language = self.language)
        size_txt = ''

        # Split description
        org_desc_split = productDescription.lower().replace('\n', " ").split(' ')
        # Removing empty from a list
        org_desc_split = list(filter(None, org_desc_split))           
        # Loop trough with index and element, so we can get previous and next
        for index, curr_el in enumerate(org_desc_split):                            
            # In try so we wont get out of range error
            try:
                curr_el = str(curr_el).lower()
                prev_el = str(org_desc_split[index - 1]).lower()
                next_el = str(org_desc_split[index + 1]).lower()
                prev_and_current = prev_el + ' ' + curr_el
                                            
                for size in sizes: 
                    # if current element is size                                   
                    if(curr_el == sizes[size]['size'] or prev_and_current == sizes[size]['size']):
                        # Get previous and current word                        
                        # Check if prev_and_current exists as a value (eg. Strap length:)
                        prev_and_current_size_found = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] == prev_and_current ) ])
                        if(prev_and_current_size_found):                            
                            # Get translation
                            word = ([sizes[size]['dk'] for size in sizes if(sizes[size]['size'] == prev_and_current)])
                            if('inch' in next_el):                                
                                next_el = self.convertInchToCm(next_el)
                            # Append to txt
                            size_txt += word[0].capitalize() + ' ' + next_el + '<br/>'                                            
                            
                        else:
                            # If Previous and Current word does not exists, it's a single word (Eg. Length:)
                            word = ([sizes[size]['dk'] for size in sizes if(sizes[size]['size'] == curr_el)])                            
                            # Calculate size if next_el has inch
                            if('inch' in next_el):
                                next_el = self.convertInchToCm(next_el)                                                            
                            # Append to txt
                            size_txt += word[0].capitalize() + ' ' + next_el + '<br/>'
            except:
                pass 

        return size_txt 

    def convertInchToCm(self, next_el:str) -> str:
        print(next_el)
        # Remove everything that isn't numbers
        split_next_el = re.split('[^0-9.,]', next_el)
        # Remove empty
        split_next_el = list(filter(None, split_next_el))        
        for i, ele in enumerate(split_next_el):
            # cast to float
            next_el_float = float(split_next_el[i])
            # Convert inches to cm and round
            next_el_float = round(next_el_float * 2.54, 2)
            # cast to string and prepend cm
            split_next_el[i] = str(next_el_float) + ' cm'

        # cast back to string
        next_el = ' - '.join(split_next_el)

        return next_el  