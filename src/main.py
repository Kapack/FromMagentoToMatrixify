from config.arguments import Arguments
from db.database import Database
from lib.make.metafield import Metafield
from lib.read_files.read_csv import ReadCsv
from lib.make.make import Make
from lib.make.collection.collection import CreateCollection
from lib.make.image import Image
from lib.make.parent import Parent
from lib.make.content.content import Content
from lib.make.prices import Prices
from lib.translate.translate import Translate
from lib.save_files.save_files import SaveFiles

class Main:
    products : dict             
    
    def __init__(self) -> None:
        # We are creating the DB every time.
        Database().create_and_insert_tables()     
        # CLI Arguments     
        language = Arguments().run()   
        # Read CSV
        readCsv = ReadCsv()        
        make = Make()
        metafield = Metafield()
        image = Image()
        parent = Parent()
        translate = Translate()
        prices = Prices()
        save = SaveFiles()
        
        """
        Run
        """
        # Products
        products = readCsv.get_products(language = language)
        # # Handle
        products = make.handle(products = products)
        # Check if product is parent
        products = make.check_if_parent(products = products)
        products = make.create_option_one(products = products)
        # Additonal Images
        products = image.create_base_image(products = products)
        products = image.create_additonal_images(products = products)        
        # Create Alt tags
        products = image.create_image_alt_text(products = products)        
        products = metafield.colors(products = products, language = language)        
        products = metafield.size(products = products)
        # Remove content from child
        products = parent.remove_content_from_child(products = products)
        # Create compatible with / Categories
        products_and_collections = make.create_categories(products = products)
        products = products_and_collections[0]
        missing_collections = products_and_collections[1]        
        # # Check for new categories (Collections)                
        CreateCollection(newCollections = missing_collections, language = language)
        # # Add Missing Content to parent products 
        products = parent.add_product_types(products = products)
        products = parent.set_vendor(products = products)
        # products = metafield.compatibleWith(products = products)
        # Translate Attributes
        products = translate.translate_attributes(products = products, language = language)
        products = metafield.material(products = products)                
        # Create Content
        products = Content().create(products = products)        
        # Currency convert        
        products = prices.get_prices(products = products, currency = 'dkk')
        # Clean attributes
        products = make.clean_and_format(products = products)
        # Save CSVs
        save.csv(products = products, language = language)
        save.additional_image_file(products = products, language = language)

if __name__ == '__main__':
    Main()