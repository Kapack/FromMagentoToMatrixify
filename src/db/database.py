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
            
    def create_and_insert_tables(self) -> None:
        # Attributes        
        ProductAttributes()
        # Descriptions
        ProductTexts()
         # Collections
        Collections()

class ProductAttributes(Database):
    def __init__(self):                
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
        sql = 'CREATE TABLE if not exists materials (id integer primary key not null, material text, dk text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/attributes/materials.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO materials VALUES(?, ?, ?)', (i, row['material'], row['dk'] ))
                i += 1
                conn.commit()

    def create_insert_product_type(self):
        sql = 'CREATE TABLE if not exists product_types (id integer primary key not null, product_type text, dk text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/attributes/product_types.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO product_types VALUES(?, ?, ?)', (i, row['product_type'], row['dk'] ))
                i += 1
                conn.commit()

    def create_insert_addjective(self):
        sql = 'CREATE TABLE if not exists addjectives (id integer primary key not null, material text, product_type text, dk_addjective text)'
        c.execute(sql)
        with open(DB_PATH + 'csv/attributes/materials_addjectives.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO addjectives VALUES(?, ?, ?, ?)', (i, row['material'].lower().strip(), row['product_type'].lower().strip(), row['dk_addjective'].strip() ))
                i += 1
                conn.commit()                


    def create_insert_sizes(self):
        sql = 'CREATE TABLE if not exists sizes (id integer primary key not null, size text, dk text)'
        c.execute(sql)
    
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
        self.create_insert_watch_band_intro()
        self.create_insert_watch_band_material()
        self.create_insert_watch_band_ending()
        self.create_insert_screen_protector_intros()
        self.create_insert_cover_intros()
        self.create_insert_cover_materials()
        self.create_insert_cover_endings()

    # Specific texts
    def create_insert_watch_band_intro(self):
        sql = 'CREATE TABLE if not exists watch_band_intro_texts (id integer primary key not null, dk text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/descriptions/watch_band/intros.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO watch_band_intro_texts VALUES(?, ?)', (i, row['dk']  ))
                i += 1
                conn.commit()

    def create_insert_watch_band_material(self):
        sql = 'CREATE TABLE if not exists watch_band_material_texts (id integer primary key not null, material_text text, dk text)'
        c.execute(sql)
    
        with open(DB_PATH + 'csv/descriptions/watch_band/material_texts.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO watch_band_material_texts VALUES(?, ?, ?)', (i, row['material_text'],row['dk'] ))
                i += 1
                conn.commit()

    def create_insert_watch_band_ending(self):
        sql = 'CREATE TABLE if not exists watch_band_ending_texts (id integer primary key not null, dk text)'
        c.execute(sql)
    
        with open(DB_PATH + 'csv/descriptions/watch_band/endings.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO watch_band_ending_texts VALUES(?, ?)', (i, row['dk']))
                i += 1
                conn.commit()
    
    def create_insert_screen_protector_intros(self):
        sql = 'CREATE TABLE if not exists screen_protecter_intro_texts (id integer primary key not null, dk text)'
        c.execute(sql)

        with open(DB_PATH + 'csv/descriptions/screen_protecter/intros.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO screen_protecter_intro_texts VALUES(?, ?)', (i, row['dk']))
                i += 1
                conn.commit()

    def create_insert_cover_intros(self):
        sql = 'CREATE TABLE if not exists cover_intro_texts (id integer primary key not null, dk text)'
        c.execute(sql)
    
        with open(DB_PATH + 'csv/descriptions/cover/intros.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO cover_intro_texts VALUES(?, ?)', (i, row['dk']))
                i += 1
                conn.commit()

    def create_insert_cover_materials(self):
        # Create Table
        sql = 'CREATE TABLE if not exists cover_material_texts (id integer primary key not null, material_text text, dk text)'
        c.execute(sql)
        # Insert values
        with open(DB_PATH + 'csv/descriptions/cover/material_texts.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO cover_material_texts VALUES(?, ?, ?)', (i, row['material_text'],row['dk'] ))
                i += 1
                conn.commit()

    def create_insert_cover_endings(self):
        # Create Table
        sql = 'CREATE TABLE if not exists cover_ending_texts (id integer primary key not null, dk text)'
        c.execute(sql)
        # Insert values
        with open(DB_PATH + 'csv/descriptions/cover/endings.csv', 'r') as file: 
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO cover_ending_texts VALUES(?, ?)', (i, row['dk']))
                i += 1
                conn.commit()


