from config.constants import DB_PATH, LOCALWORDS
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

    def create_and_insert_tables(self, language : str) -> None:                                
        # Attributes        
        ProductAttributes(language = language)
        # Descriptions
        ProductTexts(language = language)
         # Collections
        Collections(language = language)

# Attributes
class ProductAttributes(Database):
    def __init__(self, language : str):    
        self.language = language             
        self.create_insert_color()
        self.create_insert_material()
        self.create_insert_product_type()
        self.create_insert_addjective()     
        self.create_insert_sizes()

    def create_insert_color(self):
        sql = 'CREATE TABLE if not exists colors (id integer primary key not null, color text, dk_singular text, dk_plural text, dk_neutrum text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/attributes/colors.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO colors VALUES(?, ?, ?, ?, ?)', (i, row['color'], row['dk_singular'], row['dk_plural'], row['dk_neutrum']))
                i += 1
                conn.commit()

    def create_insert_material(self):
        sql = 'CREATE TABLE if not exists materials (id integer primary key not null, material text, ' + self.language + ' text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/attributes/materials.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO materials VALUES(?, ?, ?)', (i, row['material'], row[self.language] ))
                i += 1
                conn.commit()

    def create_insert_product_type(self):
        sql = 'CREATE TABLE if not exists product_types (id integer primary key not null, product_type text, ' + self.language + ' text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/attributes/product_types.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO product_types VALUES(?, ?, ?)', (i, row['product_type'], row[self.language] ))
                i += 1
                conn.commit()

    def create_insert_addjective(self):
        sql = 'CREATE TABLE if not exists addjectives (id integer primary key not null, product_type text, material text, addjective)'
        c.execute(sql)

        base_path = DB_PATH + 'csv/attributes/materials_addjectives.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO addjectives VALUES(?,?,?,?)', (i, df[row]['product_type'], df[row]['material'], df[row]['addjective'] ))
            i += 1
            conn.commit()          

    def create_insert_sizes(self):
        sql = 'CREATE TABLE if not exists sizes (id integer primary key not null, size text, ' + self.language + ' text)'
        c.execute(sql)
    
        with open(DB_PATH + 'csv/attributes/sizes.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO sizes VALUES(?, ?, ?)', (i, row['size'], row[self.language]  ))
                i += 1
                conn.commit()

# Descriptions
class ProductTexts(Database):
    def __init__(self, language : str):
        self.language = language        
        self.create_insert_watch_band_intro()
        self.create_insert_watch_band_material()
        self.create_insert_watch_band_ending()
        self.create_insert_screen_protector_intros()
        self.create_insert_cover_intros()
        self.create_insert_cover_materials()
        self.create_insert_cover_endings()

    # Specific texts
    def create_insert_watch_band_intro(self):        
        sql = 'CREATE TABLE if not exists watch_band_intro_texts (id integer primary key not null, intro text)'
        c.execute(sql)

        base_path = DB_PATH + '/csv/descriptions/watch_band/intros.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO watch_band_intro_texts VALUES(?,?)', (i, df[row]['intro']) )
            i += 1
            conn.commit() 

    def create_insert_watch_band_material(self):
        sql = 'CREATE TABLE if not exists watch_band_material_texts (id integer primary key not null, material text, text text)'
        c.execute(sql)

        base_path = DB_PATH + '/csv/descriptions/watch_band/material_texts.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO watch_band_material_texts VALUES(?,?, ?)', (i, df[row]['material'], df[row]['text']) )
            i += 1
            conn.commit() 

    def create_insert_watch_band_ending(self):
        sql = 'CREATE TABLE if not exists watch_band_ending_texts (id integer primary key not null, ending text)'
        c.execute(sql)
        
        base_path = DB_PATH + '/csv/descriptions/watch_band/endings.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO watch_band_ending_texts VALUES(?,?)', (i, df[row]['ending']) )
            i += 1
            conn.commit() 
    
    def create_insert_screen_protector_intros(self):
        sql = 'CREATE TABLE if not exists screen_protector_intro_texts (id integer primary key not null, intro text)'
        c.execute(sql)
        
        base_path = DB_PATH + '/csv/descriptions/screen_protector/intros.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO screen_protector_intro_texts VALUES(?,?)', (i, df[row]['intro']) )
            i += 1
            conn.commit() 

    def create_insert_cover_intros(self):
        sql = 'CREATE TABLE if not exists cover_intro_texts (id integer primary key not null, intro text)'
        c.execute(sql)
        
        base_path = DB_PATH + '/csv/descriptions/cover/intros.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO cover_intro_texts VALUES(?,?)', (i, df[row]['intro']) )
            i += 1
            conn.commit()

    def create_insert_cover_materials(self):
        # Create Table
        sql = 'CREATE TABLE if not exists cover_material_texts (id integer primary key not null, material text, text  text)'
        c.execute(sql)

        base_path = DB_PATH + '/csv/descriptions/cover/material_texts.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO cover_material_texts VALUES(?,?,?)', (i, df[row]['material'], df[row]['text'] ) )
            i += 1
            conn.commit()

    def create_insert_cover_endings(self):
        # Create Table
        sql = 'CREATE TABLE if not exists cover_ending_texts (id integer primary key not null, ending text)'
        c.execute(sql)

        base_path = DB_PATH + '/csv/descriptions/cover/endings.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO cover_ending_texts VALUES(?,?)', (i, df[row]['ending']) )
            i += 1
            conn.commit()

