################################################################
# Source   : https://github.com/rapid7/metasploit-framework
# Coded By : justakazh
# Github   : https://github.com/justakazh/
#
# Contribute by creating your own source following the guide:
# https://github.com/justakazh/sicat/CONTRIBUTE.md 
################################################################


import requests
import html
import os
import json
from lib.utils import highlight_keyword, ConsoleColors, print_attribute

class MetasploitFramework:

    def __init__(self):

        ## Authentication
        config_path = os.path.expanduser("~/.sicat/config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                self.api_key = config.get('gh_token')
        except FileNotFoundError:
             self.api_key = None

        ### Result data will be saved here ##
        self.result = []
        self.keyword = None
    
    def WrapperStart(self, silent=False):
        if not silent:
            print("-" * 75)
            print(f"{ConsoleColors.BLUE}[+] Searching in Metasploit Framework{ConsoleColors.ENDC}")
            print("-" * 75)

    def Output(self, data, limit, silent=False):
        for item in data:
            if limit is not None and len(self.result) >= limit:
                break
            
            name = item.get('name', 'Unknown')
            path = item.get('path', 'Unknown')
            source_link = item.get('html_url', '')
            #if start with modules/ then add msfconsole command
            command = f"msfconsole -x \"use {path}\"" if path.startswith("modules/") else f"cat /usr/share/metasploit-framework/{path}"
            
            wrap = {
                "name" : name,
                "path" : path,
                "source_name": "Metasploit Framework",
                "source_link": source_link,
                "searchBy": "code",
                "command": command,
                "keyword": self.keyword
            }
            
            self.result.append(wrap)

            # Print to console
            if not silent:
                print_attribute("Name", html.unescape(name), self.keyword)
                print_attribute("Path", html.unescape(path), self.keyword)
                print_attribute("Link", source_link, self.keyword)
                if wrap['command']:
                    print_attribute("Command", wrap.get("command"), self.keyword, no_wrap=True)
                print()


    def search(self, keyword=None, limit=None, silent=False):
        self.keyword = keyword
        try:

            ###################### Search Logic ######################
            # Logic to scrape data from source
            # Includes pagination handling and limits
            # Search based on title and query
            ##########################################################
            
            if not self.api_key:
                 if not silent:
                    print(f"{ConsoleColors.WARNING}[-] GitHub Token not found in ~/.sicat/config.json. Metasploit search (via GitHub API) may fail.{ConsoleColors.ENDC}")
                 return

            self.WrapperStart(silent)

            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.api_key}"
            }
            url = "https://api.github.com/search/code"
            page = 1

            while True:
                if limit is not None and len(self.result) >= limit:
                    break
                
                params = {
                    "q": f"{keyword} repo:rapid7/metasploit-framework",
                    "page": page,
                    "per_page": 100
                }
                
                try:
                    # Note: GitHub Search API rate limits are strict. 
                    # This simplistic loop might hit limits or get empty pages if > ~1000 results.
                    response = requests.get(url, headers=headers, params=params)

                    if response.status_code == 200:
                        items = response.json().get('items', [])
                        if not items:
                            break
                        
                        self.Output(items, limit, silent)
                        
                        page += 1
                    else:
                        if not silent:
                            print(f"\n{ConsoleColors.FAIL}[-] GitHub API Error: {response.status_code}{ConsoleColors.ENDC}")
                        break
                except Exception:
                    break

            self.wrapperEnd(silent)
            
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in Metasploit Framework source [search]: {str(e)}{ConsoleColors.ENDC}")
    
    def wrapperEnd(self, silent=False):
        if silent:
            return
        try:
            if len(self.result) == 0:
                print(f"{ConsoleColors.FAIL}[-] No Modules Found in Metasploit Framework!{ConsoleColors.ENDC}")
            else:
                print(f"{ConsoleColors.BOLD}[*] Total Result : {len(self.result)} Modules found!{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in Metasploit Framework source [wrapperEnd]: {str(e)}{ConsoleColors.ENDC}")