class Collections(Database):
    def __init__(self):        
        self.create_insert_collections()
        self.create_insert_collection_page_titles()
        self.create_insert_collection_meta_desc()
        self.create_insert_collection_description()
        self.create_insert_grand_parent_bottom_description()
        self.create_insert_child_bottom_description()
        self.create_insert_collection_kw_research()
        self.create_insert_collection_ads_keywords()

    def create_insert_collections(self):
      sql = 'CREATE TABLE if not exists collections (id integer primary key not null, name text, belongs_to text, relationship_type text)'
      c.execute(sql)

      with open(DB_PATH + 'csv/collections/collections.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        i = 1
        for row in reader:                      
          c.execute('INSERT INTO collections VALUES(?,?,?,?)', (i, row['name'], row['belongs_to'], row['relationship_type']) )
          i += 1
          conn.commit()
    
    def create_insert_collection_page_titles(self):
      sql = 'CREATE TABLE if not exists collection_page_title (id integer primary key not null, kw text, cta text)'
      c.execute(sql)        
    
      with open(DB_PATH + 'csv/collections/text/collection-meta-title.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        i = 1
        for row in reader:
          c.execute('INSERT INTO collection_page_title VALUES(?,?,?)', (i, row['kw'], row['cta']) )
          i += 1
          conn.commit()
    
    def create_insert_collection_meta_desc(self):
        sql = 'CREATE TABLE if not exists collection_meta_desc (id integer primary key not null, meta_desc text)'
        c.execute(sql) 
    
        with open(DB_PATH + 'csv/collections/text/collection-meta-title.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_meta_desc VALUES(?,?)', (i, row['meta_desc']) )
                i += 1
                conn.commit()
    
    def create_insert_collection_description(self):
        sql = 'CREATE TABLE if not exists collection_description (id integer primary key not null, description text)'
        c.execute(sql)
    
        with open(DB_PATH + 'csv/collections/text/collection-description.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_description VALUES(?,?)', (i, row['description']) )
                i += 1
                conn.commit()
    """
    Bottom Texts
    """
    def create_insert_grand_parent_bottom_description(self):
        sql = 'CREATE TABLE if not exists collection_grandparent_bottom_description (id integer primary key not null, h2 text, content text, language text)'
        c.execute(sql)

        language = 'dk'
        base_path = DB_PATH + '/csv/collections/text/grandparent-bottom-description.ods'
        sheet = language
        df = read_ods(base_path , sheet)
        df = df.fillna("")
        df = df.to_dict(orient='index')
        
        i = 1
        for row in df:
            c.execute('INSERT INTO collection_grandparent_bottom_description VALUES(?,?,?,?)', (i, df[row]['h2'], df[row]['content'], language) )
            i += 1
            conn.commit()

    def create_insert_child_bottom_description(self):
        sql = 'CREATE TABLE if not exists collection_child_bottom_description (id integer primary key not null, h2 text, content text, language text)'
        c.execute(sql)

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
    
    """
    Keywords
    """
    def create_insert_collection_kw_research(self):
        sql = 'CREATE TABLE if not exists collection_kw_research (id integer primary key not null, device text, keyword text, volume integer)'
        c.execute(sql)
    
        with open(DB_PATH + 'csv/collections/collections-kw-research.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            i = 1
            for row in reader:
                c.execute('INSERT INTO collection_kw_research VALUES(?,?,?,?)', (i, row['device'], row['keyword'], row['volume']) )
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