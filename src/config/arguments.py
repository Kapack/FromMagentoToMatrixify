import argparse
from config.constants import BGCOLORS
from lib.make.collection.collection import UpdateCollection

"""
CLI Arguments
"""

class Arguments:

    def run(self) -> str:
        # Initialize parser
        parser = argparse.ArgumentParser()

        # Adding optional argument
        parser.add_argument("-c", "--collection", choices=['yes'], help = "Saves a .csv file with all collections stored in db/csv.")
        parser.add_argument("-l", "--language", default='dk', nargs='?', help = "Type which language you're creating for? Use abbr. dk, se, no etc. ")        
        # Read arguments from command line
        args = parser.parse_args()
        
        # Validating language
        language : str = args.language.lower()
        if language not in ['dk', 'se']:
            print(BGCOLORS['FAIL'] + 'Sorry. ' + language + ' is not a valid language option. Exiting.' + BGCOLORS['ENDC'])            
            exit()
        
        # If we want to generate collection again, skip all products creations
        if args.collection and args.collection.lower() == 'yes':
            UpdateCollection()                   
            exit() 
    
        return language
