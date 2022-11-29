from config.constants import DB_PATH
import sqlite3

class Select:
    def __init__(self):
        global conn
        global c
        conn = sqlite3.connect(DB_PATH + 'database.db')
        c = conn.cursor()

    def materials(self, language:str) -> dict:
        sql = 'SELECT material, ' + language + ' FROM materials'
        c.execute(sql)
        rows = c.fetchall()

        materials = {}
        i = 0
        for key in rows:            
            materials[i] = {'material': rows[i][0], language : rows[i][1] }
            i += 1
        return materials

    def product_types(self, language : str) -> dict:
        sql = 'SELECT product_type, ' + language + ' FROM product_types'
        c.execute(sql)
        rows = c.fetchall()

        product_types = {}
        i = 0
        for key in rows:            
            product_types[i] = {'product_type': rows[i][0], language : rows[i][1] }
            i += 1
        return product_types

    # def colors(self):
    #     sql = 'SELECT color, dk_singular, dk_plural, dk_neutrum FROM colors'
    #     c.execute(sql)
    #     rows = c.fetchall()

    #     colors = {}
    #     for idx, col in enumerate(rows):
    #         colors[col[0]] = rows[idx]

    #     return colors
        
    def addjectives(self, language : str) -> list:
        sql = 'SELECT ' + language + '_addjective FROM addjectives'
        c.execute(sql)
        rows = c.fetchall()

        addjectives = []
        i = 0
        for key in rows:            
            addjectives.append(rows[i][0])
            i += 1        
        return addjectives
    
    def sizes(self, language : str) -> dict:
        sql = 'SELECT size, ' + language + ' FROM sizes'
        c.execute(sql)
        rows = c.fetchall()

        sizes = {}
        i = 0        
        for key in rows:            
            sizes[i] = {'size': rows[i][0], language : rows[i][1] }
            i += 1
        return sizes                

class SelectWatchBand(Select):

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
        sql = 'SELECT material_text, dk FROM watch_band_material_texts'
        c.execute(sql)
        rows = c.fetchall()

        material_texts = {}
        i = 0
        for key in rows:            
            material_texts[i] = {'material_text': rows[i][0], 'dk' : rows[i][1] }
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
    
class SelectScreenProtector(Select):    
    def intro_text(self) -> list:
      sql = 'SELECT dk FROM screen_protecter_intro_texts'
      c.execute(sql)
      rows = c.fetchall()

      intros = []
      i = 0
      for key in rows:            
          intros.append(rows[i][0])
          i += 1        
      return intros

class SelectCover(Select):
    def intro_text(self, language : str) -> list:
      sql = 'SELECT ' + language + ' FROM cover_intro_texts'
      c.execute(sql)
      rows = c.fetchall()

      intros = []
      i = 0
      for key in rows:            
          intros.append(rows[i][0])
          i += 1        
      return intros

    def material_texts(self, language : str) -> dict:
        sql = 'SELECT material_text,' + language + ' FROM cover_material_texts'
        c.execute(sql)
        rows = c.fetchall()

        material_texts = {}
        i = 0
        for key in rows:            
            material_texts[i] = {'material_text': rows[i][0], language : rows[i][1] }
            i += 1
        return material_texts    

class SelectCollection(Select):
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

    def collection_grandparent_description(self) -> list[dict]:
        sql = "SELECT h2, content FROM collection_grandparent_bottom_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions : list[dict] = []

        for row in rows:
            descriptions.append({ 'h2' : row[0], 'content' : row[1] })
        
        return descriptions

    def collection_child_description(self) -> list[dict]:
        sql = "SELECT h2, content FROM collection_child_bottom_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions : list[dict] = []

        for row in rows:
            descriptions.append({ 'h2' : row[0], 'content' : row[1] })
        
        return descriptions

    def collection_keyword_research(self) -> list[dict]:
        sql = "SELECT device, keyword, volume FROM collection_kw_research"
        c.execute(sql)
        rows = c.fetchall()
        
        kws : list[dict] = []        

        for row in rows:
            kws.append({'device' : row[0].lower().strip(), 'keyword' : row[1].strip(), 'volume': row[2] })

        return kws
    
    def collection_ads_keyword(self) -> list:        
        sql = "SELECT keyword FROM collection_ads_kw"
        c.execute(sql)
        rows = c.fetchall()
        ads_kw : list = []

        for row in rows:            
            ads_kw.append(row[0])

        return ads_kw