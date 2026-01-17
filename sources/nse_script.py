################################################################
# Source   : /usr/share/nmap/scripts
# Coded By : justakazh
# Guide    : https://nmap.org/book/nse-usage.html
#
# Contribute by creating your own source following the guide:
# https://github.com/justakazh/sicat/CONTRIBUTE.md 
################################################################


import os
import json
from lib.utils import highlight_keyword, ConsoleColors, print_attribute

class NSEScript:

    def __init__(self):
        ### Result data will be saved here ##
        self.result = []
        self.keyword = None
        self.nmap_script_path = "/usr/share/nmap/scripts"

    
    def WrapperStart(self, silent=False):
        if not silent:
            print("-" * 75)
            print(f"{ConsoleColors.BLUE}[+] Searching in Nmap NSE Scripts{ConsoleColors.ENDC}")
            print("-" * 75)

    def Output(self, data, limit, silent=False):
        # data is expected to be a list of items, even if just one
        for item in data:
            if limit is not None and len(self.result) >= limit:
                break
            
            name = item.get('name', 'Unknown')
            path = item.get('source_link', '')
            description = item.get('description', 'No description')
            categories = item.get('categories', 'Unknown')
            
            wrap = {
                "name": name,
                "source_link": path,
                "description": description,
                "categories": categories,
                "source_name": "Nmap NSE",
                "command" : f"nmap --script={name} [TARGET] [ARGS]",
                "keyword": self.keyword
            }
            
            self.result.append(wrap)

            # Print to console
            if not silent:
                print_attribute("Name", name, self.keyword)
                print_attribute("Path", path, self.keyword, no_wrap=True)
                print_attribute("Description", description, self.keyword)
                print_attribute("Categories", categories, self.keyword)
                print_attribute("Command", wrap.get('command', 'Unknown'), self.keyword, no_wrap=True)
                print()

    def search(self, keyword=None, limit=None, silent=False):
        self.keyword = keyword
        try:

            ###################### Search Logic ######################
            # Search for .nse files in /usr/share/nmap/scripts
            # Based on keyword (filename & content)
            ##########################################################
            
            self.WrapperStart(silent)

            if not os.path.exists(self.nmap_script_path):
                if not silent:
                    print(f"{ConsoleColors.WARNING}[!] Error : Directory not found: {self.nmap_script_path}. Please ensure Nmap is installed.{ConsoleColors.ENDC}")
                return

            for root, dirs, files in os.walk(self.nmap_script_path):
                if limit is not None and len(self.result) >= limit:
                    break
                    
                for file in files:
                    if limit is not None and len(self.result) >= limit:
                        break

                    if file.endswith(".nse"):
                        file_path = os.path.join(root, file)
                        match_found = False
                        
                        # Check filename
                        if keyword and keyword.lower() in file.lower():
                            match_found = True
                        
                        # Check content
                        if not match_found and keyword:
                            try:
                                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                    content = f.read()
                                    if keyword.lower() in content.lower():
                                        match_found = True
                            except Exception:
                                pass
                        
                        if match_found:
                            # Extract basic metadata from script content
                            description = "No description"
                            categories = "Unknown"
                            
                            try:
                                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                    lines = f.readlines()
                                    for i, line in enumerate(lines):
                                        if "description = [[" in line:
                                            # Simple heuristic to get next line as description
                                            if i + 1 < len(lines):
                                                description = lines[i+1].strip()
                                                description = description.replace(']]', '')
                                                break
                                        if "description =" in line and "[[" not in line:
                                             description = line.split("=")[1].strip().replace('"', '').replace("'", "")

                                    # Reset to find categories
                                    for line in lines:
                                        if "categories = {" in line:
                                            categories = line.split("{")[1].split("}")[0].replace('"', '').replace("'", "")
                            except:
                                pass

                            item = {
                                "name": file,
                                "source_link": file_path,
                                "description": description,
                                "categories": categories
                            }
                            self.Output([item], limit, silent)
            
            self.wrapperEnd(silent)

        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in NSEScript source [search]: {str(e)}{ConsoleColors.ENDC}")
    
    def wrapperEnd(self, silent=False):
        if silent:
            return
        try:
            if len(self.result) == 0:
                print(f"{ConsoleColors.FAIL}[-] No Scripts Found in Nmap Directory!{ConsoleColors.ENDC}")
            else:
                print(f"{ConsoleColors.BOLD}[*] Total Result : {len(self.result)} Scripts found!{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in NSEScript source [wrapperEnd]: {str(e)}{ConsoleColors.ENDC}")