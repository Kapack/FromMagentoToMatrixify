from config.constants import DB_PATH
import sqlite3
import os
import csv
from pandas_ods_reader import read_ods

class Database():
    def __init__(self):		
        global conn
        global c
        # Delete Database, so we are fully updated                
        os.remove(DB_PATH + 'database.db')
        # Create new Database
        conn = sqlite3.connect(DB_PATH + 'database.db')
        conn.text_factory = str
        c = conn.cursor()
            
    def createAndInsertTables(self) -> None:
        # Attributes        
        ProductAttributes()
        # Descriptions
        ProductTexts()
         # Collections
        Collections()

class ProductAttributes(Database):
    def __init__(self):        
        self.createMaterial()
        self.insertMaterial()
        self.createColor()
        self.insertColor()
        self.createProductType()
        self.insertProductType()
        self.createAddjective()
        self.insertAddjective()                
        self.createSizes()
        self.insertSizes()

    def createColor(self):
        sql = 'CREATE TABLE if not exists colors (id integer primary key not null, color text, dk_singular text, dk_plural text, dk_neutrum text)'
        c.execute(sql)

    def insertColor(self):
        with open(DB_PATH + 'csv/attributes/colors.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO colors VALUES(?, ?, ?, ?, ?)', (i, row['color'], row['dk_singular'], row['dk_plural'], row['dk_neutrum']))
                i += 1
                conn.commit()

    def createMaterial(self):
        sql = 'CREATE TABLE if not exists materials (id integer primary key not null, material text, dk text)'
        c.execute(sql)

    def insertMaterial(self):
        with open(DB_PATH + 'csv/attributes/materials.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO materials VALUES(?, ?, ?)', (i, row['material'], row['dk'] ))
                i += 1
                conn.commit()

    def createProductType(self):
        sql = 'CREATE TABLE if not exists product_types (id integer primary key not null, product_type text, dk text)'
        c.execute(sql)

    def insertProductType(self):
        with open(DB_PATH + 'csv/attributes/product_types.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO product_types VALUES(?, ?, ?)', (i, row['product_type'], row['dk'] ))
                i += 1
                conn.commit()

    def createAddjective(self):
        sql = 'CREATE TABLE if not exists addjectives (id integer primary key not null, dk_addjective text)'
        c.execute(sql)

    def insertAddjective(self):
        with open(DB_PATH + 'csv/attributes/addjectives.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO addjectives VALUES(?, ?)', (i, row['dk_addjective'] ))
                i += 1
                conn.commit()

    def createSizes(self):
        sql = 'CREATE TABLE if not exists sizes (id integer primary key not null, size text, dk text)'
        c.execute(sql)
    
    def insertSizes(self):
        with open(DB_PATH + 'csv/attributes/sizes.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO sizes VALUES(?, ?, ?)', (i, row['size'], row['dk']  ))
                i += 1
                conn.commit()

# Descriptions
class ProductTexts(Database):
    def __init__(self):        
        self.createWatchBandIntroText()
        self.insertWatchBandIntroText()
        self.createWatchBandMaterialText()
        self.insertWatchBandMaterialText()
        self.createWatchBandEndingtext()
        self.insertWatchBandEndingText()

    # Specific texts
    def createWatchBandIntroText(self):
        sql = 'CREATE TABLE if not exists watch_band_intro_texts (id integer primary key not null, dk text)'
        c.execute(sql)

    def insertWatchBandIntroText(self):
        with open(DB_PATH + 'csv/descriptions/watch_band/intros.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO watch_band_intro_texts VALUES(?, ?)', (i, row['dk']  ))
                i += 1
                conn.commit()

    def createWatchBandMaterialText(self):
        sql = 'CREATE TABLE if not exists watch_band_material_texts (id integer primary key not null, material_text text, material_text_dk text)'
        c.execute(sql)
    
    def insertWatchBandMaterialText(self):
        with open(DB_PATH + 'csv/descriptions/watch_band/material_texts.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO watch_band_material_texts VALUES(?, ?, ?)', (i, row['material_text'],row['material_text_dk'] ))
                i += 1
                conn.commit()

    def createWatchBandEndingtext(self):
        sql = 'CREATE TABLE if not exists watch_band_ending_texts (id integer primary key not null, dk text)'
        c.execute(sql)
    
    def insertWatchBandEndingText(self):
        with open(DB_PATH + 'csv/descriptions/watch_band/endings.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO watch_band_ending_texts VALUES(?, ?)', (i, row['dk']))
                i += 1
                conn.commit()

