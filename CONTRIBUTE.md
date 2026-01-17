# How to Contribute a New Source to SICAT

We welcome contributions to expand SICAT's scanning capabilities! Adding a new source involves creating a new module module, registering it, and integrating it into the main CLI tool.

Follow this step-by-step guide to add a new intelligence source.

---

## 1. Create the Source Module

Create a new Python file in the `sources/` directory (e.g., `sources/my_new_source.py`).

Your class structure should follow this standard pattern used by existing sources:

**Template (`sources/my_new_source.py`):**

```python
################################################################
# Source   : https://api.example.com
# Coded By : YourName
# Contribute by creating your own source following the guide:
# https://github.com/justakazh/sicat/CONTRIBUTE.md 
################################################################

import requests
import html
from lib.utils import highlight_keyword, ConsoleColors, print_attribute

class MyNewSource:

    def __init__(self):
        ### Result data will be saved here ##
        self.result = []
        self.keyword = None
        self.url = "https://api.example.com/v1/search"

    def WrapperStart(self, silent=False):
        if not silent:
            print("-" * 75)
            print(f"{ConsoleColors.BLUE}[+] Searching in My New Source{ConsoleColors.ENDC}")
            print("-" * 75)

    def Output(self, data, limit, silent=False):
        for item in data:
            if limit is not None and len(self.result) >= limit:
                break
            
            # Extract fields from your API response
            title = item.get('title', 'Unknown')
            link = item.get('url', '')
            description = item.get('description', 'No description')
            
            # Standardize the result object
            wrap = {
                "title": title,
                "description": description,
                "source_name": "My New Source",
                "source_link": link,
                "searchBy": "keyword",
                "keyword": self.keyword
            }
            
            self.result.append(wrap)

            # Print to console using helper
            if not silent:
                print_attribute("Title", html.unescape(title), self.keyword)
                print_attribute("Link", link, self.keyword, no_wrap=True)
                print_attribute("Description", html.unescape(description), self.keyword)
                print()

    def search(self, keyword=None, limit=None, silent=False):
        self.keyword = keyword
        try:
            self.WrapperStart(silent)

            # --- API Request Logic ---
            params = {'q': keyword}
            response = requests.get(self.url, params=params)
            
            if response.status_code == 200:
                data = response.json().get('items', []) # Adjust based on API structure
                self.Output(data, limit, silent)
            else:
                if not silent:
                    print(f"{ConsoleColors.FAIL}[-] API Error: {response.status_code}{ConsoleColors.ENDC}")

            self.wrapperEnd(silent)

        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in MyNewSource [search]: {str(e)}{ConsoleColors.ENDC}")

    def wrapperEnd(self, silent=False):
        if silent:
            return
        try:
            if len(self.result) == 0:
                print(f"{ConsoleColors.FAIL}[-] No results found in My New Source!{ConsoleColors.ENDC}")
            else:
                print(f"{ConsoleColors.BOLD}[*] Total Result : {len(self.result)} found!{ConsoleColors.ENDC}")
        except Exception as e:
            print(f"{ConsoleColors.FAIL}[-] Error in MyNewSource [wrapperEnd]: {str(e)}{ConsoleColors.ENDC}")
```

---

## 2. Register the Module

Open `sources/__init__.py` and export your new class so it can be imported easily.

**Edit `sources/__init__.py`:**

```python
from .exploit_db import Exploitdb
from .nvd_nist import NVDNIST
# ... existing imports ...
from .my_new_source import MyNewSource  # <--- Add this line

# Add your class to the __all__ list to ensure it is exported
__all__ = [
    "Exploitdb",
    "NVDNIST",
    # ...
    "MyNewSource" # <--- Add this line
]
```

---

## 3. Integrate into CLI (`sicat.py`)

You need to add a command-line argument for your source and call the search method in the main execution loop.

**Step 3a: Add CLI Argument**

In `sicat.py`, inside the `argparse` setup (around line 30+):

```python
# Modules Arguments
parser.add_argument("-mns", "--my-new-source", action="store_true", help="Enable search in My New Source")
```

**Step 3b: Add to Auto-Select Logic**

In `sicat.py`, update the "select all" check (around line 75):

```python
# If no specific module is selected, select all
if not (args.exploit_db or ... or args.my_new_source): 
    # ...
    args.my_new_source = True # <--- Add this line
```

**Step 3c: Add Execution Logic**

In `sicat.py`, inside the main keyword loop (around line 130+, after other module checks), add the block to run your scanner:

```python
        if args.my_new_source:
            try:
                scanner = MyNewSource()
                scanner.search(keyword, args.limit, args.silent)
                if scanner.result:
                    all_results.extend(scanner.result)
            except Exception as e:
                print(f"[-] Error running My New Source: {e}")
```

---

## 4. Add to Web Interface & Backend

To enable your source in the Web GUI (`--web-interface`), you must update both the frontend template and the backend logic.

**Step 4a: Update Frontend (`lib/templates/index.html`)**

Find the "Modules Selection Card" section and add a new checkbox chip using the existing style:

```html
<!-- My New Source -->
<label class="cursor-pointer group">
    <input type="checkbox" name="modules" value="my_new_source" checked class="peer sr-only">
    <div
        class="px-4 py-1.5 rounded-full bg-dark-300 border border-dark-400 text-slate-400 text-sm font-medium transition-all peer-checked:bg-primary peer-checked:text-white peer-checked:border-primary peer-checked:shadow-[0_0_15px_rgba(59,130,246,0.4)] hover:bg-dark-400 hover:border-slate-500">
        My New Source
    </div>
</label>
```

**Step 4b: Update Backend (`lib/web_server.py`)**

The web server processes the form data and runs the selected scanners. You must add the logic to handle your new module key (`value="my_new_source"`).

In `lib/web_server.py`, inside the `/scan` route handler:

```python
    # ... inside the module scanning loop ...

    if 'my_new_source' in selected_modules:
        try:
            scanner = MyNewSource()
            scanner.search(keyword, limit, silent=True) # Always force silent=True for web
            if scanner.result:
                all_results.extend(scanner.result)
        except Exception as e:
            print(f"Error in My New Source: {e}")
```

---

## 5. Verify Reporting

SICAT's `ReportGenerator` is dynamic. As long as your source's `Output` method populates `self.result` with dictionaries containing standard keys, it will automatically appear in the HTML report.

**Standard Keys:**
*   `source_name` (e.g. "My Source")
*   `source_link` (URL to the finding)
*   `title` or `name`
*   `description` (optional)
*   `keyword` (the term searched)

---

## Checklist

- [ ] Created `sources/my_new_source.py`
- [ ] Registered in `sources/__init__.py`
- [ ] Added argument in `sicat.py`
- [ ] Added execution logic in `sicat.py`
- [ ] Added checkbox in `lib/templates/index.html`
- [ ] Added handler logic in `lib/web_server.py`
- [ ] Tested CLI: `python sicat.py -k "test" -mns`
- [ ] Tested Web: `python sicat.py --web-interface` -> select "My New Source"
