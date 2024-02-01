import requests



class NvdDB:
    def __init__(self):
        pass
    

    def find(self, keyword = "", version = ""):
        keyword = f"{keyword} {version}"
        keyword = keyword.replace(" ", "%20")
        resp = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return False