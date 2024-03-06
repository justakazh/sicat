from lib.vuln_exploitobserver import ExploitObserver

keyword = "CVE-2021-3450"
# keyword = "esp32"
ExploitObserver = ExploitObserver()

getnvd = ExploitObserver.find(keyword)