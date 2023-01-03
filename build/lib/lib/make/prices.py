import math

class Prices:
    # Original currency is EU
    def get_prices(self, products:dict, currency:str):
        for product in products:
            
            if(products[product]['prices']['price']):
                # First convert to SEK / we're calculating backwards, compared to org. Magento .csv workflow            
                org_price_sek = self.convert_to_sek(price = products[product]['prices']['price'])
                # If special price is set
                # Special price will be Variant Price, and the org Price will be compare price
                if(products[product]['prices']['special_price']):
                    special_price_sek = self.convert_to_sek(price = products[product]['prices']['special_price'])
                
                # Setting product price, according to currency
                if currency == 'dkk':
                    price_dkk = self.convert_to_dkk(price = org_price_sek)
                    products[product]['prices']['variant_price'] = price_dkk
                    # If product has a special price, overwrite
                    if(products[product]['prices']['special_price']):
                        special_price_dkk = self.convert_to_dkk(price = special_price_sek)
                        products[product]['prices']['variant_price'] = special_price_dkk
                        products[product]['prices']['variant_compare_price'] = price_dkk

        return products

    def convert_to_sek(self, price) -> int:
        # Euro to SEK
        sek = float(price) / .11
        # Roundup to nearest 9
        sek = self.round_up_to_nearest_nine(price = sek)
        return sek
    
    def convert_to_dkk(self, price) -> float:
        # SEK to DKK
        dkk = price * 0.7
        # Roundup to nearest 9
        dkk = self.round_up_to_nearest_nine(price = dkk)
        return dkk

    def round_up_to_nearest_nine(self, price) -> int:
        # Roundup to nearest 10 and minus 1 (Nearest 9)
        price = int(math.ceil(price / 10) * (10) - 1)
        return price