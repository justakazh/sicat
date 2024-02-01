import requests



class PacketStormSecurity:
    def __init__(self):
        pass
    


    def find(self, keyword="", version=""):
        keyword = f"{keyword} {version}"
        resp = requests.get(f"https://packetstormsecurity.com/search/?q={keyword}")
        if resp.status_code == 200:
            return resp.text
        else:
            return False