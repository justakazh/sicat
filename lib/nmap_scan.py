import subprocess
import shutil
from xml.etree import ElementTree as ET


class Nmap:
    def __init__(self):
        self.port_services = []

    def requirements(self):
        # Check if nmap is installed/available in PATH
        if shutil.which("nmap") is None:
             raise Exception("[-] Nmap is not installed or not in PATH. Please install Nmap to use this feature.")

    def scan(self, target):
        self.requirements()
        try:
            print(f"[*] Scanning {target} with Nmap...")
            # Use subprocess.run with list args to avoid shell injection
            # Added -Pn to skip host discovery (treat as online), important for localhost/firewalled targets
            command = ["nmap", "-sV", "-Pn", "--min-rate", "1000", target, "-oX", "-"]
            
            process = subprocess.run(command, capture_output=True, text=True, check=True)
            result = process.stdout
            
            if not result.strip():
                print("[-] Empty output from Nmap.")
                return

            root = ET.fromstring(result)
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
                print("[-] No open ports found.")

        except subprocess.CalledProcessError as e:
            raise Exception(f"[-] Nmap scan failed: {e.stderr}")
        except ET.ParseError as e:
            raise Exception(f"[-] Failed to parse Nmap XML output: {e}")
        except Exception as e:
            raise Exception(f"[-] An error occurred during Nmap scan: {e}")

