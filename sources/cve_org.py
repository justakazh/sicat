################################################################
# Source   : https://www.cve.org/
# Coded By : justakazh
# Github   : https://github.com/justakazh/
#
# Contribute by creating your own source following the guide:
# https://github.com/justakazh/sicat/CONTRIBUTE.md 
################################################################

import requests
import html
from lib.utils import highlight_keyword, ConsoleColors, print_attribute

class CVEORG:

    def __init__(self):
        ### Result data will be saved here ##
        self.result = []
        self.keyword = None
    
    def WrapperStart(self, silent=False):
        if not silent:
            print("-" * 75)
            print(f"{ConsoleColors.BLUE}[+] Searching in CVE.org{ConsoleColors.ENDC}")
            print("-" * 75)
    
        
    
    def Output(self, data, limit, silent=False):
        for item in data:
            if limit is not None and len(self.result) >= limit:
                break
            
            title = item.get('_id', 'Unknown')
            # Safely access nested dictionary keys
            containers = item.get('_source', {}).get('containers', {})
            cna = containers.get('cna', {})
            descriptions_list = cna.get('descriptions', [])
            description = descriptions_list[0].get('value', "No description available") if descriptions_list else "No description available"
            
            source_name = "CVE.ORG"
            source_link = f"https://www.cve.org/CVERecord?id={title}"
            searchBy = "all"
            
            wrap = {
                "title": title,
                "description": description,
                "source_name": source_name,
                "source_link": source_link,
                "searchBy": searchBy,
                "keyword": self.keyword
            }
            
            self.result.append(wrap)

            # Print to console
            if not silent:
                print_attribute("Title", html.unescape(title), self.keyword)
                print_attribute("Link", source_link, self.keyword, no_wrap=True)
                print_attribute("Description", html.unescape(description), self.keyword)
                print()

    def search(self, keyword=None, limit=None, silent=False):
        self.keyword = keyword # Save keyword
        try:
            ###################### Search Logic ######################
            # Logic to scrape data from source
            # Includes pagination handling and limits
            # Search based on title and query
            ##########################################################

            self.WrapperStart(silent)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Content-Type": "application/json"
            }
            
            start = 0
            while True:
                if limit is not None and len(self.result) >= limit:
                    break

                payload = {
                    "query": keyword,
                    "from": start,
                    "size": 25,
                    "sort": {"property": "cveId", "order": "desc"}
                }
                
                try:
                    resp = requests.post("https://www.cve.org/restapiv1/search", json=payload, headers=headers)
                    
                    if resp.status_code == 200:
                        resp_data = resp.json().get('data', [])
                        if not resp_data:
                            break
                        
                        self.Output(resp_data, limit, silent)
                        
                        if len(resp_data) < 25:
                            break
                    else:
                        if not silent:
                            print(f"\n{ConsoleColors.FAIL}[-] Error fetching from CVE.org: {resp.status_code}{ConsoleColors.ENDC}")
                        break
                except Exception as e:
                    if not silent:
                        print(f"\n{ConsoleColors.FAIL}[-] Exception in CVE.org request: {str(e)}{ConsoleColors.ENDC}")
                    break
                    
                start += 25
            
            self.wrapperEnd(silent)

        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in CVE.org source [search]: {str(e)}{ConsoleColors.ENDC}")
    
    def wrapperEnd(self, silent=False):
        if silent:
            return
        try:
            if len(self.result) == 0:
                print(f"{ConsoleColors.FAIL}[-] No CVEs Found in CVE.org!{ConsoleColors.ENDC}")
            else:
                print(f"{ConsoleColors.BOLD}[*] Total Result : {len(self.result)} CVEs found!{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in CVE.org source [wrapperEnd]: {str(e)}{ConsoleColors.ENDC}")