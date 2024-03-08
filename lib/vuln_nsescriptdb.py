from common.nse_script_db import NSEScriptDB

class NSEScriptDBSearcher:
    def __init__(self, filepath):
        self.db = NSEScriptDB(filepath)
        

    def find(self, keyword="", version=""):
        keyword = f"{keyword}{version}"
        return self.db.search_script(keyword)