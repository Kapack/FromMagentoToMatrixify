"""
Collection is created from the Magento field _category,
This field will be the same as Tag in ImportToMatrixify.csv
"""

from db.select import Select
from config.constants import CONTENT_DIR_IMPORT_TO_MATRIXIFY, BGCOLORS
from slugify import slugify
import random
import pandas as pd

# Super
class Collection:
  def __init__(self) -> None:
    self.select = Select()
    self.collectionKwResearch = self.select.collection_keyword_research()
    self.collectionAdsKw : list = self.select.collection_ads_keyword()

  # Create default page tile      
  def collectionPageTitle(self, collectionName:str) -> str:
    pageTitle : str
    pageTitles = self.select.collection_page_title()

    # Get a default random kw
    randomKw = random.choice(pageTitles['kw'])
    first_pt = collectionName + ' ' + randomKw

    # If name exists in keyword research, use that as a first part
    allFirsts = {}
    for key in self.collectionKwResearch:      
      if key['device'].lower() == collectionName.lower():
        # print(key['keyword'])
        allFirsts[key['keyword']] = key['volume']
    
    # If there's a keyword research
    if allFirsts:
      # Get the one with max search volume
      first_pt = max(allFirsts, key = allFirsts.get)
                    
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
  
  def collectionDescription(self, collectionName:str) -> str:    
    description : str
    description = self.select.collection_description()
    # Pick random
    description = random.choice(description)
    if '[DEVICE]' in description:
      description = description.replace('[DEVICE]', collectionName)

    return description

  def createGoogleAds(self, collections) -> None:
    adsKeywords = self.collectionAdsKw
    collectionNames : list[str] = collections

    # if collections comes from update, we don't want dict but only a list with names
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
    self.saveCollection(collections = keywords, filepath = '/ads/kw.csv', warningmsg = 'Google Ads Keywords created\n')    

  def saveCollection(self, collections : list[dict], filepath : str, warningmsg : str):
    # Save as csv
    df = pd.DataFrame.from_dict(collections)
    df.to_csv (CONTENT_DIR_IMPORT_TO_MATRIXIFY + filepath, index = False, header=True)  
    print(BGCOLORS['WARNING'] + warningmsg + BGCOLORS['ENDC'])
    
# Subclass
class CreateCollection(Collection):  
  def __init__(self, newCollections : list[dict]) -> None:
    super().__init__()
    # Only run if any new collections
    if(newCollections):
      missingCollection = self.newCollections(newCollections)
      msg = str(len(newCollections)) + ' missing collections was found. \n Todo: \n 1: update Shopify. \n 2: Update db/csv/collections.csv \n 3: Update shopify/other \n 4: Run main.py again \n 5: Import products'      
      self.createGoogleAds(collections = newCollections)      
      self.saveCollection(collections=missingCollection, filepath= '0-new-smart-collections.csv', warningmsg = msg)    

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
  def __init__(self) -> None:
    super().__init__()
    self.allCollections : list[dict] = self.select.collections()
    updateCollections = self.updateCollection()    
    msg = 'A updated collection list has been created. Be aware of what you\'re overwriting'
    self.createGoogleAds(collections = self.allCollections)
    self.saveCollection(collections = updateCollections, filepath = 'updated-collections/update-smart-collections.csv', warningmsg = msg)


  def updateCollection(self) -> list[dict]:    
    updateCollections : list[dict] = []    

    for collection in self.allCollections:
      pageTitle = self.collectionPageTitle(collection['name'])
      metaDesc = self.collectionMetaDesc(collection['name'])
      description = self.collectionDescription(collection['name'])
      templateSuffix = self.collectionTemplate(collection['relationship_type'])
      
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
      })
    
    return updateCollections    

  # Chosing template
  def collectionTemplate(self, relationship_type:str) -> str:
    templateSuffix = ''
    if relationship_type.lower() == 'parent':
      templateSuffix = 'parent-collection'
    
    return templateSuffix