class Parent:
    """
    If product is a child, we don't need name and description
    """
    def removeContentFromChild(self, products:dict) -> dict:
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
                products[product]['categories'] = ''                       
        return products     

    def addProductTypes(self, products:dict) -> dict:
        for product in products:
            if products[product]['parent'] == True:                
                if products[product]['product_type'] == 'Watch Band':
                    products[product]['type_standard_id'] = '342'
                    products[product]['type_standard_name'] = 'Watch Bands'
                    products[product]['type_standard'] = 'Apparel & Accessories > Jewelry > Watch Accessories > Watch Bands'
                                        
                elif products[product]['product_type'] == 'Screen Protecter':
                    products[product]['type_standard_id'] = '1549'
                    products[product]['type_standard_name'] = 'Screen Protectors'
                    products[product]['type_standard'] = 'Electronics > Electronics Accessories > Electronics Films & Shields >Screen Protectors'
                                    
                elif products[product]['product_type'] == 'Charger':
                    products[product]['type_standard_id'] = '1582'
                    products[product]['type_standard_name'] = 'Power Adapters & Chargers'
                    products[product]['type_standard'] = 'Electronics > Electronics Accessories > Power > Power Adapters & Chargers'                    
                
                elif products[product]['product_type'] == 'Cable':
                    products[product]['type_standard_id'] = '1456'
                    products[product]['type_standard_name'] = 'System & Power Cables'
                    products[product]['type_standard'] = 'Electronics > Electronics Accessories > Cables > System & Power Cables'
                
                else:
                    products[product]['custom_product_type'] = products[product]['product_type']
        return products
    
    def setVendor(self, products) -> dict:
        for product in products:            
            if products[product]['parent'] == True:                
                vendor = products[product]['manufacturer']                
                if not vendor:                    
                    vendor = 'urrem.dk'
                products[product]['vendor'] = vendor
                                        
        return products