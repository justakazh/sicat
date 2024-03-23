
# SiCat - The useful exploit finder

![SiCat Preview](vendor/preview.png)
  

## Introduction

SiCat is an advanced exploit search tool designed to identify and gather information about exploits from both open sources and local repositories effectively. With a focus on cybersecurity, SiCat allows users to quickly search online, finding potential vulnerabilities and relevant exploits for ongoing projects or systems.

  

SiCat's main strength lies in its ability to traverse both online and local resources to collect information about relevant exploitations. This tool aids cybersecurity professionals and researchers in understanding potential security risks, providing valuable insights to enhance system security.

  

### SiCat Resources

 - [Exploit-DB](https://www.exploit-db.com/)
 - [Exploit Observer](https://exploit.observer)
 - [Packetstorm Security](https://packetstormsecurity.com/)
 - [Exploit Alert](https://www.exploitalert.com/)
 - [NVD Database](https://nvd.nist.gov/)
 - [Metasploit Modules](https://github.com/rapid7/metasploit-framework/tree/master/modules)


## Installation

``` bash
git clone https://github.com/justakazh/sicat.git && cd sicat

pip  install  -r  requirements.txt

```

  

## Usage
```bash

~$ python sicat.py --help

```  

### Command Line Options:

| Command | Description |
| --- | --- |
| `-h` | Show help message and exit |
| `-k KEYWORD` |  |
| `-kv KEYWORK_VERSION` |  |
| `-nm` | Identify via nmap output |
| `--nvd` | Use NVD as info source |
| `--packetstorm` | Use PacketStorm as info source |
| `--exploitdb` | Use ExploitDB as info source |
| `--exploitobserver` | Use ExploitObserver as info source |
| `--exploitalert` | Use ExploitAlert as info source |
| `--msfmoduke` | Use metasploit as info source |
| `-o OUTPUT` | Path to save output to |
| `-ot OUTPUT_TYPE` | Output file type: json or html |


-k KEYWORD, --keyword KEYWORD

File name or path to save the output

-kv KEYWORD_VERSION, --keyword_version KEYWORD_VERSION

File name or path to save the output

-nm NMAP, --nmap NMAP

Identify via nmap output

--nvd Use NVD as a source of information

--packetstorm Use PacketStorm as a source of information

--exploitdb Use ExploitDB as a source of information

--exploitobserver Use ExploitObserver as a source of information

--exploitalert Use ExploitAlert as a source of information

--msfmodule Use metasploit module as a source of information

-o OUTPUT, --output OUTPUT

path to save the output

-ot OUTPUT_TYPE, --output_type OUTPUT_TYPE

output file type json and html

```

### Examples

  

*From keyword*

```

python sicat.py -k telerik --exploitdb --msfmodule
python sicat.py -k CVE-2021-3450 --exploitobserver --output .

```

  

*From nmap output*

```

nmap --open -sV localhost -oX nmap_out.xml
python sicat.py -nm nmap_out.xml --packetstorm

```

## To-do
- [ ] Input from nmap result from pipeline
- [ ] Nmap multiple host support
- [ ] Search NSE Script
- [ ] Search by PORT

## Contribution

I'm aware that perfection is elusive in coding. If you come across any bugs, feel free to contribute by fixing the code or suggesting new features. Your input is always welcomed and valued.
