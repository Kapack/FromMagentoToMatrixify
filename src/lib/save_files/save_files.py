import csv
from config.constants import CONTENT_DIR_IMPORT_TO_MATRIXIFY, BGCOLORS

class SaveFiles:
    def csv(self, products:dict, language:str) -> None:
        with open(CONTENT_DIR_IMPORT_TO_MATRIXIFY + '1-import-'+ language +'-main-products.csv', 'w') as file:            
            fieldnames = [
                'Handle', 
                'Variant SKU', 
                'Variant Barcode', 
                'Title', 
                'Command', 
                'Variant Command', 
                'Tags Command', 
                'Body (HTML)', 
                'Vendor', 
                'Tags', 
                'Option1 Name', 
                'Option1 Value', 
                'Option2 Name', 
                'Option2 Value', 
                'Option3 Name', 
                'Option3 Value', 
                'Variant Grams', 
                'Variant Inventory Tracker', 
                'Variant Inventory Qty', 
                'Variant Inventory Policy',	
                'Variant Fulfillment Service', 
                'Variant Price',
                'Variant Compare At Price',
                'Variant Requires Shipping', 
                'Variant Taxable',
                'Variant Weight Unit', 
                'Variant Image',
                'Image Src', 
                'Image Alt Text', 
                'Image Position',
                'SEO Title', 
                'SEO Description', 
                'Status', 
                'Variant Country of Origin', 
                'Type: Standard ID',
                'Type: Standard Name',
                'Type: Standard',                
                'Metafield: custom.compatible_with [list.single_line_text_field]',
                'Metafield: custom.multiple_material [list.single_line_text_field]',
                'Metafield: custom.storrelse [single_line_text_field]',
                'Variant Metafield: custom.farve [list.color]',
                # 'Variant Metafield: color.string [single_line_text_field]',
                'Metafield: mm-google-shopping.custom_product [string]',           
                ]
                
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()            

            for product in products:                                               
                writer.writerow({
                    'Handle' : products[product]['handle'], 
                    'Variant SKU' : products[product]['sku'], 
                    'Variant Barcode' : products[product]['ean'], 
                    'Title' : products[product]['name'], 
                    'Command' : products[product]['command'], 
                    'Variant Command' : products[product]['variant_command'], 
                    'Tags Command' : 'MERGE', 
                    'Body (HTML)' :  products[product]['description'], 
                    'Vendor' : products[product]['vendor'], 
                    'Tags' :  products[product]['categories']['category'],
                    'Option1 Name' : products[product]['options']['option1_name'], 
                    'Option1 Value' : products[product]['options']['option1_value'],                    
                    'Option2 Name' : products[product]['options']['option2_name'],
                    'Option2 Value' : products[product]['options']['option2_value'],
                    'Option3 Name' : '', 
                    'Option3 Value' : '',
                    'Variant Grams' : products[product]['variant_grams'], 
                    'Variant Inventory Tracker' : products[product]['variant_inventory_tracker'], 
                    'Variant Inventory Qty' : products[product]['variant_inventory_qty'], 
                    'Variant Inventory Policy' : products[product]['variant_Inventory_policy'], 
                    'Variant Fulfillment Service' : products[product]['variant_fulfillment_service'], 
                    'Variant Price' : products[product]['prices']['variant_price'],
                    'Variant Compare At Price' : products[product]['prices']['variant_compare_price'],
                    'Variant Requires Shipping' : products[product]['variant_requires_shipping'], 
                    'Variant Taxable' : products[product]['variant_taxable'], 
                    'Variant Weight Unit' : products[product]['variant_weight_unit'], 
                    'SEO Title' : products[product]['seo_title'], 
                    'SEO Description' : products[product]['seo_description'], 
                    'Status' : products[product]['status'], 
                    # The Main/First/Featured Image
                    'Variant Image' : products[product]['variant_image'],                     
                    # We need Image Src in order for Image Position to work
                    'Image Src' : products[product]['variant_image'], 
                    'Image Alt Text' : products[product]['image_alt_text'], 
                    'Image Position' : products[product]['image_position'],
                    'Variant Country of Origin' : products[product]['variant_country_of_origin'], 
                    'Type: Standard ID' : products[product]['types']['type_standard_id'],
                    'Type: Standard Name' : products[product]['types']['type_standard_name'],
                    'Type: Standard' : products[product]['types']['type_standard'],                    
                    'Metafield: custom.compatible_with [list.single_line_text_field]' : products[product]['categories']['metafield_compatible_with'],                                        
                    'Metafield: custom.multiple_material [list.single_line_text_field]' : products[product]['materials']['metafield'],
                    'Metafield: custom.storrelse [single_line_text_field]' : products[product]['size'],
                    'Variant Metafield: custom.farve [list.color]' : products[product]['colors']['hex'],   
                    # 'Variant Metafield: color.string [single_line_text_field]' : products[product]['colors']['string'],
                    'Metafield: mm-google-shopping.custom_product [string]' : 'false',
                    })
        print(BGCOLORS['SUCCESS'] + 'Import file is saved' + BGCOLORS['ENDC'])
    
    def additional_image_file(self, products:dict, language : str) -> None:
        with open(CONTENT_DIR_IMPORT_TO_MATRIXIFY + '2-import-'+ language +'-product-add-images.csv', 'w') as file:
            fieldnames = ['Variant SKU', 'Image Src', 'Image Alt Text', 'Image Position', 'Image Command']

            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()

            for product in products:
                writer.writerow({
                    'Variant SKU' : products[product]['sku'], 
                    'Image Src' : products[product]['additional_images'], 
                    'Image Alt Text' : products[product]['image_alt_text'],
                    # Start from position 2, so we show images in the right order
                    'Image Position' : '2',
                    'Image Command' : 'MERGE', 
                    # 'Variant Command' : 'MERGE', 
                })
        print(BGCOLORS['SUCCESS'] + 'Additional images is saved' + BGCOLORS['ENDC'])
        