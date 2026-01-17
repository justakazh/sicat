
from colorama import Fore, Style, init
import re
import html
import textwrap
import shutil

init(autoreset=True)

class ConsoleColors:
    HEADER = Fore.MAGENTA + Style.BRIGHT
    BLUE = Fore.BLUE + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    FAIL = Fore.RED + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT
    UNDERLINE = '\033[4m'

def highlight_keyword(text, keyword):
    if not keyword or not text:
        return text
    
    # Case insensitive formatting
    # Custom logic to avoid highlighting http/https when they appear as protocol prefixes
    regex_pattern = re.escape(keyword)
    if keyword.lower() == 'http':
        regex_pattern += r'(?!s?://)' # Don't match http:// or https://
    elif keyword.lower() == 'https':
        regex_pattern += r'(?!://)'   # Don't match https://

    # We use a lambda in sub to preserve the case of the matched text while surrounding it with color
    pattern = re.compile(regex_pattern, re.IGNORECASE)
    return pattern.sub(lambda m: f"{ConsoleColors.FAIL}{m.group(0)}{ConsoleColors.ENDC}", text)

def print_attribute(label, value, keyword=None, no_wrap=False):
    if value is None:
        value = "N/A"
    value = str(value)
    
    # Standardize label width (e.g., 12 chars). 
    # Format: "- Label        : Value"
    # Prefix length calculation: "- " (2) + 12 + " : " (3) = 17
    # Adjust padding as needed. Let's use 13 to cover "Description" comfortably.
    pad_length = 13
    label_prefix = f"- {label:<{pad_length}} : "
    indent = " " * len(label_prefix)
    
    if no_wrap:
        # Don't wrap lines, just concatenate. Highlighting works better this way too.
        wrapped_text = label_prefix + value
    else:
        # Get terminal width, default to 80 if not determined, max out at something reasonable like 100 or 120 so it doesn't span too wide on huge monitors
        term_width = shutil.get_terminal_size((80, 20)).columns
        content_width = min(term_width, 100) # Cap at 100 for readability
        
        # Wrap text
        # initial_indent provided to textwrap includes the label, this ensures the first line fits properly.
        wrapped_text = textwrap.fill(value, width=content_width, initial_indent=label_prefix, subsequent_indent=indent)
    
    # Apply highlighting
    # Note: highlighting adds ANSI codes. If a keyword was split across lines by textwrap, it won't highlight. 
    # This is an accepted trade-off for layout stability.
    final_text = highlight_keyword(wrapped_text, keyword)
    
    # Colorize the Label (the first occurrence of label_prefix)
    # We reconstruct the colored label pattern.
    # Note: If highlight_keyword colored something inside the label (unlikely), replace might fail or double color. 
    # We assume label doesn't contain the keyword usually.
    colored_label_prefix = f"{ConsoleColors.GREEN}-{ConsoleColors.ENDC} {label:<{pad_length}} : "
    
    # Replace only the start
    # To be safe against keyword being in label, we strictly replace the start of string if it matches label_prefix
    if final_text.startswith(label_prefix):
         final_text = colored_label_prefix + final_text[len(label_prefix):]
    else:
        # Fallback if keyword highlighted something in label
        final_text = final_text.replace(label_prefix, colored_label_prefix, 1)

    print(final_text)

def print_banner(text):
    print(f"{ConsoleColors.HEADER}{text}{ConsoleColors.ENDC}")

def print_info(label, value):
    print(f"{ConsoleColors.GREEN}-{ConsoleColors.ENDC} {label:<14} : {value}")

def print_success(text):
    print(f"{ConsoleColors.GREEN}[+] {text}{ConsoleColors.ENDC}")

def print_error(text):
    print(f"{ConsoleColors.FAIL}[-] {text}{ConsoleColors.ENDC}")

def print_warning(text):
    print(f"{ConsoleColors.WARNING}[!] {text}{ConsoleColors.ENDC}")
