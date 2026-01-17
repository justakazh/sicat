################################################################
# Source   : https://github.com/topscoder/nuclei-wordfence-cve
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

class WordfenceCVE:

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
            print(f"{ConsoleColors.BLUE}[+] Searching in Wordfence CVE Templates{ConsoleColors.ENDC}")
            print("-" * 75)

    def Output(self, data, limit, silent=False):
        for item in data:
            if limit is not None and len(self.result) >= limit:
                break
            
            name = item.get('name', 'Unknown')
            path = item.get('path', 'Unknown')
            source_link = item.get('html_url', '')
            
            wrap = {
                "name" : name,
                "path" : path,
                "source_name": "Wordfence CVE Templates",
                "source_link": source_link,
                "command" : f"nuclei -t ~/nuclei-wordfence-cve/{path} -u [TARGET]",
                "searchBy": "code",
                "keyword": self.keyword
            }
            
            self.result.append(wrap)

            # Print to console
            if not silent:
                print_attribute("Template", html.unescape(path), self.keyword)
                print_attribute("Link", source_link, self.keyword, no_wrap=True)
                print_attribute("Command", wrap.get('command', 'Unknown'), self.keyword, no_wrap=True)
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
                    print(f"\n{ConsoleColors.FAIL}[!] GitHub Token (gh_token) not found in ~/.sicat/config.json{ConsoleColors.ENDC}")
                    print(f"{ConsoleColors.WARNING}[!] Please add your GitHub token to the config file to enable Wordfence CVE Templates search.{ConsoleColors.ENDC}")
                    print(f"{ConsoleColors.WARNING}[!] Format: {{ \"gh_token\": \"YOUR_TOKEN\" }}{ConsoleColors.ENDC}\n")
                 # We don't return here, might still try or fail gracefully below, but original returned
                 return

            self.WrapperStart(silent)

            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.api_key}"
            }
            url = "https://api.github.com/search/code"
            
            # --- Search in topscoder/nuclei-wordfence-cve ---
            page = 1
            while True:
                if limit is not None and len(self.result) >= limit:
                    break

                # print(f"\r{ConsoleColors.BLUE}[+] Fetching page: {int(page/100) + 1}{ConsoleColors.ENDC}", end="", flush=True)
                params = {
                    "q": f"{keyword} repo:topscoder/nuclei-wordfence-cve",
                    "page": page,
                    "per_page": 100
                }
                
                try:
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        items = response.json().get('items', [])
                        if not items:
                            break
                        
                        self.Output(items, limit, silent)
                        
                        page += 1
                        if page > 10: 
                             # print(f"\n{ConsoleColors.WARNING}[!] Limit reached (10 pages). Stopping.{ConsoleColors.ENDC}")
                             break
                    else:
                        if not silent:
                            print(f"\n{ConsoleColors.FAIL}[-] GitHub API Error: {response.status_code}{ConsoleColors.ENDC}")
                        break
                except Exception:
                    break

            self.wrapperEnd(silent)
            
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in Wordfence Templates source [search]: {str(e)}{ConsoleColors.ENDC}")
    
    def wrapperEnd(self, silent=False):
        if silent:
            return
        try:
            if len(self.result) == 0:
                print(f"{ConsoleColors.FAIL}[-] No Templates Found!{ConsoleColors.ENDC}")
            else:
                print(f"{ConsoleColors.BOLD}[*] Total Result : {len(self.result)} Templates found!{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in Wordfence Templates source [wrapperEnd]: {str(e)}{ConsoleColors.ENDC}")
