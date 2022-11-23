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
        Database().createAndInsertTables()     
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
        products = readCsv.getProducts(language = language)
        # # Handle
        products = make.handle(products = products)
        # Check if product is parent
        products = make.checkIfParent(products = products)
        products = make.createOptionOne(products = products)
        # Additonal Images
        products = image.createBaseImage(products = products)
        products = image.createAdditonalImages(products = products)        
        # Create Alt tags
        products = image.createImageAltText(products = products)        
        products = metafield.colors(products = products, language = language)        
        products = metafield.size(products = products)
        # Remove content from child
        products = parent.removeContentFromChild(products = products)
        # Create compatible with / Categories
        productsAndCollections = make.createCategories(products = products)
        products = productsAndCollections[0]
        missingCollections = productsAndCollections[1]        
        # # Check for new categories (Collections)                
        CreateCollection(newCollections = missingCollections, language = language)
        # # Add Missing Content to parent products 
        products = parent.addProductTypes(products = products)
        products = parent.setVendor(products = products)
        # products = metafield.compatibleWith(products = products)
        # Translate Attributes
        products = translate.translateAttributes(products = products, language = language)
        products = metafield.material(products = products)                
        # Create Content
        products = Content().create(products = products)        
        # Currency convert        
        products = prices.getPrices(products = products, currency = 'dkk')
        # Clean attributes
        products = make.cleanAndFormat(products = products)
        # Save CSVs
        save.csv(products = products, language = language)
        save.saveAdditionalImageFile(products = products, language = language)

if __name__ == '__main__':
    Main()