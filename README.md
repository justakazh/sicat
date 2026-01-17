# SICAT - The Useful Vulnerability & Exploit Finder

<div align="center">
    <img src="https://socialify.git.ci/justakazh/sicat/image?description=1&font=Inter&language=1&name=1&owner=1&pattern=Circuit%20Board&theme=Dark" alt="SICAT" width="640" height="320" />
</div>

<div align="center">
    <h2> Advanced Vulnerability & Exploit Scanner </h2>
    <p>
        <a href="https://github.com/justakazh/sicat/stargazers">
            <img src="https://img.shields.io/github/stars/justakazh/sicat?style=for-the-badge&color=blue" alt="Stars" />
        </a>
        <a href="https://github.com/justakazh/sicat/forks">
            <img src="https://img.shields.io/github/forks/justakazh/sicat?style=for-the-badge&color=purple" alt="Forks" />
        </a>
        <a href="https://github.com/justakazh/sicat/issues">
            <img src="https://img.shields.io/github/issues/justakazh/sicat?style=for-the-badge&color=red" alt="Issues" />
        </a>
        <a href="https://github.com/justakazh/sicat/blob/main/LICENSE">
            <img src="https://img.shields.io/github/license/justakazh/sicat?style=for-the-badge&color=green" alt="License" />
        </a>
    </p>
</div>

**SICAT** is a powerful tool designed to aggregate and search for vulnerabilities and exploits from multiple high-profile sources. It simplifies the reconnaissance phase by automatically checking reputable databases based on keywords, Nmap scan results, or detected web technologies.

---

## Key Improvements & Features

This version of **SICAT** introduces significant enhancements over the original implementation:

### 1. Modern Web Interface
- **New GUI**: A stunning, dark-themed web interface accessible via `--web-interface`.
- **Hacker Aesthetics**: Features animated ASCII art, "Matrix-like" loading screens, and a minimalist search engine feel.
- **Interactive**: Real-time visual feedback during scans and easy-to-use toggle chips for source selection.

### 2. Professional Reporting
- **HTML Reports**: Generates detailed, interactive HTML reports (`-r`) using DataTables.
- **Features**: Sortable columns, search filtering, pagination, and a clean, responsive design matching the CLI's dark theme.

### 3. Intelligent Keyword Generation
- **Auto-Discovery**: Automatically builds search keywords from:
    - **Nmap Scans**: Live IP scanning (`-nmap`) or XML file parsing (`-nmap-file`).
    - **Web Technology Detection**: Wappalyzer integration (`-web`) to identify running stacks (CMS, Server, Frameworks).
- **Keyword Builder**: Deduplicates and refines keywords for more accurate search results.

### 4. New & Enhanced Sources
Expanded search capabilities across 8 major databases:
- **[Exploit-DB](https://www.exploit-db.com/)**: Classic exploit archive.
- **[NVD NIST](https://nvd.nist.gov/)**: National Vulnerability Database.
- **[CVE.org](https://www.cve.org/)**: Official CVE records.
- **[GitHub](https://github.com/)**: Public repositories and PoCs.
- **[Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates)**: Community-curated vulnerability templates.
- **[Wordfence CVE](https://github.com/topscoder/nuclei-wordfence-cve)**: Nuclei templates specifically for WordPress vulnerabilities.
- **[Metasploit Framework](https://www.metasploit.com/)**: Replaceable modules.
- **[NSE Scripts](https://nmap.org/book/nse.html)**: Nmap Scripting Engine scripts.

### 5. Optimized Experience
- **Refined CLI**: Cleaner argparse help, better console output tables, and silent mode (`-s`).
- **Performance**: Multithreaded scanning structure (where applicable) for faster gathering.

---

## Installation

### Linux / WSL / MacOS

Quickly install dependencies and add `sicat` to your system path using the installer script. This supports standard Debian/Ubuntu, Kali (fixes PEP 668 errors), Fedora, Arch, and MacOS environments.

```bash
# Clone the repository
git clone https://github.com/justakazh/sicat.git
cd sicat

# Make script executable
chmod +x install.sh

# Run installer
./install.sh
```

### Windows

Double-click `install.bat` or run it from the command prompt. This will:
1. Check for Python and Nmap.
2. Install Nmap via Winget if missing (requires Admin).
3. Install Python dependencies.
4. Verify the `sicat` command is available in your PATH.

### Docker

You can also run SICAT in a container to avoid dependency issues.

1. **Build the image**:
   ```bash
   docker build -t sicat .
   ```

2. **Run the container**:
   ```bash
   docker run --rm -it sicat -k "wordpress"
   ```

### Manual Installation (Advanced)

```bash
# Install system-wide
pip install .

# Or for development
pip install -e .
```

---

## Configuration

Some modules (like GitHub, Nuclei Templates, Wordfence CVE) require a GitHub Personal Access Token to avoid API rate limits.

1. **Auto-Generate**: Run `sicat` once, and it will create `~/.sicat/config.json`.
2. **Edit**: Open `~/.sicat/config.json` and add your token:

```json
{
    "gh_token": "YOUR_GITHUB_ACCESS_TOKEN"
}
```

> **Why?** Without a token, GitHub allows only 60 requests/hour. With a token, you get 5,000/hour, ensuring deep searches without interruption.

---

## Usage

### CLI Mode

**Basic Search:**
```bash
sicat -k "WordPress 5.8"
```

**Search Specific Sources:**
```bash
sicat -k "Apache Struts" -edb -gh -nuclei
```

**Generate HTML Report:**
```bash
sicat -k "Joomla" -o results.json -r report.html
```

**Auto-Scan via Nmap:**
```bash
# Scans the target IP with Nmap first, then searches exploits for found services
sicat -nmap 192.168.1.10 -edb -cve
```

**Auto-Scan via Web Detection:**
```bash
# Detects technologies (e.g. Laravel, Vue.js) and searches exploits for them
sicat -web https://example.com -gh -nvd
```

### Web Interface Mode

Launch the web GUI to run scans from your browser:

```bash
sicat --web-interface
```
> Navigate to `http://localhost:5000` in your browser.

## CLI Options

```text
  -u, --update          Update all local databases and resources
  -k KEYWORD            Specific keyword to search for (e.g. 'WordPress 5.8')
  -nmap TARGET          Target IP for live Nmap scan
  -nmap-file FILE       Path to Nmap XML file
  -web URL              Target URL for Wappalyzer scan
  
  --web-interface       Start the web-based GUI interface

  -edb                  Enable search in Exploit-DB
  -nvd                  Enable search in NVD NIST Database
  -cve                  Enable search in CVE.org
  -nuclei               Enable search in Nuclei Templates
  -wcve                 Enable search in Wordfence CVE Templates
  -gh                   Enable search in GitHub Repositories
  -msf                  Enable search in Metasploit Framework
  -nse                  Enable search in Nmap NSE Scripts

  -s                    Run in silent mode
  -l LIMIT              Limit the number of results per module (default: 25)
  -o OUTPUT             Path to save the console output
  -ot {text,json}       Format of the output file
  -r [FILE]             Generate an HTML report
```

---

## Contribution

Contributions are welcome! Please check [CONTRIBUTE.md](CONTRIBUTE.md) for a guide on how to add new sources or features.

## Legal Disclaimer

**SICAT** is intended for educational and ethical testing purposes only. Usage of this tool for attacking targets without prior mutual consent is illegal. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

## License

This project is licensed under the MIT License.

---
<div align="center">
    Made with love by @justakazh
</div>
