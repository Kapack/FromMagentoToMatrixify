"""
Collection is created from the Magento field _category,
This field will be the same as Tag in ImportToMatrixify.csv
"""

from db.select import SelectCollection
from config.constants import CONTENT_DIR_IMPORT_TO_MATRIXIFY, BGCOLORS, CUSTOM_COLLECTION_BOTTOM_DESCRIPTIONS
from slugify import slugify
import random
import pandas as pd

# Super
class Collection:
  def __init__(self) -> None:
    self.select = SelectCollection()
    self.collectionKwResearch : list[dict] = self.select.collection_keyword_research()
    self.collectionAdsKw : list = self.select.collection_ads_keyword()

  # Create default page tile      
  def collectionPageTitle(self, collectionName:str) -> str:
    pageTitle : str
    pageTitles = self.select.collection_page_title()

    # Get a default random kw
    randomKw = random.choice(pageTitles['kw'])
    first_pt = collectionName + ' ' + randomKw
    
    # Using most searched keyword if it exists
    mostSearchedKeywords = self.mostSearchedKeywords(collectionName = collectionName)
    if mostSearchedKeywords['first']:
      first_pt = mostSearchedKeywords['first']      
                    
    # Chose a random CTA
    randomCta = random.choice(pageTitles['cta'])
    
    if '[DEVICE]' in randomCta:
      randomCta = randomCta.replace('[DEVICE]', collectionName)
          
    pageTitle = first_pt + ' | ' + randomCta

    return pageTitle
  
  # Create default meta description
  def collectionMetaDesc(self, collectionName:str) -> str:
    meta_desc : str
    meta_descs = self.select.collection_meta_desc()
    # pick a random from list
    meta_desc = random.choice(meta_descs)
    # Replace [DEVICE] variable in text
    if '[DEVICE]' in meta_desc:
      meta_desc = meta_desc.replace('[DEVICE]', collectionName)
    
    return meta_desc
  
  # Header Description
  def collectionDescription(self, collection_name:str, relationship_type : str = '') -> str:    
    description : list = ['']

    if relationship_type.lower() == 'grandparent':
      description = self.select.grandparent_description()
    
    if relationship_type.lower() == 'parent':
      description = self.select.parent_description()

    if relationship_type.lower() == 'child':
      description = self.select.child_description()
    # Default description    
    else: 
      description = self.select.child_description()

    # Pick random
    description = random.choice(description)
    
    # Replace variables
    if '[DEVICE]' in description:
      description = description.replace('[DEVICE]', collection_name)

    return description

  # Bottom SEO Text
  def bottomDescription(self, collection:dict) -> str:        
    bottomTxt : str = ''
    bottomDescs : list[dict] = []

    if collection['relationship_type'].lower() == 'grandparent':
      # Get texts
      bottomDescs : list[dict] = self.select.grandparent_bottom_description()
      # Choosing default random text
      bottomTxt = random.choice(bottomDescs)

    if collection['relationship_type'].lower() == 'child':
      # Get texts
      bottomDescs : list[dict] = self.select.child_bottom_description()      
      # Picking a default random from bottom descriptions    
      bottomTxt = random.choice(bottomDescs)

    # Using most searched keyword if it exists
    mostSearchedKeywords = self.mostSearchedKeywords(collectionName = collection['name'])            
    if mostSearchedKeywords['second']:
      second_most_searched = mostSearchedKeywords['second'].lower()
      second_most_searched_as_device = second_most_searched.replace(collection['name'].lower(), '[DEVICE]')        

      # If there is a second most searched. Chose a headline, where keyword exists.      
      allSecondTxt = []        
      for desc in bottomDescs:
        if collection['name'].lower() == 'apple watch':          
          # if sentence exists as a Description H2. Append all to list
          if second_most_searched_as_device.lower() in desc['h2'].lower():
            allSecondTxt.append(desc)
      
      # Picking random
      if allSecondTxt:
        # Getting a random text from picked keywords
        bottomTxt = random.choice(allSecondTxt)        
      
    # Create text and replace DEVICE        
    if bottomTxt != '':        
      bottomTxt = '<h2>' + bottomTxt['h2'] + '</h2>' + '<p>' + bottomTxt['content'] + '</p>'
      bottomTxt = bottomTxt.replace('[DEVICE]', collection['name'])      
    
    return bottomTxt
  
  # Google Ads
  def createGoogleAds(self, collections, language) -> None:
    adsKeywords = self.collectionAdsKw
    collectionNames : list[str] = collections

    # if collections comes from update (dict), we don't want dict but only a list with names
    if type(collectionNames[0]) == dict:
      collectionNames = [collection['name'] for collection in collectionNames]      

    keywords = []    
    for name in collectionNames:      
      ads_kw = []
      for kw in adsKeywords:
        if '[DEVICE]' in kw:
          # Create a list of keywords
          ads_kw.append(kw.replace('[DEVICE]', name))      

      # Create dictionary
      keywords.append({ 'name' : name, 'keywords' : ', '.join(ads_kw), 'negative_keywords' : '[' + name + ']' })
    # Save collection
    self.saveCollection(collections = keywords, filepath = '/ads/'+ language +'-kws.csv', msg = 'Google Ads Keywords created\n', msg_type = 'WARNING')    

  def saveCollection(self, collections : list[dict], filepath : str, msg : str, msg_type : str):
    # Save as csv
    df = pd.DataFrame.from_dict(collections)
    df.to_csv (CONTENT_DIR_IMPORT_TO_MATRIXIFY + filepath, index = False, header=True)  
    print(BGCOLORS[msg_type] + msg + BGCOLORS['ENDC'])

  def mostSearchedKeywords(self, collectionName : str) -> dict[str]:
    mostSearched = {'first' : '', 'second' : ''}

    # If name exists in keyword research
    searchedKws : dict[str] = {}
    
    for key in self.collectionKwResearch:      
      if key['device'].lower() == collectionName.lower():
        searchedKws[key['keyword']] = key['volume']
        
    # If there's a keyword research
    if searchedKws:
      # Get the one with max search volume
      first = max(searchedKws, key = searchedKws.get)
      mostSearched['first'] = first
      # second most searched
      for keyword, volume in searchedKws.items():        
        if volume < searchedKws[first] and max:          
          mostSearched['second'] = keyword

    return mostSearched
    
