import xmltodict
import json

class NmapParse:
    def __init__(self):
        pass
    


    def parse(self, file):
        output = []
        o = open(file, "r").read()
        d = json.loads(json.dumps(xmltodict.parse(o)))
        # print(d['nmaprun']['host']['ports']['port'])
        for port in d['nmaprun']['host']['ports']['port']:
            try:
                if 'service' in port:
                    if '@product' in port['service']:
                        if '@version' in port['service']:
                            output.append({
                                "service" : port['service']['@product'],
                                "version" : port['service']['@version']
                            })
                        else:
                            output.append({
                                "service" : port['service']['@product'],
                                "version" : ""
                            })
            except Exception as e:
                return False
        
        return output
        