from config.constants import LOCALWORDS
from utils.helper import replace_last, split_measurements_from_string
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

    def name(self, translated_material : str, product_types : list) -> str:
        translated_product_type = product_types['translate']
        product_types = product_types['product_type']

        # Adjective according material        
        mat_addjective = self.give_addjective_from_material(material = self.material, product_type = product_types, language = self.language)
        
        # Replacing comma
        if ',' in translated_material:
            # Replace last occurence of , with and
            translated_material = replace_last(translated_material, ',', ' ' + LOCALWORDS[self.language]['and'] + ' ')
            # Remove double spaces
            translated_material = " ".join(translated_material.split())
            
        # Building productname
        product_name = mat_addjective.capitalize() + ' ' +  self.model +  ' ' + ''.join(translated_material) + ' ' +  ''.join(translated_product_type)
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
            if(self.material == material_texts[i]['material']):                            
                material_list_texts.append(material_texts[i][self.language])
        
        # If any texts got append to material_list_texts, pick one random
        if(material_list_texts):
            material_txt = random.choice(material_list_texts)
            if '[DEVICE]' in material_txt:
                material_txt = material_txt.replace('[DEVICE]', self.model) 
                              
        # Check if original text contains anything about sizes
        # sizes_found = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] in original_description.lower() ) ])        
        # sizes_found = ([ sizes[size]['size'] for size in sizes if(sizes[size]['size'] in original_description.lower() ) ])
        sizes_found = [size['size'] for size in sizes if size['size'] in original_description.lower()]        
        if (sizes_found):
            # Get sizes
            size_txt = self.size_text(productDescription = original_description)

        # Append Ending Text
        ending_txt = random.choice(ending_texts)

        # Building our description
        description = intro_txt + ' ' + material_txt + ('<br/><br/><b>M??l:</b><br/>' + size_txt if size_txt else '') + '<br/><b><i>' + ending_txt + '</i></b>'        
        
        return description
    
    def size_text(self, productDescription : str) -> str:        
        sizes = self.select.sizes(language = self.language)
        size_txt = ''

        # All keys in db sizes, so we wont risk to get double texts
        all_size_keys = []
        for size in sizes:
            all_size_keys.append(size['size'])    

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
                next_next_el = str(org_desc_split[index + 2]).lower()
                prev_and_current = prev_el + ' ' + curr_el
                size_number = ''

                for size in sizes:
                    # If current element is a size, and prev_and_current does not exits in db
                    if(curr_el == size['size']) and (prev_and_current not in all_size_keys):
                        translated_size_key = ([size[self.language] for size in sizes if(size['size'] == curr_el)])
                        # Calculate size if next_el has inch
                        if 'inch' in next_el:  
                            # Check if we need convert measurement
                            size_number = self.convertInchToCm(next_el)
                            # Append to txt
                            size_txt += translated_size_key[0].capitalize() + ' ' + size_number + '<br/>'

                    # If only prev_and_current exists in db (Double sizez)
                    if(prev_and_current == size['size']):                        
                        # Get translation
                        translated_size_key = ([size[self.language] for size in sizes if(size['size'] == prev_and_current)])
                        
                        # For sizes like: Strap width: 20 inches
                        if next_el.isnumeric() and 'inch' in next_next_el:                            
                            size_number = self.convertInchToCm(next_el)                            
                        
                        # For sizes like: Wrist circumference: 5.5-8.7 inches                        
                        if '-' in next_el and 'inch' in next_next_el:                            
                            next_el_split = next_el.split('-')
                            sizes_in_cm = []
                            for el in next_el_split:
                                # If element is a digigt 
                                if el.replace('.','',1).isdigit():
                                    # Convert element to float
                                    el_as_float = float(el)
                                    # Calculate in cm Insert into sizes and convert to str
                                    sizes_in_cm.append(str(round(el_as_float * 2.54, 2)))                            
                            
                            # For our text:                            
                            size_number = '-'.join(sizes_in_cm) + 'cm'
                        
                        # For sizes like: Strap length: 89 + 117mm
                        if '+' in next_next_el :
                            from_size = next_el
                            to_size = str(org_desc_split[index + 3]).lower()
                            to_size_split = split_measurements_from_string(to_size)

                            # Validatiing
                            if from_size.isdigit() and to_size_split[0].isdigit():
                                to_size = to_size_split[0]                                
                                measurement = to_size_split[1]
                                size_number = from_size + ' + ' + to_size + measurement
                                                                                                                        
                        # Building final size_txt
                        size_txt += translated_size_key[0].capitalize() + ' ' + size_number + '<br/>'
     
            except:
                pass 

        return size_txt 

    def convertInchToCm(self, next_el:str) -> str:
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
            split_next_el[i] = str(next_el_float) + 'cm'

        # cast back to string
        next_el = ' - '.join(split_next_el)

        return next_el  