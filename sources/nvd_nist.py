################################################################
# Source   : https://nvd.nist.gov/
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

class NVDNIST:

    def __init__(self):
        ### Result data will be saved here ##
        self.result = []
        self.keyword = None
    
    def WrapperStart(self, silent=False):
        if not silent:
            print("-" * 75)
            print(f"{ConsoleColors.BLUE}[+] Searching in NVD NIST{ConsoleColors.ENDC}")
            print("-" * 75)

    def Output(self, data, limit, silent=False):
        for item in data:
            if limit is not None and len(self.result) >= limit:
                break
            
            cve_item = item.get('cve', {})
            title = cve_item.get('id', 'Unknown ID')
            descriptions = "No description"
            if cve_item.get('descriptions'):
                 descriptions = cve_item['descriptions'][0].get('value', "No description")
            
            source_name = "NVD NIST"
            source_link = f"https://nvd.nist.gov/vuln/detail/{title}"
            searchBy = "all"
            
            wrap = {
                "title": title,
                "description": descriptions,
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
                print_attribute("Description", html.unescape(descriptions), self.keyword)
                print()

    def search(self, keyword=None, limit=None, silent=False):
        self.keyword = keyword
        try:
            ###################### Search Logic ######################
            # Logic to scrape data from source
            # Includes pagination handling and limits
            # Search based on title and query
            ##########################################################
            
            self.WrapperStart(silent)
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            
            start = 0
            while True:
                if limit is not None and len(self.result) >= limit:
                    break
                
                # print(f"\r{ConsoleColors.BLUE}[+] Fetching page: {int(start/15) + 1}{ConsoleColors.ENDC}", end="", flush=True)
                
                # Note: NVD API 2.0 recommends using an API key for better rates. 
                # Without a key, rate limits are strict.
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=15&startIndex={start}"
                
                try:
                    resp = requests.get(url, headers=headers)
                    if resp.status_code == 200:
                        vulnerabilities = resp.json().get('vulnerabilities', [])
                        if not vulnerabilities:
                            break
                        
                        self.Output(vulnerabilities, limit, silent)
                        
                        if len(vulnerabilities) < 15:
                            break
                    else:
                        if not silent:
                            print(f"\n{ConsoleColors.FAIL}[-] Error in NVD NIST source [search]: {resp.status_code}{ConsoleColors.ENDC}")
                        break
                except Exception as e:
                    if not silent:
                        print(f"\n{ConsoleColors.FAIL}[-] Exception in NVD NIST request: {str(e)}{ConsoleColors.ENDC}")
                    break
                
                start += 15

            self.wrapperEnd(silent)

        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in NVD NIST source [search]: {str(e)}{ConsoleColors.ENDC}")
    
    def wrapperEnd(self, silent=False):
        if silent:
            return
        try:
            if len(self.result) == 0:
                print(f"{ConsoleColors.FAIL}[-] No results found in NVD NIST.{ConsoleColors.ENDC}")
            else:
                print(f"{ConsoleColors.BOLD}[*] Total Result : {len(self.result)} CVEs found!{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in NVD NIST source [wrapperEnd]: {str(e)}{ConsoleColors.ENDC}")