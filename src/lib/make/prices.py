import math

class Prices:
    # Original currency is EU
    def getPrices(self, products:dict, currency:str):
        for product in products:
            
            if(products[product]['price']):
                # First convert to SEK / we're calculating backwards, compared to org. Magento .csv workflow            
                org_price_sek = self.convertToSEK(price = products[product]['price'])
                # If special price is set
                # Special price will be Variant Price, and the org Price will be compare price
                if(products[product]['special_price']):
                    special_price_sek = self.convertToSEK(price = products[product]['special_price'])
                
                # Setting product price, according to currency
                if currency == 'dkk':
                    price_dkk = self.convertToDKK(price = org_price_sek)
                    products[product]['variant_price'] = price_dkk                
                    # If product has a special price, overwrite
                    if(products[product]['special_price']):
                        special_price_dkk = self.convertToDKK(price = special_price_sek)                  
                        products[product]['variant_price'] = special_price_dkk                
                        products[product]['variant_compare_price'] = price_dkk                

        return products

    def convertToSEK(self, price) -> int:
        # Euro to SEK
        sek = float(price) / .11
        # Roundup to nearest 9
        sek = self.roundUpToNearestNine(price = sek)
        return sek
    
    def convertToDKK(self, price) -> float:
        # SEK to DKK
        dkk = price * 0.7
        # Roundup to nearest 9
        dkk = self.roundUpToNearestNine(price = dkk)
        return dkk

    def roundUpToNearestNine(self, price) -> int:
        # Roundup to nearest 10 and minus 1 (Nearest 9)
        price = int(math.ceil(price / 10) * (10) - 1)
        return price