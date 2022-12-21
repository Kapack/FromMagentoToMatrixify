from itertools import groupby
from config.constants import LOCALWORDS

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def convert_list_to_string(the_list : list) -> str:
    list_to_string : str
    list_to_string = ', '.join(str(e) for e in the_list)                
    return list_to_string

"""
Replace last occurrence of a substring in a string
"""
def replace_last(string, old, new):
    if old not in string:
        return string

    index = string.rfind(old)

    return string[:index] + new + string[index+len(old):]

def get_model_name(product : dict, language : str) -> str:
  model_name : str = ''
  product_models : list = product['model']
  product_categories = product['categories']['category']  
  # product_type : str = product['product_types']['translate']    

  # Deciding on modelname
  if len(product_models) == 1:
    model_name = product_models[0]    
  if len(product_models) == 2:    
    model_name = product_models[0] + ' / ' + product_models[1]
  

  if len(product_categories) > 2:    
    # Getting first word in each categories
    word = [i.split()[0] for i in product_categories]
    # Check if all elements is equal / Every element is the same
    is_same = all_equal(word)    
    if(is_same):
        model_name = LOCALWORDS[language]['universel'].capitalize() + ' ' + word[0]
    else:
        model_name = LOCALWORDS[language]['universel'].capitalize()
   
  return model_name