# Subclass
class CreateCollection(Collection):  
  def __init__(self, newCollections : list[dict], language : str) -> None:
    super().__init__()
    # Only run if any new collections
    if(newCollections):
      missingCollection = self.newCollections(newCollections)
      msg = 'Product Import list NOT created!\n' + str(len(newCollections)) + ' Missing collections was found. \n Todo: \n 0: Find the new categories in import/0-new-smart-collections.csv \n 1: update Shopify with new collections. \n 2: Update db/csv/collections.csv \n 3: Update shopify/other - page \n 4: Run this code again \n 5: Import products'      
      self.createGoogleAds(collections = newCollections, language = language)      
      self.saveCollection(collections=missingCollection, filepath= '0-new-'+ language +'-smart-collections.csv', msg = msg, msg_type = 'FAIL')    

  def newCollections(self, missingCollections:list[dict]) -> list[dict]:    
    newCollections : list = []        

    for collection in missingCollections:            
      pageTitle = self.collectionPageTitle(collection)
      metaDesc = self.collectionMetaDesc(collection)
      description = self.collectionDescription(collection)      
      newCollections.append({
        'Handle' : slugify(collection),          
        'Command' : 'MERGE',
        'Title' : collection,
        'Body HTML' : description,
        'Must Match' : 'all conditions', 
        'Rule: Product Column' : 'Tag', 
        'Rule: Relation' : 'Equals', 
        'Rule: Condition' : collection,
        'Metafield: title_tag [string]' : pageTitle,
        'Metafield: description_tag [string]' : metaDesc,        
      })

    return newCollections

