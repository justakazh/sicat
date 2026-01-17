#!/usr/bin/env python3
import argparse
import json
import os
import sys

# Add script directory to Python path to allow execution from any location
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sources import *
from lib.utils import ConsoleColors
from lib import *
from lib.report_generator import ReportGenerator
from lib.web_server import start_server

def main():

    #check config file
    config_path = os.path.expanduser("~/.sicat/config.json")
    if not os.path.exists(config_path):
        print(f"{ConsoleColors.FAIL}[-] Config file not found.{ConsoleColors.ENDC}")
        print(f"{ConsoleColors.GREEN}[*] Creating config file.{ConsoleColors.ENDC}")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        open(config_path, "w").write("{}")

    parser = argparse.ArgumentParser(description="SiCat - Vulnerability & Exploit Finder")
    
    # General Arguments
    parser.add_argument("-u", "--update", action="store_true", help="Update all local databases and resources")
    parser.add_argument("-k", "--keyword", required=False, help="Specific keyword to search for (e.g. 'WordPress 5.8', 'CVE-2021-12345')")
    parser.add_argument("-nmap", "--nmap", required=False, help="Target IP for live Nmap scan. Discovered services will be added to search keywords.")
    parser.add_argument("-nmap-file", "--nmap-file", required=False, help="Path to Nmap XML file. Parsed services will be added to search keywords.")
    parser.add_argument("-web", "--web", required=False, help="Target URL for Wappalyzer scan. Detected technologies will be added to search keywords.")
    
    # Modules Arguments
    parser.add_argument("-edb", "--exploit-db", action="store_true", help="Enable search in Exploit-DB")
    parser.add_argument("-nvd", "--nvd-nist", action="store_true", help="Enable search in NVD NIST Database")
    parser.add_argument("-cve", "--cve-org", action="store_true", help="Enable search in CVE.org")
    parser.add_argument("-nuclei", "--nuclei-templates", action="store_true", help="Enable search in Nuclei Templates")
    parser.add_argument("-gh", "--github", action="store_true", help="Enable search in GitHub Repositories")
    parser.add_argument("-msf", "--metasploit-framework", action="store_true", help="Enable search in Metasploit Framework Modules")
    parser.add_argument("-nse", "--nse-script", action="store_true", help="Enable search in Nmap NSE Scripts")
    parser.add_argument("-wcve", "--wordfence-cve", action="store_true", help="Enable search in Wordfence CVE Templates")
    
    # Process Arguments
    parser.add_argument("-s", "--silent", action="store_true", help="Run in silent mode (suppress banner and non-essential output)")
    parser.add_argument("-l", "--limit", type=int, default=25, help="Limit the number of results per module (default: 25)")

    # Output Arguments
    parser.add_argument("-o", "--output", help="Path to save the console output")
    parser.add_argument("-ot", "--output-type", default="text", choices=["text", "json"], help="Format of the output file (text or json)")
    parser.add_argument("-r", "--report", nargs='?', const='default', help="Generate an HTML report. Optionally specify the file path.")
    parser.add_argument("--web-interface", action="store_true", help="Start the web-based GUI interface")

    args = parser.parse_args()


    ######## Banner #############
    if not args.silent:
        print(f"""
    _._     _,-'""`-._
    (,-.`._,'(       |\\`-/|   @justakazh
        `-.-' \\ )-`( , {ConsoleColors.RED}o{ConsoleColors.ENDC} {ConsoleColors.RED}o{ConsoleColors.ENDC})
            `-    \\`_`"'-
SICAT - The Useful {ConsoleColors.RED}Vulnerability{ConsoleColors.ENDC} & {ConsoleColors.RED}Exploit{ConsoleColors.ENDC} Finder
    """)


    if args.web_interface:
        try:
            start_server()
            return
        except ImportError as e:
            print(f"{ConsoleColors.FAIL}[-] Error starting web server: {e}. Please ensure flask is installed (pip install flask).{ConsoleColors.ENDC}")
            return
        except Exception as e:
             print(f"{ConsoleColors.FAIL}[-] Error starting web server: {e}{ConsoleColors.ENDC}")
             return

    # If no specific module is selected, select all
    if not (args.exploit_db or args.nvd_nist or args.cve_org or args.nuclei_templates or 
            args.github or args.metasploit_framework or args.nse_script or args.wordfence_cve):
        # Auto-select all modules if none are specified
        args.exploit_db = True
        args.nvd_nist = True
        args.cve_org = True
        args.nuclei_templates = True
        args.github = True
        args.metasploit_framework = True
        args.nse_script = True
        args.wordfence_cve = True

    keywords = []

    # 1. Manual Keyword
    if args.keyword:
        keywords.append(args.keyword)

    # 2. Nmap Scan
    if args.nmap:
        nm = Nmap()
        nm.scan(args.nmap)
        if nm.port_services:
            # print(f"{ConsoleColors.GREEN}[+] Nmap Services found: {nm.port_services}{ConsoleColors.ENDC}")
            keywords.extend(nm.port_services)

    # 3. Nmap XML File
    if args.nmap_file:
        from lib.nmap_file import NmapParse
        np = NmapParse()
        np.parse(args.nmap_file)
        if np.port_services:
            # print(f"{ConsoleColors.GREEN}[+] Nmap XML Services found: {np.port_services}{ConsoleColors.ENDC}")
            keywords.extend(np.port_services)

    # 4. Web Technologies (Wappalyzer)
    if args.web:
        from lib.wappalyzer_scan import WebTech
        wt = WebTech()
        wt.scan(args.web)
        if wt.webtech:
             # print(f"{ConsoleColors.GREEN}[+] Web Technologies found: {wt.webtech}{ConsoleColors.ENDC}")
             keywords.extend(wt.webtech)

    # Deduplicate and build keywords
    kb = KeywordBuilder()
    kb.build(keywords)
    keywords = kb.keywords

    if not keywords:
        print(f"{ConsoleColors.FAIL}[-] No keywords provided. Use -k, -nmap, -nmap-file, or -web.{ConsoleColors.ENDC}")
        return

    print(f"{ConsoleColors.BLUE}[*] Total Keywords to search: {len(keywords)}{ConsoleColors.ENDC}")
    for k in keywords:
        print(f"{ConsoleColors.BLUE} -> {k}{ConsoleColors.ENDC}")
    print()

    all_results = []

    for keyword in keywords:
        print(f"{ConsoleColors.HEADER}>>> Searching for: {keyword} <<<{ConsoleColors.ENDC}")
        
        if args.exploit_db:
            try:
                scanner = Exploitdb()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running ExploitDB: {e}")

        if args.nvd_nist:
            try:
                scanner = NVDNIST()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running NVD NIST: {e}")

        if args.cve_org:
            try:
                scanner = CVEORG()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running CVE.org: {e}")

        if args.nuclei_templates:
            try:
                scanner = NucleiTemplates()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running Nuclei Templates: {e}")

        if args.wordfence_cve:
            try:
                scanner = WordfenceCVE()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running Wordfence CVE: {e}")

        if args.github:
            try:
                scanner = Github()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running Github: {e}")

        if args.metasploit_framework:
            try:
                scanner = MetasploitFramework()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running Metasploit Framework: {e}")

        if args.nse_script:
            try:
                scanner = NSEScript()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running NSE Script: {e}")

        

    # Output Saving Logic
    print("")
    print("")
    if args.output:
        try:
            output_path = args.output
            output_type = args.output_type.lower()
            
            # Ensure directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if output_type == "json":
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(all_results, f, indent=4)
            else:
                # Text output
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(f"SiCat Results for keyword: {keyword}\n")
                    f.write("=" * 60 + "\n\n")
                    for item in all_results:
                        f.write(f"Source: {item.get('source_name', 'Unknown')}\n")
                        # Iterate through all other keys
                        for k, v in item.items():
                            if k != 'source_name':
                                f.write(f"{k.capitalize()}: {v}\n")
                        f.write("-" * 40 + "\n")
            
            if not args.silent:
                print(f"{ConsoleColors.GREEN}[+] Output saved to {output_path} ({output_type}){ConsoleColors.ENDC}")

        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error saving output: {e}{ConsoleColors.ENDC}")

    if args.report:
        try:
            print(f"{ConsoleColors.BLUE}[*] Generating HTML report...{ConsoleColors.ENDC}")
            rg = ReportGenerator(all_results, keywords)
            
            report_name = None
            if args.report != 'default':
                # User specified a path for the report
                report_name = args.report
            elif args.output:
                # Fallback: derive from output argument if report path not specified
                report_name = os.path.splitext(args.output)[0] + "_report.html"
            
            saved_path = rg.save_report(report_name)
            if saved_path:
                print(f"{ConsoleColors.GREEN}[+] Report saved to {saved_path}{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error generating report: {e}{ConsoleColors.ENDC}")

if __name__ == "__main__":
    main()
