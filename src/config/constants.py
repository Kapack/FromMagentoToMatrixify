import os
# DIRECTORIES
DB_PATH = os.getcwd() + "/src/db/"
CONTENT_FILES_EXPORT_FROM_MAGENTO = os.getcwd() + "/files/export/magento/fromMagento.csv"
CONTENT_DIR_IMPORT_TO_MATRIXIFY = os.getcwd() + "/files/import/default/"

# EXTERNAL LINKS
MAGENTO_IMG_URL = 'https://lux-case.com/media/catalog/product'

# User Message Colors
BGCOLORS = { 'HEADER' : '\033[95m', 'OKBLUE' : '\033[94m', 'OKCYAN' : '\033[96m', 'SUCCESS' : '\033[42m', 'WARNING' : '\033[43m', 'FAIL' : '\033[91m', 'ENDC' : '\033[0m', 'BOLD' : '\033[1m', 'UNDERLINE' : '\033[4m' }

# LOCALWORDS = {'DK' : 'og'}
LOCALWORDS = {
    'dk' : 
    {
        'and' : 'og', 
        'universel' : 'universal', 
        'parent_col' : 'tilbehør', 
        'with' : 'med', 
        'in' : 'i'
    }, 
    'se' : 
    {
        'and' : 'och', 
        'universel' : 'universell', 
        'parent_col' : 'tillbehör', 
        'with' : 'med', 
        'in' : 'i'
    } 
}

LOCAL_DICT = {
    'color' : {
        'dk' : 'farve', 
        'se' : 'färg'
        } 
    }
