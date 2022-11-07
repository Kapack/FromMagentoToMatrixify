from itertools import groupby
from config.constants import LOCALWORDS

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def convertListToString(theList : list) -> str:
    listToString : str
    listToString = ', '.join(str(e) for e in theList)                
    return listToString

def getModelName(product : dict) -> str:
  modelName : str = ''
  manufacturer : str = product['manufacturer'] 
  productCategories : list = product['categories']  
  # Clean up the categories  
  while manufacturer in productCategories : productCategories.remove(manufacturer)    
      
  # Deciding on modelname
  if len(productCategories) == 1:
    modelName = productCategories[0]    
  if len(productCategories) == 2:    
    modelName = productCategories[0] + ' / ' + productCategories[1]
  
  if len(productCategories) > 2:    
    # Getting first word in each categories
    word = [i.split()[0] for i in productCategories]
    # Check if all elements is equal / Every element is the same
    isSame = all_equal(word)    
    if(isSame):
        modelName = LOCALWORDS['dk']['universel'].capitalize() + ' ' + word[0]    
    else:
        modelName = LOCALWORDS['dk']['universel'].capitalize() + ' Smartwatch'
   
  # Make sure we have manufacturer as first element in categories, the while loop removes all 
  if manufacturer:     
    productCategories.insert(0, manufacturer)                                         
  return modelName


