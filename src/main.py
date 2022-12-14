from config.arguments import Arguments
from db.database import Database
from lib.make.collection.collection import UpdateCollection
from lib.make.metafield import Metafield
from lib.read_files.read_csv import ReadCsv
from lib.make.make import Make
from lib.make.collection.collection import CreateCollection
from lib.make.image import Image
from lib.make.parent_product.parent_product import ParentProduct
from lib.make.content.content import Content
from lib.make.prices import Prices
from lib.translate.translate import Translate
from lib.save_files.save_files import SaveFiles

class Main:
    products : dict             
    
    def __init__(self) -> None:
        # CLI Arguments     
        arguments = Arguments().run()   
        language = arguments.language.lower()            
        # We are creating the DB every time.
        Database().create_and_insert_tables(language = language)     
        
        # If we want to generate collection again, skip all products creations
        if arguments.collection and arguments.collection.lower() == 'yes':
            UpdateCollection(language = language)                   
            exit()                   
        
        # Read CSV
        readCsv = ReadCsv()        
        make = Make(language = language)
        metafield = Metafield()
        image = Image()
        parent = ParentProduct(language = language)        
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
        products = image.create_option_alt_text(products = products)        
        products = metafield.colors(products = products, language = language)        
        products = metafield.size(products = products)
        # Remove content from child
        products = parent.remove_content_from_child(products = products)
        # Create compatible with / Categories
        products_and_collections = make.create_categories(products = products)
        products = products_and_collections[0]
        missing_collections = products_and_collections[1]        
        
        if len(missing_collections) > 0:
        # Check for new categories (Collections)                
            CreateCollection(newCollections = missing_collections, language = language)
            exit()

        # Add Missing Content to parent products         
        products = parent.correcting_product_types(products = products)
        products = parent.set_shopify_product_types(products = products)
        # products = parent.set_models(products = products)
        products = parent.set_vendor(products = products)
        products = parent.set_material(products = products)
        products = parent.set_model(products = products)
        # Translate Attributes
        products = Translate().translate_attributes(products = products, language = language)
        products = metafield.material(products = products)                
        # Create Content
        products = Content().create(products = products, language = language)   
        products = image.create_seo_alt_text(products = products)
        # Currency convert        
        products = prices.get_prices(products = products, currency = 'dkk')
        # Clean attributes
        products = make.clean_and_format(products = products)
        # Save CSVs
        save.csv(products = products, language = language)
        save.additional_image_file(products = products, language = language)

if __name__ == '__main__':
    Main()