# Collections
class Collections(Database):
    def __init__(self, language : str):             
        self.language = language        
        self.create_insert_collections()
        self.create_insert_collection_page_titles()
        self.create_insert_collection_meta_desc()

        self.create_insert_grandparent_description()
        self.create_insert_grandparent_bottom_description()
        
        self.create_insert_parent_collection_description()
        self.create_insert_parent_bottom_description()

        self.create_insert_child_collection_description()
        self.create_insert_child_bottom_description()
        
        self.create_insert_collection_kw_research()
        self.create_insert_collection_ads_keywords()        
    

    def create_insert_collections(self):
      sql = 'CREATE TABLE if not exists collections (id integer primary key not null, name text, belongs_to text, relationship_type text, alternative_names text)'
      c.execute(sql)

      with open(DB_PATH + 'csv/collections/collections.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        i = 1

        for row in reader:                 
            collection_name = row['name']
            if '[parent_col]' in collection_name.lower():
                collection_name = collection_name.replace('[PARENT_COL]', LOCALWORDS[self.language]['parent_col'].title())
            
            belongs_to = row['belongs_to']
            if '[parent_col]' in belongs_to.lower():
                belongs_to = belongs_to.replace('[PARENT_COL]', LOCALWORDS[self.language]['parent_col'].title())

            c.execute('INSERT INTO collections VALUES(?,?,?,?,?)', (i, collection_name, belongs_to, row['relationship_type'], row['alternative_names'] ))
            i += 1
            conn.commit()
    
    def create_insert_collection_page_titles(self):
        sql = 'CREATE TABLE if not exists collection_page_title (id integer primary key not null, kw text, cta text)'
        c.execute(sql)

        base_path = DB_PATH + '/csv/collections/text/collection-meta-title.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')   
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_page_title VALUES(?,?,?)', (i, df[row]['kw'], df[row]['cta']) )
            i += 1
            conn.commit()   
    
    def create_insert_collection_meta_desc(self):
        sql = 'CREATE TABLE if not exists collection_meta_desc (id integer primary key not null, meta_desc text)'
        c.execute(sql) 
        
        base_path = DB_PATH + '/csv/collections/text/collection-meta-title.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index') 

        i = 1
        for row in df:
            c.execute('INSERT INTO collection_meta_desc VALUES(?,?)', (i, df[row]['meta_desc']) )
            i += 1
            conn.commit()   
    
    """
    Grandparent descriptions
    """
    def create_insert_grandparent_description(self):
        sql = 'CREATE TABLE if not exists collection_grandparent_description (id integer primary key not null, description text)'
        c.execute(sql)
        base_path = DB_PATH + '/csv/collections/text/grandparent-description.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_grandparent_description VALUES(?,?)', (i, df[row]['description']) )
            i += 1
            conn.commit()   

    def create_insert_grandparent_bottom_description(self):
        sql = 'CREATE TABLE if not exists collection_grandparent_bottom_description (id integer primary key not null, h2 text, content text)'
        c.execute(sql)
        base_path = DB_PATH + '/csv/collections/text/grandparent-bottom-description.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_grandparent_bottom_description VALUES(?,?,?)', (i, df[row]['h2'], df[row]['content']) )
            i += 1
            conn.commit()    
    
    """
    Parent Descriptions
    """
    def create_insert_parent_collection_description(self):
        sql = 'CREATE TABLE if not exists collection_parent_description (id integer primary key not null, description text)'
        c.execute(sql)

        base_path = DB_PATH + '/csv/collections/text/parent-collection-description.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')

        i = 1
        for row in df:
            c.execute('INSERT INTO collection_parent_description VALUES(?,?)', (i, df[row]['description']) )
            i += 1
            conn.commit()

    def create_insert_parent_bottom_description(self):
        sql = 'CREATE TABLE if not exists collection_parent_bottom_description (id integer primary key not null, h2 text, content text)'
        c.execute(sql)
        base_path = DB_PATH + '/csv/collections/text/parent-collection-bottom-description.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_parent_bottom_description VALUES(?,?,?)', (i, df[row]['h2'], df[row]['content']) )
            i += 1
            conn.commit()   

    """
    Child descriptions
    """
    def create_insert_child_collection_description(self):
        sql = 'CREATE TABLE if not exists collection_child_description (id integer primary key not null, description text)'
        c.execute(sql)
    
        base_path = DB_PATH + '/csv/collections/text/child-collection-description.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_child_description VALUES(?,?)', (i, df[row]['description']) )
            i += 1
            conn.commit()

    
    def create_insert_child_bottom_description(self):
        sql = 'CREATE TABLE if not exists collection_child_bottom_description (id integer primary key not null, h2 text, content text)'
        c.execute(sql)
                
        base_path = DB_PATH + '/csv/collections/text/child-bottom-description.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_child_bottom_description VALUES(?,?,?)', (i, df[row]['h2'], df[row]['content']) )
            i += 1
            conn.commit()

    
    """
    Keywords
    """
    def create_insert_collection_kw_research(self):
        sql = 'CREATE TABLE if not exists collection_kw_research (id integer primary key not null, device text, keyword text, volume integer)'
        c.execute(sql)
        base_path = DB_PATH + 'csv/collections/collections-kw-research.ods'
        sheet = self.language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_kw_research VALUES(?,?,?,?)', (i, df[row]['device'], df[row]['keyword'], df[row]['volume']) )
            i += 1
            conn.commit()

    def create_insert_collection_ads_keywords(self):
        sql = 'CREATE TABLE if not exists collection_ads_kw (id integer primary key not null, keyword text)'
        c.execute(sql)
        
        with open(DB_PATH + 'csv/collections/ads/collections-common-kw.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_ads_kw VALUES(?,?)', (i, row['keyword']) )
                i += 1
                conn.commit()