class Parent:
    """
    If product is a child, we don't need name and description
    """
    def remove_content_from_child(self, products:dict) -> dict:
        for product in products:            
            if products[product]['parent'] == False:
                # Remove name
                products[product]['name'] = ''
                # Remove description                
                products[product]['description'] = ''
                # Remove Vendor
                products[product]['vendor'] = ''
                # Remove manufacturer
                products[product]['manufacturer'] = ''
                # Remove categories
                products[product]['categories']['category'] = ''
                products[product]['product_types']['product_type'] = ''
        return products     

    """
    WIP
    """
    def correcting_product_types(self, products:dict) -> dict:
        for product in products:
            if products[product]['parent'] == True:
                # Correction 2-in-1 products (Cover + Screen protectors)
                if products[product]['product_types']['product_type'] == 'cover':
                    if any(x in products[product]['name'] for x in ['screen film', 'tempered glass', 'screen protector']):
                        products[product]['product_types']['product_type'] = 'cover, screen protecter'                   

                if products[product]['product_types']['product_type'] == 'screen protecter':
                    if any(x in products[product]['name'] for x in ['cover', 'frame']):
                        products[product]['product_types']['product_type'] = 'cover, screen protecter'
        return products
                
    def set_shopify_product_types(self, products:dict) -> dict:
        for product in products:
            if products[product]['parent'] == True:                
                if products[product]['product_types']['product_type'] == 'watch band':
                    products[product]['types']['type_standard_id'] = '5123'
                    products[product]['types']['type_standard_name'] = 'Watch Bands'
                    products[product]['types']['type_standard'] = 'Apparel & Accessories > Jewelry > Watch Accessories > Watch Bands'
                                        
                elif products[product]['product_types']['product_type'] == 'screen protecter':
                    products[product]['types']['type_standard_id'] = '5468'
                    products[product]['types']['type_standard_name'] = 'Screen Protectors'
                    products[product]['types']['type_standard'] = 'Electronics > Electronics Accessories > Electronics Films & Shields > Screen Protectors'
                                    
                elif products[product]['product_types']['product_type'] == 'charger':
                    products[product]['types']['type_standard_id'] = '505295'
                    products[product]['types']['type_standard_name'] = 'Power Adapters & Chargers'
                    products[product]['types']['type_standard'] = 'Electronics > Electronics Accessories > Power > Power Adapters & Chargers'                    
                
                elif products[product]['product_types']['product_type'] == 'cable':
                    products[product]['types']['type_standard_id'] = '1763'
                    products[product]['types']['type_standard_name'] = 'System & Power Cables'
                    products[product]['types']['type_standard'] = 'Electronics > Electronics Accessories > Cables > System & Power Cables'
                
                elif products[product]['product_types']['product_type'] == 'stand':
                    products[product]['types']['type_standard_id'] = '5974'
                    products[product]['types']['type_standard_name'] = 'Jewelry Holders'
                    products[product]['types']['type_standard'] = 'Health & Beauty > Jewelry Cleaning & Care > Jewelry Holders'

                elif products[product]['product_types']['product_type'] == 'stylus pen':
                    products[product]['types']['type_standard_id'] = '5308'
                    products[product]['types']['type_standard_name'] = 'Stylus Pens'
                    products[product]['types']['type_standard'] = 'Electronics > Electronics Accessories > Computer Accessories > Stylus Pens'

                else:
                    products[product]['types']['type_standard_id'] = '5122'
                    products[product]['types']['type_standard_name'] = 'Watch Accessories'
                    products[product]['types']['type_standard'] = 'Apparel & Accessories > Jewelry > Watch Accessories'
                    
        return products
    
    def set_vendor(self, products) -> dict:
        for product in products:            
            if products[product]['parent'] == True:                
                vendor = products[product]['manufacturer']                
                if not vendor:                    
                    vendor = 'urrem.dk'
                products[product]['vendor'] = vendor
                                        
        return products
    
    def set_material(self, products : dict) -> dict:
        for product in products:
            if products[product]['parent'] == True:
                ## Setting Tempered glass to Screen protectors
                if products[product]['product_types']['product_type'].lower() == 'screen protecter' and 'tempered glass' in products[product]['name']:
                    products[product]['materials']['material'] = products[product]['materials']['material'].lower().replace('glass', 'tempered glass')

        return products