import requests
import json




class MsfModule:
    def __init__(self):
        pass

    def find(self, keyword = "", version=""):
        try:
            datamod = []
            keyword = f"{keyword.lower()} {version.lower()}"
            o = open("files/msf_module.json", "r").read()
            modules = json.loads(o)
            result = [data for data in modules if keyword in data['title']]
            return result
        except:
            return False
            pass