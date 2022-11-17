from config.constants import MAGENTO_IMG_URL
import re

class Image():

    def createBaseImage(self, products:dict) -> dict:
        baseImage : str

        for product in products:
            imagesSplit = products[product]['additional_images'].split(',')
            baseImage = imagesSplit[0]
            # Append lux-case url
            baseImage = MAGENTO_IMG_URL + baseImage
            # Assign new value            
            products[product]['variant_image'] = baseImage
                         
        return products

    def createAdditonalImages(self, products:dict) -> dict:
        addImg : str

        for product in products:            
            # Split add images 
            addImgSplit = products[product]['additional_images'].split(',')
            # Append url
            addImg = [MAGENTO_IMG_URL + path for path in addImgSplit]            
            # Images Src to string                        
            addImg = '; '.join(str(e) for e in addImg)
            products[product]['additional_images'] = addImg
            
        return products

    def createImageAltText(self, products:dict) -> dict:
        imageAltText : str
        for product in products:            
            # Replace special char with -
            imageAltText = re.sub("[^A-Za-z0-9]","-", products[product]['options']['option1_value'])
            # Split
            imageAltTextSplit = imageAltText.split('-')
            # Remove empty (Because of duouble dashes)             
            str_list = list(filter(None, imageAltTextSplit))
            imageAltText = '-'.join(str_list)                                    
            # imageAltText = '#color_' + imageAltText.lower()
            imageAltText = '#serie_' + imageAltText.lower()            
            products[product]['image_alt_text'] = imageAltText                     
        return products