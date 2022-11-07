import csv
from config.constants import CONTENT_FILES_EXPORT_FROM_MAGENTO

class ReadCsv:
	def getProducts(self) -> list[dict]:
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
          			'option1_name' : 'Serie',
					'option1_value' : '',
					'variant_grams' : '100',
					'variant_inventory_tracker' : 'shopify',
					'variant_inventory_qty' : key['qty'],
					'variant_Inventory_policy' : 'deny',
					'variant_fulfillment_service' : 'manual',
					'variant_price' : '',
          			'variant_compare_price' : '',
					'variant_requires_shipping' : 'TRUE',
					'variant_taxable' : 'TRUE',
					'variant_weight_unit' : 'kg',
					'variant_image' : '',
					'image_position' : '1',
					'seo_title' : '',
					'seo_description' : '',
					'status' : 'active',					
					'additional_images' : key['additional_images'],
					'image_alt_text' : '',
					'variant_country_of_origin' : 'SE',
					'custom_product_type' : '',
					'type_standard_id' : '',
					'type_standard_name' : '',
					'type_standard' : '',
					'price' : key['price'],
					'special_price' : key['special_price'],
					'product_type' : key['m2_type'], 					 
					'size' : '',
					'material' : key['material'],
					'translated_material' : '',
					'metafield_material' : '',	
					'g_metafield_material' : '',				
					'translated_product_type' : '',
					'categories' : key['_category'],
					'parent': False,
					'metafield_compatible_with' : '',
					'color' : key['color'],
					'hex_color' : key['color'],
					'string_color' : key['color'],
				}
				i += 1
			return products