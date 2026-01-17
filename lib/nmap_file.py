from xml.etree import ElementTree as ET
import os

class NmapParse:
    def __init__(self):
        self.port_services = []

    def parse(self, file_path):
        try:
            if not os.path.exists(file_path):
                 print(f"[-] File not found: {file_path}")
                 return

            print(f"[*] Parsing Nmap XML file: {file_path}")
            
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
            except ET.ParseError as e:
                print(f"[-] Failed to parse Nmap XML file: {e}")
                return

            found_services = False
            for host in root.iter("host"):
                for port in host.iter("port"):
                    state_el = port.find("state")
                    if state_el is None or state_el.get("state") != "open":
                        continue
                    
                    found_services = True
                    port_id = port.get('portid')
                    service_el = port.find("service")
                    
                    service_name = "unknown"
                    service_version = ""
                    service_product = ""
                    
                    if service_el is not None:
                        service_name = service_el.get("name", "unknown")
                        service_version = service_el.get("version", "")
                        service_product = service_el.get("product", "")

                    # Construct a useful search string
                    # Preference: Product + Version, fallback to Name
                    info = []
                    if service_product:
                        info.append(service_product)
                    elif service_name:
                        info.append(service_name)
                        
                    if service_version:
                        info.append(service_version)
                        
                    service_info = " ".join(info)
                    
                    entri_port_service = f"{port_id}/tcp|{service_product if service_product else service_name}|{service_version}".strip()

                    if entri_port_service not in self.port_services:
                        self.port_services.append(entri_port_service)
                        print(f"[+] Found Port Service: {entri_port_service}")
            
            if not found_services:
                print("[-] No open ports found in file.")

        except Exception as e:
            print(f"[-] An error occurred during Nmap file parsing: {e}")
