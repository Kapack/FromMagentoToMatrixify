from config.constants import MAGENTO_IMG_URL
import re

class Image():

    def create_base_image(self, products:dict) -> dict:
        base_image : str

        for product in products:
            images_split = products[product]['additional_images'].split(',')
            base_image = images_split[0]
            # Append lux-case url
            base_image = MAGENTO_IMG_URL + base_image
            # Assign new value            
            products[product]['variant_image'] = base_image
                         
        return products

    def create_additonal_images(self, products:dict) -> dict:
        add_img : str

        for product in products:            
            # Split add images 
            add_img_split = products[product]['additional_images'].split(',')
            # Append url
            add_img = [MAGENTO_IMG_URL + path for path in add_img_split]            
            # Images Src to string                        
            add_img = '; '.join(str(e) for e in add_img)
            products[product]['additional_images'] = add_img
            
        return products

    def create_image_alt_text(self, products:dict) -> dict:
        image_alt_text : str
        for product in products:            
            # Replace special char with -
            image_alt_text = re.sub("[^A-Za-z0-9]","-", products[product]['options']['option1_value'])
            # Split
            image_alt_text_split = image_alt_text.split('-')
            # Remove empty (Because of duouble dashes)             
            str_list = list(filter(None, image_alt_text_split))
            image_alt_text = '-'.join(str_list)                                    
            # imageAltText = '#color_' + imageAltText.lower()
            image_alt_text = '#serie_' + image_alt_text.lower()            
            products[product]['image_alt_text'] = image_alt_text
        return products