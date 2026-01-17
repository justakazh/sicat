
import os
import sys
from flask import Flask, render_template, request, make_response

# Add parent directory to path to allow importing sources when running this file directly or from sicat.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources import *
from lib.report_generator import ReportGenerator

# Use absolute path for templates to ensure they load correctly from any CWD
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    keyword = request.form.get('keyword')
    selected_modules = request.form.getlist('modules')
    
    if not keyword:
        return "Keyword is required", 400

    all_results = []
    
    # Run scans based on selection
    limit_val = request.form.get('limit', 50)
    try:
        limit = int(limit_val)
    except ValueError:
        limit = 50 

    if 'exploit_db' in selected_modules:
        try:
            scanner = Exploitdb()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in ExploitDB: {e}")

    if 'nvd_nist' in selected_modules:
        try:
            scanner = NVDNIST()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in NVD NIST: {e}")

    if 'cve_org' in selected_modules:
        try:
            scanner = CVEORG()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in CVE.org: {e}")

    if 'nuclei_templates' in selected_modules:
        try:
            scanner = NucleiTemplates()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in Nuclei: {e}")

    if 'github' in selected_modules:
        try:
            scanner = Github()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in Github: {e}")

    if 'metasploit_framework' in selected_modules:
        try:
            scanner = MetasploitFramework()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in Metasploit: {e}")

    if 'nse_script' in selected_modules:
        try:
            scanner = NSEScript()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in NSE: {e}")

    if 'wordfence_cve' in selected_modules:
        try:
            scanner = WordfenceCVE()
            scanner.search(keyword, limit, silent=True)
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in Wordfence CVE: {e}")

    # Generate Report HTML
    rg = ReportGenerator(all_results, [keyword])
    html_content = rg.generate_html()
    
    return html_content

def start_server(host='0.0.0.0', port=5000):
    print(f"[*] Starting SiCat Web Server on http://{host}:{port}")
    app.run(host=host, port=port)

if __name__ == '__main__':
    start_server()
