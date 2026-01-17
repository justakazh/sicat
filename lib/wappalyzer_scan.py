import webtech


class WebTech:

    def __init__(self):
        self.webtech = [] 

    def scan(self, target):
        try:
            report = webtech.WebTech(options={'json': True}).start_from_url(target)
            for tech in report['tech']:
                name = tech['name']
                version = tech['version'] if tech['version'] else ""
                entry = f"{name} {version}".strip()
                if entry not in self.webtech:
                    self.webtech.append(entry)
        except webtech.utils.ConnectionException:
            print("Connection error")
        
