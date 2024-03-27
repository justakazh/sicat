import sqlite3

class NSEScriptDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS nse_script (
                                script_name TEXT PRIMARY KEY,
                                script_type TEXT,
                                category1 TEXT,
                                category2 TEXT,
                                category3 TEXT,
                                category4 TEXT,
                                category5 TEXT,
                                description TEXT,
                                link TEXT)''')
        self.conn.commit()

    def upsert_script(self, script_name, script_data):
        self.cursor.execute('SELECT * FROM nse_script WHERE script_name = ?', (script_name,))
        existing_record = self.cursor.fetchone()

        if existing_record:
            self.cursor.execute('''UPDATE nse_script
                                   SET script_type = ?,
                                       description = ?,
                                       link = ?
                                   WHERE script_name = ?''',
                                (script_data['script_type'],
                                 script_data['description'],
                                 script_data['link'],
                                 script_name))
        else:
            self.cursor.execute('''INSERT INTO nse_script
                                   (script_name, script_type, description, link)
                                   VALUES (?, ?, ?, ?)''',
                                (script_name,
                                 script_data['script_type'],
                                 script_data['description'],
                                 script_data['link']))

        categories = script_data.get('categories', [])
        for i in range(5):
            if i < len(categories):
                self.cursor.execute('''UPDATE nse_script
                                       SET category{} = ?
                                       WHERE script_name = ?'''.format(i + 1),
                                    (categories[i], script_name))
            else:
                self.cursor.execute('''UPDATE nse_script
                                       SET category{} = '-'
                                       WHERE script_name = ?'''.format(i + 1),
                                    (script_name,))

        self.conn.commit()

    def search_script(self, keyword):
        try:
            
            self.cursor.execute("SELECT * FROM nse_script WHERE script_name LIKE ?", ('%' + keyword + '%',))
            rows = self.cursor.fetchall()

            if rows:
                return rows
            else:
                return False
            
        except sqlite3.Error as e:
            print("SQLite error:", e)
        
        finally:
            self.conn.commit()


    def close(self):
        self.conn.close()