class Collections(Database):
    def __init__(self):        
        self.createCollections()
        self.insertCollections()
        self.createCollectionPageTitles()
        self.insertCollectionPageTitles()
        self.createCollectionMetaDesc()
        self.insertCollectionMetaDesc()
        self.createCollectionDescription()
        self.insertCollectionDescription()
        self.createChildBottomDescription()
        self.insertChildBottomDescription()
        self.createCollectionKWResearch()
        self.insertCollectionKWResearch()
        self.createCollectionAdsKeywords()
        self.insertCollectionAdsKeywords()



    def createCollections(self):
      sql = 'CREATE TABLE if not exists collections (id integer primary key not null, name text, belongs_to text, relationship_type text)'
      c.execute(sql)

    def insertCollections(self):
      with open(DB_PATH + 'csv/collections/collections.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        i = 1
        for row in reader:                      
          c.execute('INSERT INTO collections VALUES(?,?,?,?)', (i, row['name'], row['belongs_to'], row['relationship_type']) )
          i += 1
          conn.commit()
    
    def createCollectionPageTitles(self):
      sql = 'CREATE TABLE if not exists collection_page_title (id integer primary key not null, kw text, cta text)'
      c.execute(sql)        
    
    def insertCollectionPageTitles(self):
      with open(DB_PATH + 'csv/collections/text/collection-meta-title.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        i = 1
        for row in reader:
          c.execute('INSERT INTO collection_page_title VALUES(?,?,?)', (i, row['kw'], row['cta']) )
          i += 1
          conn.commit()
    
    def createCollectionMetaDesc(self):
      sql = 'CREATE TABLE if not exists collection_meta_desc (id integer primary key not null, meta_desc text)'
      c.execute(sql) 
    
    def insertCollectionMetaDesc(self):
     with open(DB_PATH + 'csv/collections/text/collection-meta-title.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        i = 1
        for row in reader:
          c.execute('INSERT INTO collection_meta_desc VALUES(?,?)', (i, row['meta_desc']) )
          i += 1
          conn.commit()
    
    def createCollectionDescription(self):
      sql = 'CREATE TABLE if not exists collection_description (id integer primary key not null, description text)'
      c.execute(sql)
    
    def insertCollectionDescription(self):
        with open(DB_PATH + 'csv/collections/text/collection-description.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_description VALUES(?,?)', (i, row['description']) )
                i += 1
                conn.commit()
    
    def createChildBottomDescription(self):
        sql = 'CREATE TABLE if not exists collection_child_bottom_description (id integer primary key not null, h2 text, content text, language text)'
        c.execute(sql)

    def insertChildBottomDescription(self):
        language = 'dk'
        base_path = DB_PATH + '/csv/collections/text/child-bottom-description.ods'
        sheet = language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_child_bottom_description VALUES(?,?,?,?)', (i, df[row]['h2'], df[row]['content'], language) )
            i += 1
            conn.commit()
    
    
    def createCollectionKWResearch(self):
      sql = 'CREATE TABLE if not exists collection_kw_research (id integer primary key not null, device text, keyword text, volume integer)'
      c.execute(sql)
    
    def insertCollectionKWResearch(self):
        with open(DB_PATH + 'csv/collections/collections-kw-research.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_kw_research VALUES(?,?,?,?)', (i, row['device'], row['keyword'], row['volume']) )
                i += 1
                conn.commit()

    def createCollectionAdsKeywords(self):
      sql = 'CREATE TABLE if not exists collection_ads_kw (id integer primary key not null, keyword text)'
      c.execute(sql)
        
    def insertCollectionAdsKeywords(self):
        with open(DB_PATH + 'csv/collections/ads/collections-common-kw.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_ads_kw VALUES(?,?)', (i, row['keyword']) )
                i += 1
                conn.commit()