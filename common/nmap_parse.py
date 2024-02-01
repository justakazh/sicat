import xmltodict
import json

class NmapParse:
    def __init__(self):
        pass
    


    def parse(self, file):
        output = []
        o = open(file, "r").read()
        d = json.loads(json.dumps(xmltodict.parse(o)))
        try:
            for port in d['nmaprun']['host']['ports']['port']:
                output.append({
                    "service" : port['service']['@product'],
                    "version" : port['service']['@version']
                })
            return output
        except Exception as e:
            return False
        