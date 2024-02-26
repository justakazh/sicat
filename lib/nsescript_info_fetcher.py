import requests
from bs4 import BeautifulSoup
from common.nse_script_db import NSEScriptDB
from tqdm import tqdm

class ScriptInfoFetcher:
    def __init__(self, scripts_url="https://svn.nmap.org/nmap/scripts/", 
                 info_url="https://nmap.org/nsedoc/scripts/", 
                 db_file='files/exploit.db'):
        self.scripts_url = scripts_url
        self.info_url = info_url
        self.db = NSEScriptDB(db_file)

    def fetch_script_info(self):
        response = requests.get(self.scripts_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            script_links = soup.find_all('a', href=True)
            script_names = [link.text.strip() for link in script_links if link['href'].endswith('.nse')]

            for script_name in tqdm(script_names, desc="Fetching Script Info"):  # tqdmを使用してプログレスバーを表示
                script_info = {}
                response = requests.get(self.info_url + script_name.lower().replace(".nse", "") + ".html")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    script_name = script_name.lower().replace(".nse", "")

                    # Script type
                    script_type_section = soup.find('p')
                    if script_type_section:
                        script_types_text = script_type_section.get_text(strip=True)
                        script_types = script_types_text.split('Categories:')[0].strip().replace('Script types:\n', '')
                        script_info['script_type'] = script_types

                    # Categories
                    categories = script_types_text.split('Categories:')[1].split('Download:')[0].strip().split(',')
                    script_info['categories'] = [category.strip() for category in categories]

                    # Download link
                    download_link = script_types_text.split('Download:')[1].strip()
                    script_info['link'] = download_link
                    
                    # Description
                    description = soup.find('h2').find_next_sibling('p').text.strip()
                    script_info['description'] = description

                    self.db.upsert_script(script_name, script_info)

                else:
                    print("Failed to fetch description and category for", script_name, ". Status code:", response.status_code)

            self.db.close()

        else:
            print("Failed to fetch script names. Status code:", response.status_code)
            return None
