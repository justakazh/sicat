
import os
from datetime import datetime
import json
import html

class ReportGenerator:
    def __init__(self, results, keywords):
        self.results = results
        self.keywords = keywords
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_html(self):
        # Calculate stats and group by source
        source_counts = {}
        grouped_results = {}
        for r in self.results:
            s = r.get('source_name', 'Unknown')
            source_counts[s] = source_counts.get(s, 0) + 1
            if s not in grouped_results:
                grouped_results[s] = []
            grouped_results[s].append(r)
        
        # Prepare content parts
        keywords_html = "".join([f'<span class="bg-dark-200 border border-primary text-primary px-3 py-1 rounded-full text-xs font-mono mr-2 mb-2 inline-flex items-center whitespace-nowrap"><i class="fa-solid fa-fingerprint mr-2"></i>{html.escape(k.replace("\n", " "))}</span>' for k in self.keywords])
        
        source_counts_html = ''.join(f'''
            <div class="bg-dark-100 p-5 rounded-xl border border-gray-700/50 hover:border-secondary/50 shadow-lg transform transition hover:-translate-y-1 relative overflow-hidden group">
                <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <i class="fa-solid fa-box-open text-6xl text-secondary"></i>
                </div>
                <h3 class="text-gray-400 text-xs font-bold uppercase tracking-wider mb-2 relative z-10">{k}</h3>
                <div class="text-3xl font-extrabold text-white relative z-10">{v}</div>
            </div>
            ''' for k, v in source_counts.items())

        tables_html = ""
        if not self.results:
            tables_html = '<div class="text-center p-10 text-gray-400"><i class="fa-solid fa-magnifying-glass text-4xl mb-4 opacity-50"></i><br>No results found</div>'
        else:
            # Column Icon Mapping
            col_icons = {
                'title': 'fa-file-lines', 'name': 'fa-file-lines',
                'keyword': 'fa-fingerprint',
                'description': 'fa-align-left', 'path': 'fa-folder-open',
                'command': 'fa-terminal',
                'source_link': 'fa-link', 'url': 'fa-link', 'link': 'fa-link', 'href': 'fa-link',
                'platform': 'fa-desktop',
                'type': 'fa-shapes',
                'date': 'fa-calendar-days',
                'categories': 'fa-layer-group',
                'author_id': 'fa-user'
            }

            for source, items in grouped_results.items():
                # Identify all unique keys in this group, excluding internal ones
                keys = set()
                allowed_keys = []
                
                # First pass to find all keys
                for item in items:
                    keys.update(item.keys())
                
                # Filter and order keys
                ignore_keys = ['source_name', 'searchBy']
                
                # Priority keys to show first
                priority_head = ['title', 'name', 'keyword', 'platform', 'type', 'description', 'path']
                priority_tail = ['categories', 'date', 'author_id', 'command', 'source_link', 'url', 'link', 'href']
                
                # Determine columns
                final_columns = []
                
                # Add priority head keys if they exist
                for k in priority_head:
                    if k in keys and k not in ignore_keys:
                        final_columns.append(k)
                        
                # Add any other keys not in priority or ignore
                for k in keys:
                    if k not in ignore_keys and k not in priority_head and k not in priority_tail:
                        final_columns.append(k)
                        
                # Add priority tail keys
                for k in priority_tail:
                    if k in keys and k not in ignore_keys:
                        final_columns.append(k)

                # Generate Table Header
                thead = "<thead><tr class='text-left text-primary uppercase text-xs tracking-wider'>"
                for col in final_columns:
                    # icon = col_icons.get(col, 'fa-table-columns') # Icon removed as requested
                    thead += f"<th class='py-4 px-4 font-bold border-b border-gray-700 bg-dark-200/50'>{col.replace('_', ' ').upper()}</th>"
                thead += "</tr></thead>"
                
                # Generate Table Body
                tbody = "<tbody>" + self._generate_rows(items, final_columns) + "</tbody>"
                
                tables_html += f"""
                <div class="mb-16">
                    <div class="flex items-center mb-6">
                        <div class="p-2 bg-secondary/10 rounded-lg mr-3">
                            <i class="fa-solid fa-server text-secondary text-xl"></i>
                        </div>
                        <h2 class="text-2xl font-bold text-white tracking-tight">{html.escape(source)}</h2>
                        <span class="ml-4 px-3 py-1 bg-dark-100 text-gray-400 text-xs rounded-full border border-gray-700">{str(len(items))} findings</span>
                    </div>
                    <div class="bg-dark-200 rounded-xl shadow-2xl border border-gray-700/50 p-6">
                        <table class="sicat-table w-full text-sm text-left text-gray-300">
                            {thead}
                            {tbody}
                        </table>
                    </div>
                </div>
                """

        # Read template
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'base.html')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Replace placeholders
            html_content = template_content.replace('{{ timestamp }}', self.timestamp) \
                                           .replace('{{ keywords_html }}', keywords_html) \
                                           .replace('{{ total_results }}', str(len(self.results))) \
                                           .replace('{{ source_counts_html }}', source_counts_html) \
                                           .replace('{{ tables_html }}', tables_html)
            
            return html_content
        except Exception as e:
            print(f"Error loading template: {e}")
            return "Error generating report"

    def _generate_rows(self, items, columns):
        rows = ""
        for item in items:
            rows += "<tr class='hover:bg-dark-100 transition-colors border-b border-gray-700 last:border-0'>"
            for col in columns:
                val = item.get(col, '')
                
                # Check for empty value
                if val is None or str(val).strip() == "":
                    cell_content = "-"
                else:
                    # Formatting based on column type
                    cell_content = str(val)
                    
                    if col in ['source_link', 'url', 'link', 'href']:
                        cell_content = f'<a href="{val}" target="_blank" class="inline-flex items-center px-3 py-1 rounded-md bg-primary/10 text-primary hover:bg-primary/20 border border-primary/20 transition-all text-xs font-bold uppercase tracking-wide"><i class="fa-solid fa-arrow-up-right-from-square mr-2"></i>View</a>'
                    elif col in ['command']:
                        cell_content = f'<code class="bg-dark-600 px-2 py-1 rounded text-red-400 font-mono text-xs select-all whitespace-nowrap">{html.escape(str(val))}</code>'
                    elif col in ['keyword']:
                         cell_content = f'<span class="bg-dark-400 text-green-400 px-2 py-0.5 rounded text-xs border border-green-400/30 whitespace-nowrap">{html.escape(str(val).replace(chr(10), " "))}</span>'
                    elif len(cell_content) > 200:
                        # Truncate long descriptions
                        cell_content = html.escape(cell_content[:197]) + "..."
                    else:
                        cell_content = html.escape(cell_content)
                    
                rows += f"<td class='py-3 px-4 align-top'>{cell_content}</td>"
            rows += "</tr>"
        return rows

    def save_report(self, filename=None):
        if not filename:
            filename = f"sicat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        # ensure extension
        if not filename.endswith('.html'):
            filename += '.html'

        content = self.generate_html()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return filename
        except Exception as e:
            print(f"Error saving report: {e}")
            return None
