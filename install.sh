#!/bin/bash

# SICAT Installation Script

echo -e "\033[0;34m[*] SICAT Installation Script\033[0m"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "\033[0;31m[-] Python 3 is not installed. Please install it first.\033[0m"
    exit 1
fi

# Check for PIP
if ! command -v pip3 &> /dev/null; then
    echo -e "\033[0;33m[!] pip3 not found, checking pip...\033[0m"
    if ! command -v pip &> /dev/null; then
        echo -e "\033[0;31m[-] pip is not installed. Please install python3-pip.\033[0m"
        exit 1
    fi
fi

# Check for Nmap
if ! command -v nmap &> /dev/null; then
    echo -e "\033[0;33m[!] Nmap not found. Attempting to install...\033[0m"
    if [ -x "$(command -v apt)" ]; then
        sudo apt update && sudo apt install -y nmap
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y nmap
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install -y nmap
    elif [ -x "$(command -v pacman)" ]; then
        sudo pacman -S --noconfirm nmap
    elif [ -x "$(command -v brew)" ]; then
        brew install nmap
    else
        echo -e "\033[0;31m[-] Could not install Nmap automatically. Please install it manually.\033[0m"
    fi
else
    echo -e "\033[0;32m[+] Nmap is already installed.\033[0m"
fi

echo -e "\033[0;34m[*] Installing SICAT system-wide...\033[0m"

# Install function to handle PEP 668 (Kali/Debian 12+)
install_sicat() {
    # 1. Try pipx if available (Best practice)
    if command -v pipx &> /dev/null; then
        echo -e "\033[0;33m[*] 'pipx' found. Using pipx for installation...\033[0m"
        pipx install . --force
        return $?
    fi

    # 2. Try standard pip install
    if pip3 install .; then
        return 0
    fi

    # 3. Fallback: PEP 668 --break-system-packages
    echo -e "\n\033[0;33m[!] Standard install failed (Externally Managed Environment detected).\033[0m"
    echo -e "\033[0;33m[*] Retrying with --break-system-packages...\033[0m"
    pip3 install . --break-system-packages
    return $?
}

if install_sicat; then
    echo -e "\n\033[0;32m[+] Successfully installed SICAT!\033[0m"
    echo -e "[*] You can now run: \033[1msicat --help\033[0m"
    exit 0
else
    echo -e "\n\033[0;31m[-] All installation attempts failed.\033[0m"
    echo -e "[*] Try running: \033[1mpipx install .\033[0m"
    exit 1
fi
