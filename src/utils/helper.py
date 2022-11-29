from itertools import groupby
from config.constants import LOCALWORDS

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def convert_list_to_string(the_list : list) -> str:
    list_to_string : str
    list_to_string = ', '.join(str(e) for e in the_list)                
    return list_to_string

def get_model_name(product : dict) -> str:
  model_name : str = ''
  manufacturer : str = product['manufacturer'] 
  product_categories : list = product['categories']['category']  
  # Clean up the categories  
  while manufacturer in product_categories : product_categories.remove(manufacturer)    
      
  # Deciding on modelname
  if len(product_categories) == 1:
    model_name = product_categories[0]    
  if len(product_categories) == 2:    
    model_name = product_categories[0] + ' / ' + product_categories[1]
  
  if len(product_categories) > 2:    
    # Getting first word in each categories
    word = [i.split()[0] for i in product_categories]
    # Check if all elements is equal / Every element is the same
    is_same = all_equal(word)    
    if(is_same):
        model_name = LOCALWORDS['dk']['universel'].capitalize() + ' ' + word[0]    
    else:
        model_name = LOCALWORDS['dk']['universel'].capitalize() + ' Smartwatch'
   
  # Make sure we have manufacturer as first element in categories, the while loop removes all 
  if manufacturer:     
    product_categories.insert(0, manufacturer)                                         
  return model_name