# Subclass
class UpdateCollection(Collection):  
  def __init__(self, language:str) -> None:
    super().__init__()
    self.allCollections : list[dict] = self.select.collections()
    child_collections = self.childCollection()    
    parent_collections = self.parentCollection()        
    self.createGoogleAds(collections = self.allCollections, language = language)
    msg = 'Child collection list has been created. Be aware of what you\'re overwriting'
    self.saveCollection(collections = child_collections, filepath = 'updated-collections/update-child-'+ language +'-smart-collections.csv', msg = msg, msg_type = 'WARNING')
    msg = 'Parent collection list has been created. Be aware of what you\'re overwriting'
    self.saveCollection(collections = parent_collections, filepath = 'updated-collections/update-parents-'+ language +'-smart-collections.csv', msg = msg, msg_type = 'WARNING')


  def childCollection(self) -> list[dict]:    
    updateCollections : list[dict] = []    

    for collection in self.allCollections:
      if collection['relationship_type'].lower() == 'child':      
        # We don't want to overwrite custom/unique written text
        if collection['name'].lower() not in CUSTOM_COLLECTION_BOTTOM_DESCRIPTIONS:

          pageTitle = self.collectionPageTitle(collection['name'])
          metaDesc = self.collectionMetaDesc(collection['name'])
          description = self.collectionDescription(collection_name = collection['name'],  relationship_type = collection['relationship_type'])
          templateSuffix = self.collectionTemplate(collection['relationship_type'])
          bottomDescription = self.bottomDescription(collection=collection)
          
          updateCollections.append({
            'Handle' : slugify(collection['name']),  
            'Command' : 'Merge',      
            'Title' : collection['name'],
            'Body HTML' : description,
            'Must Match' : 'all conditions', 
            'Rule: Product Column' : 'Tag', 
            'Rule: Relation' : 'Equals', 
            'Rule: Condition' : collection['name'],
            'Metafield: title_tag [string]' : pageTitle,
            'Metafield: description_tag [string]' : metaDesc,
            'Template Suffix' : templateSuffix,
            'Metafield: custom.belongs_to [single_line_text_field]' : collection['belongs_to'],
            'Metafield: custom.bottom_description [multi_line_text_field]' : bottomDescription,
          })
          # Adding Variant Inventory condition
          updateCollections.append({
            'Handle' : slugify(collection['name']),  
            'Command' : 'Merge',      
            'Title' : '',
            'Body HTML' : '',
            'Must Match' : '', 
            'Rule: Product Column' : 'Variant Inventory', 
            'Rule: Relation' : 'Greater Than', 
            'Rule: Condition' : '0',
            'Metafield: title_tag [string]' : '',
            'Metafield: description_tag [string]' : '',
            'Template Suffix' : '',
            'Metafield: custom.belongs_to [single_line_text_field]' : '',
            'Metafield: custom.bottom_description [multi_line_text_field]' : '',
          })

    
    return updateCollections

  def parentCollection(self) -> list[dict]:
    updateCollections : list[dict] = []    
    
    for parent_collection in self.allCollections:
      if parent_collection['relationship_type'].lower() == 'parent' or parent_collection['relationship_type'].lower() == 'grandparentparent':
        # We don't want to overwrite custom/unique written text
        if parent_collection['name'].lower() not in CUSTOM_COLLECTION_BOTTOM_DESCRIPTIONS:
          
          pageTitle = self.collectionPageTitle(parent_collection['name'])
          metaDesc = self.collectionMetaDesc(parent_collection['name'])
          description = self.collectionDescription(collection_name = parent_collection['name'],  relationship_type = parent_collection['relationship_type'])
          templateSuffix = self.collectionTemplate(parent_collection['relationship_type'])
          bottomDescription = self.bottomDescription(collection=parent_collection)
          
          updateCollections.append({
            'Handle' : slugify(parent_collection['name']),  
            'Command' : 'Merge',      
            'Title' : parent_collection['name'],
            'Body HTML' : description,
            'Must Match' : 'any condition', 
            'Rule: Product Column' : 'Tag', 
            'Rule: Relation' : 'Equals', 
            'Rule: Condition' : parent_collection['name'],
            'Metafield: title_tag [string]' : pageTitle,
            'Metafield: description_tag [string]' : metaDesc,
            'Template Suffix' : templateSuffix,
            'Metafield: custom.belongs_to [single_line_text_field]' : parent_collection['belongs_to'],
            'Metafield: custom.bottom_description [multi_line_text_field]' : bottomDescription,
          })
          
          # Appending parent conditions (Child)
          # Loop through collections and find all where belongsTo, is current name
          childs = [collection for collection in self.allCollections if collection['belongs_to'].lower() == parent_collection['name'].lower()]
          for child in childs:            
            updateCollections.append({
              'Handle' : slugify(parent_collection['name']),  
              'Command' : 'Merge',      
              'Title' : '',
              'Body HTML' : '',
              'Must Match' : '', 
              'Rule: Product Column' : 'Tag', 
              'Rule: Relation' : 'Equals', 
              'Rule: Condition' : child['name'],
              'Metafield: title_tag [string]' : '',
              'Metafield: description_tag [string]' : '',
              'Template Suffix' : '',
              'Metafield: custom.belongs_to [single_line_text_field]' : '',
              'Metafield: custom.bottom_description [multi_line_text_field]' : '',
            })
    

    return updateCollections

  
  

  # Chosing template
  def collectionTemplate(self, relationship_type:str) -> str:
    templateSuffix = ''
    if relationship_type.lower() == 'parent' or relationship_type.lower() == 'grandparent':
      templateSuffix = 'parent-collection'
    
    return templateSuffix