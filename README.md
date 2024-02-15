
# SiCat - The useful exploit finder

![SiCat Preview](vendor/preview.png)
  

## Introduction

SiCat is an advanced exploit search tool designed to identify and gather information about exploits from both open sources and local repositories effectively. With a focus on cybersecurity, SiCat allows users to quickly search online, finding potential vulnerabilities and relevant exploits for ongoing projects or systems.

  

SiCat's main strength lies in its ability to traverse both online and local resources to collect information about relevant exploitations. This tool aids cybersecurity professionals and researchers in understanding potential security risks, providing valuable insights to enhance system security.

  

### SiCat Resources

 - [Exploit-DB](https://www.exploit-db.com/)
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
| `--exploitalert` | Use ExploitAlert as info source |
| `--msfmoduke` | Use metasploit as info source |
| `-o OUTPUT` | Path to save output to |
| `-ot OUTPUT_TYPE` | Output file type: json or html |


### Examples

  

*From keyword*

```

python sicat -k telerik --exploitdb --msfmodule

```

  

*From nmap output*

```

nmap -sV localhost -oX nmap_out.xml
python sicat -nm nnmap_out.xml --packetstorm

```

## To-do
- [ ] Input from nmap result from pipeline
- [ ] Nmap multiple host support
- [ ] Search NSE Script

## Contribution

I'm aware that perfection is elusive in coding. If you come across any bugs, feel free to contribute by fixing the code or suggesting new features. Your input is always welcomed and valued.
