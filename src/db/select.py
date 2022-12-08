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
        
    # def addjectives(self, language : str) -> list:
    #     sql = 'SELECT ' + language + '_addjective FROM addjectives'
    #     c.execute(sql)
    #     rows = c.fetchall()

    #     addjectives = []
    #     i = 0
    #     for key in rows:            
    #         addjectives.append(rows[i][0])
    #         i += 1        
    #     return addjectives
    
    def addjectives(self, language : str) -> dict:
        sql = 'SELECT product_type, material, ' + language + '_addjective FROM addjectives'
        c.execute(sql)
        rows = c.fetchall()
        # addjectives = [{
        #     'cover' : {
        #         'silicone / tpu' : ['1', '3']
        #     }
        # }]        
        #
        
        # Setting product type keys
        product_type_keys = []
        i = 0
        for value in rows:
            split_product_types = rows[i][0].split(',')

            for product_type in split_product_types:
                product_type_keys.append(product_type.lower().strip())

            product_type_keys = list(dict.fromkeys(product_type_keys))
            i += 1        
        #   
        addjectives = {}             
        # Setting materials as key
        for product_type_key in product_type_keys:            
            mat_keys = []
            # Rows is from DB
            for value in rows:
                value_split_types = value[0].split(',')
                value_material = value[1]
                
                for val_split_type in value_split_types:                    
                    val_split_type = val_split_type.lower().strip()
                    if product_type_key in val_split_type:
                        
                        # Append material:
                        mat_keys.append(value_material)
                        # Removing duplicates
                        mat_keys = list(dict.fromkeys(mat_keys))
                        # Setting material is dict keys
                        addjectives[product_type_key] = dict.fromkeys(mat_keys)                        

        # Setting addjectives
        for product_type_key in addjectives:
            for material in addjectives[product_type_key]:
                value_adj_list = []
                # Loop trough DB
                for value in rows:
                    value_split_types = value[0].split(',')
                    value_material = value[1].lower().strip()
                    value_adj = value[2].strip()                    
                    for val_split_type in value_split_types: 
                        val_split_type = val_split_type.lower().strip()                    
                        if product_type_key in val_split_type and material == value_material:
                            # Setting values
                            value_adj_list.append(value_adj)
                            addjectives[val_split_type][material] = value_adj_list
                            
        
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
      sql = 'SELECT intro FROM watch_band_intro_texts'
      c.execute(sql)
      rows = c.fetchall()

      intros = []
      i = 0
      for key in rows:            
          intros.append(rows[i][0])
          i += 1        
      return intros

    def watchband_material_texts(self) -> dict:
        sql = 'SELECT material, text FROM watch_band_material_texts'
        c.execute(sql)
        rows = c.fetchall()

        material_texts = {}
        i = 0
        for key in rows:            
            material_texts[i] = {'material': rows[i][0], 'text' : rows[i][1] }
            i += 1
        return material_texts

    def watchband_ending_texts(self) -> list:
        sql = 'SELECT ending FROM watch_band_ending_texts'
        c.execute(sql)
        rows = c.fetchall()

        endings = []
        i = 0
        for key in rows:            
            endings.append(rows[i][0])
            i += 1        
        return endings
    
class SelectScreenProtector(Select):    
    def intro_text(self) -> list:
      sql = 'SELECT intro FROM screen_protecter_intro_texts'
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
      sql = 'SELECT intro FROM cover_intro_texts'
      c.execute(sql)
      rows = c.fetchall()

      intros = []
      i = 0
      for key in rows:            
          intros.append(rows[i][0])
          i += 1        
      return intros

    def material_texts(self, language : str) -> dict:
        sql = 'SELECT material, text FROM cover_material_texts'
        c.execute(sql)
        rows = c.fetchall()

        material_texts = {}
        i = 0
        for key in rows:            
            material_texts[i] = {'material_text': rows[i][0], 'text' : rows[i][1] }
            i += 1
        return material_texts    
    
    def ending_texts(self, language : str) -> list:
        sql = 'SELECT ending FROM cover_ending_texts'
        c.execute(sql)
        rows = c.fetchall()

        endings = []
        i = 0
        for key in rows:            
            endings.append(rows[i][0])
            i += 1        
        return endings

class SelectCollection(Select):
    # Collections
    def collections(self) -> list[dict]:
      sql = 'SELECT name, belongs_to, relationship_type, alternative_names FROM collections'
      c.execute(sql)
      rows = c.fetchall()
      collections = []
      
      for i, key in enumerate(rows):        
        alt_names = []
        if rows[i][3]:
            alt_names = rows[i][3].split(', ')
            # print(alt_names)
        collections.append({'name' : rows[i][0], 'belongs_to': rows[i][1], 'relationship_type' : rows[i][2], 'alternative_names' : alt_names })
      
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

    def grandparent_description(self) -> list[dict]:
        sql = "SELECT description FROM collection_grandparent_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions = []

        for key, value in enumerate(rows):
            descriptions.append(value[0])
        
        return descriptions

    def grandparent_bottom_description(self) -> list[dict]:
        sql = "SELECT h2, content FROM collection_grandparent_bottom_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions : list[dict] = []

        for row in rows:
            descriptions.append({ 'h2' : row[0], 'content' : row[1] })
        
        return descriptions
    
    def parent_description(self) -> list[str]:
        sql = "SELECT description FROM collection_parent_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions = []

        for key, value in enumerate(rows):
            descriptions.append(value[0])
        
        return descriptions

    def child_description(self) -> list[str]:
        sql = "SELECT description FROM collection_child_description"
        c.execute(sql)
        rows = c.fetchall()
        descriptions = []

        for key, value in enumerate(rows):
            descriptions.append(value[0])
        
        return descriptions
    
    def child_bottom_description(self) -> list[dict]:
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