import csv
from config.constants import CONTENT_FILES_EXPORT_FROM_MAGENTO, LOCAL_DICT

class ReadCsv:
	def get_products(self, language:str) -> list[dict]:
		# We will append and return to this dict
		products : list[dict] = {}
		# Open csv file
		with open(CONTENT_FILES_EXPORT_FROM_MAGENTO, 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			# Iterate through
			i = 0
			for key in reader:		
				products[i] = { 
					'handle' : '',
					'sku' : key['sku'],
					'ean': key['ean'],
					'name' : key['name'],
          			'manufacturer' : key['manufacturer'],
          			'model' : key['model'],					
					'command' : 'MERGE',
					'variant_command' : 'MERGE',
					'tags_command' : 'MERGE',
					'description' : key['description'],
					'vendor' : 'urrem.dk',
					'tags' : '', 
					'options' : {'option1_name' : 'Serie', 'option1_value' : '', 'option2_name' : LOCAL_DICT['color'][language].capitalize(), 'option2_value' : ''},					
					'variant_grams' : '100',
					'variant_inventory_tracker' : 'shopify',
					'variant_inventory_qty' : key['qty'],
					'variant_Inventory_policy' : 'deny',
					'variant_fulfillment_service' : 'manual',
					'variant_requires_shipping' : 'TRUE',
					'variant_taxable' : 'TRUE',
					'variant_weight_unit' : 'kg',
					'variant_image' : '',
					'variant_country_of_origin' : 'SE',
					'image_position' : '1',
					'seo_title' : '',
					'seo_description' : '',
					'status' : 'active',					
					'additional_images' : key['additional_images'],
					'image_alt_text' : '',
					'custom_product_type' : '',
					'types' : {'type_standard_id' : '', 'type_standard_name' : '', 'type_standard' : ''},
					'prices' : {'price' : key['price'], 'special_price' : key['special_price'], 'variant_price' : '', 'variant_compare_price' : ''},
					'product_types' : {'product_type' : key['m2_type'].lower(), 'translate' : ''},
					'size' : '',
					'materials' : {'material' : key['material'], 'translated' : '', 'metafield' : ''},
					# 'colors' : {'color' : key['color'], 'hex' : key['color'], 'string' : key['color']},			
					'colors' : {'color' : key['color'], 'hex' : key['color']},			
					'categories' : {'category' : key['_category'], 'metafield_compatible_with' : '' },	
					'parent': False,
				}
				i += 1
			return products