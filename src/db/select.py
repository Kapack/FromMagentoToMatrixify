from config.constants import DB_PATH
import sqlite3
import os

class Select:
    def __init__(self):
        global conn
        global c
        conn = sqlite3.connect(DB_PATH + 'database.db')
        c = conn.cursor()

    def materials(self) -> dict:
        sql = 'SELECT material, dk FROM materials'
        c.execute(sql)
        rows = c.fetchall()

        materials = {}
        i = 0
        for key in rows:            
            materials[i] = {'material': rows[i][0], 'dk' : rows[i][1] }
            i += 1
        return materials

    def product_types(self) -> dict:
        sql = 'SELECT product_type, dk FROM product_types'
        c.execute(sql)
        rows = c.fetchall()

        product_types = {}
        i = 0
        for key in rows:            
            product_types[i] = {'product_type': rows[i][0], 'dk' : rows[i][1] }
            i += 1
        return product_types

    def colors(self):
        sql = 'SELECT color, dk_singular, dk_plural, dk_neutrum FROM colors'
        c.execute(sql)
        rows = c.fetchall()
        # print(rows)

        colors = {}
        for idx, col in enumerate(rows):
            colors[col[0]] = rows[idx]
            #print(idx)
        #print(d['all black'])
        
        
        # colors = list(rows)
        # print(colors)
        return colors
        #supplier_skus = list(reader)

        # colors = {}
        # i = 0
        # for key in rows:            
        #     colors[i] = {'color': rows[i][0], 'dk_singular' : rows[i][1], 'dk_plural' : rows[i][2], 'dk_neutrum' : rows[i][3]}
        #     i += 1
        # return colors
        
    def addjectives(self) -> list:
        sql = 'SELECT dk_addjective FROM addjectives'
        c.execute(sql)
        rows = c.fetchall()

        dk_addjectives = []
        i = 0
        for key in rows:            
            dk_addjectives.append(rows[i][0])
            i += 1        
        return dk_addjectives
    
    # Descriptions 
    def sizes(self) -> dict:
        sql = 'SELECT size, dk FROM sizes'
        c.execute(sql)
        rows = c.fetchall()

        sizes = {}
        i = 0        
        for key in rows:            
            sizes[i] = {'size': rows[i][0], 'dk' : rows[i][1] }
            i += 1
        return sizes                

    # Specific product type
    def watchband_intro_texts(self) -> list:
      sql = 'SELECT dk FROM watch_band_intro_texts'
      c.execute(sql)
      rows = c.fetchall()

      dk_endings = []
      i = 0
      for key in rows:            
          dk_endings.append(rows[i][0])
          i += 1        
      return dk_endings

    def watchband_material_texts(self) -> dict:
        sql = 'SELECT material_text, material_text_dk FROM watch_band_material_texts'
        c.execute(sql)
        rows = c.fetchall()

        material_texts = {}
        i = 0
        for key in rows:            
            material_texts[i] = {'material_text': rows[i][0], 'material_text_dk' : rows[i][1] }
            i += 1
        return material_texts

    def watchband_ending_texts(self) -> list:
        sql = 'SELECT dk FROM watch_band_ending_texts'
        c.execute(sql)
        rows = c.fetchall()

        dk_endings = []
        i = 0
        for key in rows:            
            dk_endings.append(rows[i][0])
            i += 1        
        return dk_endings
    
    # Collections
    def collections(self) -> list[dict]:
      sql = 'SELECT name, belongs_to, relationship_type FROM collections'
      c.execute(sql)
      rows = c.fetchall()
      collections = []
      
      for i, key in enumerate(rows):
        collections.append({'name' : rows[i][0], 'belongs_to': rows[i][1], 'relationship_type' : rows[i][2]})
      
      return collections
    
    def collection_page_title(self) -> dict:
        sql = 'SELECT kw, cta FROM collection_page_title'
        c.execute(sql)
        rows = c.fetchall()

        page_titles = {'kw' : [], 'cta' : []}

        i = 0
        for key in rows:
            if rows[i][0]:            
                page_titles['kw'].append(rows[i][0])
            page_titles['cta'].append(rows[i][1])
            i += 1
                
        return page_titles
    
    def collection_meta_desc(self) -> list[str]:
        sql = 'SELECT meta_desc FROM collection_meta_desc'
        c.execute(sql)
        rows = c.fetchall()
        
        meta_descs = []

        i = 0
        for row in rows:
            if rows[i][0]:
                meta_descs.append(rows[i][0])                

            i += 1
        return meta_descs
    
    def collection_description(self) -> list[str]:
        sql = "SELECT description FROM collection_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions = []

        for key, value in enumerate(rows):
            descriptions.append(value[0])
        
        return descriptions
    
    def collection_keyword_research(self) -> list[dict]:
        sql = "SELECT device, keyword, volume FROM collection_kw_research"
        c.execute(sql)
        rows = c.fetchall()
        
        kws : list[dict] = []        

        for row in rows:
            kws.append({'device' : row[0].lower(), 'keyword' : row[1], 'volume': row[2] })

        return kws
