import os
import re
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

SUBPAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="bn">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="../media/logo.svg" type="image/svg+xml">
    <title>{title} - মিসবাহ</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>

<body>

    <nav>
        <div class="nav-left">
            <a href="../index.html" class="logo">মিসবাহ</a>
        </div>

        <div class="nav-center">
            <p class="bismillah">بسم الله الرحمن الرحيم</p>
        </div>

        <div class="nav-right">
            <ul>
                <li><a href="../index.html">প্রচ্ছদ</a></li>
                <li class="dropdown">
                    <a href="#" class="active">আলোচ্য</a>
                    <ul class="dropdown-menu">
                        <!-- CATEGORIES_PLACEHOLDER -->
                    </ul>
                </li>
                <li><a href="../about.html">উদ্দেশ্য</a></li>
            </ul>
        </div>
    </nav>

    <nav class="mobile-nav">
        <div class="mobile-top-bar">
            <div class="m-left"><a href="../index.html" class="logo">মিসবাহ</a></div>
            <div class="m-center">
                <p class="mobile-bismillah">بسم الله</p>
            </div>
            <div class="m-right"><button class="hamburger" onclick="toggleMobileMenu()">☰</button></div>
        </div>
        <ul id="mobile-menu-list">
            <li><a href="../index.html">প্রচ্ছদ</a></li>
            <li>
                <a href="#" onclick="toggleMobileSub(event)">আলোচ্য ▾</a>
                <ul class="mobile-sub-menu" id="mobile-sub">
                    <!-- MOBILE_CATEGORIES_PLACEHOLDER -->
                </ul>
            </li>
            <li><a href="../about.html">উদ্দেশ্য</a></li>
        </ul>
    </nav>

    <header class="{id}-hero" style="{header_style}">
        <h1 style="{h1_style}">{title}</h1>
    </header>

    <div class="container boxed">
        <div class="topic-label-section">সূচি</div>

        <div class="topics-grid">
            <!-- TOPICS_PLACEHOLDER -->
        </div>
    </div>
    <br>

    <footer>
        <p class="text" style="color: gold; font-weight: bold; margin: 0;">السلام عليكم ورحمة الله وبركاته</p>
    </footer>

    <script>
        function toggleMobileMenu() {
            var menu = document.getElementById('mobile-menu-list');
            menu.classList.toggle('show');
        }
        function toggleMobileSub(e) {
            e.preventDefault();
            var sub = document.getElementById('mobile-sub');
            sub.style.display = sub.style.display === 'block' ? 'none' : 'block';
        }
        window.onclick = function (event) {
            if (!event.target.matches('.hamburger') && !event.target.closest('#mobile-menu-list')) {
                var menu = document.getElementById('mobile-menu-list');
                if (menu.classList.contains('show')) {
                    menu.classList.remove('show');
                }
            }
        }
    </script>

</body>
</html>
"""

LEAF_TEMPLATE = """<!DOCTYPE html>
<html lang="bn">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="../../media/logo.svg" type="image/svg+xml">
    <title>{title} - মিসবাহ</title>
    <link rel="stylesheet" href="../../assets/style.css">
</head>

<body>

    <nav>
        <div class="nav-left">
            <a href="../../index.html" class="logo">মিসবাহ</a>
        </div>
        <div class="nav-center">
            <p class="bismillah">بسم الله الرحمن الرحيم</p>
        </div>
        <div class="nav-right">
            <ul>
                <li><a href="../../index.html">প্রচ্ছদ</a></li>
                <li class="dropdown">
                    <a href="#" class="active">আলোচ্য</a>
                    <ul class="dropdown-menu">
                        <!-- CATEGORIES_PLACEHOLDER -->
                    </ul>
                </li>
                <li><a href="../../about.html">উদ্দেশ্য</a></li>
            </ul>
        </div>
    </nav>

    <nav class="mobile-nav">
        <div class="mobile-top-bar">
            <div class="m-left"><a href="../../index.html" class="logo">মিসবাহ</a></div>
            <div class="m-center">
                <p class="mobile-bismillah">بسم الله</p>
            </div>
            <div class="m-right"><button class="hamburger" onclick="toggleMobileMenu()">☰</button></div>
        </div>
        <ul id="mobile-menu-list">
            <li><a href="../../index.html">প্রচ্ছদ</a></li>
            <li>
                <a href="#" onclick="toggleMobileSub(event)">আলোচ্য ▾</a>
                <ul class="mobile-sub-menu" id="mobile-sub">
                    <!-- MOBILE_CATEGORIES_PLACEHOLDER -->
                </ul>
            </li>
            <li><a href="../../about.html">উদ্দেশ্য</a></li>
        </ul>
    </nav>

    <div class="header">
        {title}
    </div>
    <div class="master-container">
        <div class="section-title">{section_title}</div>

        <!-- CONTENT_PLACEHOLDER -->
    </div>

    <footer>
        <p class="text" style="color: gold; font-weight: bold; margin: 0;">السلام عليكم ورحمة الله وبركاته</p>
    </footer>

    <script>
        function toggleMobileMenu() {
            var menu = document.getElementById('mobile-menu-list');
            menu.classList.toggle('show');
        }
        function toggleMobileSub(e) {
            e.preventDefault();
            var sub = document.getElementById('mobile-sub');
            sub.style.display = sub.style.display === 'block' ? 'none' : 'block';
        }
        window.onclick = function (event) {
            if (!event.target.matches('.hamburger') && !event.target.closest('#mobile-menu-list')) {
                var menu = document.getElementById('mobile-menu-list');
                if (menu.classList.contains('show')) {
                    menu.classList.remove('show');
                }
            }
        }
    </script>

</body>
</html>
"""


def find_matching_div_end(html, start_idx):
    """Given the position of an opening <div tag, find the index of its matching closing </div>."""
    depth = 0
    i = start_idx
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i
            i += 6
        else:
            i += 1
    return len(html)


def get_categories():
    categories = []
    if not os.path.exists("sub"):
        return categories
    for f in sorted(os.listdir("sub")):
        if f.endswith(".html"):
            path = os.path.join("sub", f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                # Find title
                title_match = re.search(r"<title>(.*?) - মিসবাহ</title>", content)
                title = title_match.group(1) if title_match else f.replace(".html", "").capitalize()
                categories.append({
                    "id": f.replace(".html", ""),
                    "title": title,
                    "filename": f
                })
    return categories


def update_navbars():
    categories = get_categories()
    
    # We will look for files in:
    # 1. Root directory (*.html)
    # 2. sub/ directory (*.html)
    # 3. leaf/* directories (*.html)
    
    def render_nav_list(prefix):
        items = []
        for cat in categories:
            items.append(f'<li><a href="{prefix}{cat["filename"]}">{cat["title"]}</a></li>')
        return "\n                        ".join(items)

    def process_file(file_path, prefix):
        if not os.path.exists(file_path):
            return
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update desktop dropdown
        dropdown_pattern = r"(<ul class=\"dropdown-menu\">)(.*?)(</ul>)"
        replacement = f"\\1\n                        {render_nav_list(prefix)}\n                    \\3"
        content = re.sub(dropdown_pattern, replacement, content, flags=re.DOTALL)

        # Update mobile dropdown
        mobile_pattern = r"(<ul class=\"mobile-sub-menu\" id=\"mobile-sub\">)(.*?)(</ul>)"
        replacement_mob = f"\\1\n                    {render_nav_list(prefix)}\n                \\3"
        content = re.sub(mobile_pattern, replacement_mob, content, flags=re.DOTALL)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 1. Root files
    for f in os.listdir("."):
        if f.endswith(".html") and f != "t.html":
            process_file(f, "sub/")
            
    # 2. sub files
    if os.path.exists("sub"):
        for f in os.listdir("sub"):
            if f.endswith(".html"):
                process_file(os.path.join("sub", f), "")
                
    # 3. leaf files
    if os.path.exists("leaf"):
        for folder in os.listdir("leaf"):
            folder_path = os.path.join("leaf", folder)
            if os.path.isdir(folder_path):
                for f in os.listdir(folder_path):
                    if f.endswith(".html"):
                        process_file(os.path.join(folder_path, f), "../../sub/")


def update_index_subjects_grid(new_cat_id=None, new_cat_title=None, new_cat_desc=None):
    if not os.path.exists("index.html"):
        return
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        
    descriptions = {
        "db": "নিশ্চয়ই আমি তোমাদের খুব কাছেই আছি",
        "fact": "আল্লাহর ফয়সালাই শেষ কথা এবং এটাই চরম সত্য"
    }
    
    card_matches = re.findall(r'<a href="sub/(.*?)\.html" class="subject-card">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</a>', content, flags=re.DOTALL)
    for cat_id, title, desc in card_matches:
        descriptions[cat_id] = desc.strip()
        
    if new_cat_id and new_cat_desc:
        descriptions[new_cat_id] = new_cat_desc
        
    categories = get_categories()
    
    grid_items = []
    for cat in categories:
        cat_id = cat["id"]
        title = cat["title"]
        desc = descriptions.get(cat_id, "")
        grid_items.append(f'            <a href="sub/{cat_id}.html" class="subject-card">\n                <h3>{title}</h3>\n                <p>{desc}</p>\n            </a>')
        
    grid_html = "\n\n".join(grid_items)

    start_tag = '<div class="subjects-grid">'
    start_idx = content.find(start_tag)
    if start_idx != -1:
        content_start = start_idx + len(start_tag)
        end_idx = find_matching_div_end(content, start_idx)
        content = content[:content_start] + "\n" + grid_html + "\n        " + content[end_idx:]
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)


class AdminRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        
        # API Endpoints
        if url.path == "/api/media":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            media_files = []
            if os.path.exists("media"):
                media_files = [f for f in sorted(os.listdir("media")) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
            self.wfile.write(json.dumps({"files": media_files}, ensure_ascii=False).encode("utf-8"))
            return
            
        elif url.path == "/api/structure":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            categories = get_categories()
            # Also get pages under each category
            for cat in categories:
                cat_id = cat["id"]
                cat["pages"] = []
                dir_path = os.path.join("leaf", cat_id)
                if os.path.exists(dir_path):
                    for f in sorted(os.listdir(dir_path)):
                        if f.endswith(".html"):
                            with open(os.path.join(dir_path, f), "r", encoding="utf-8") as file:
                                file_content = file.read()
                                title_match = re.search(r"<title>(.*?) - মিসবাহ</title>", file_content)
                                title = title_match.group(1) if title_match else f
                                cat["pages"].append({
                                    "filename": f,
                                    "title": title
                                })
            
            self.wfile.write(json.dumps({"categories": categories}, ensure_ascii=False).encode("utf-8"))
            return
            
        # Serve static file
        file_path = url.path.lstrip("/")
        if not file_path or file_path == "admin":
            file_path = "admin.html"
            
        if os.path.exists(file_path):
            self.send_response(200)
            if file_path.endswith(".html"):
                self.send_header("Content-Type", "text/html; charset=utf-8")
            elif file_path.endswith(".css"):
                self.send_header("Content-Type", "text/css; charset=utf-8")
            elif file_path.endswith(".js"):
                self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.end_headers()
            
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))
        
        if url.path == "/api/create-sub-page":
            cat_id = data.get("id").strip().lower()
            cat_title = data.get("title").strip()
            
            if not cat_id or not cat_title:
                self.send_json_response(400, {"error": "Missing parameters"})
                return
                
            os.makedirs("sub", exist_ok=True)
            os.makedirs(os.path.join("leaf", cat_id), exist_ok=True)
            
            file_path = os.path.join("sub", f"{cat_id}.html")
            if os.path.exists(file_path):
                self.send_json_response(400, {"error": "Category already exists"})
                return
                
            header_image = data.get("header_image", "").strip()
            if header_image:
                header_style = f"background: url('../media/{header_image}') center/cover; box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.3); padding: 70px 20px; text-align: center; color: white;"
                h1_style = "font-size: 3rem; margin: 0; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);"
            else:
                header_style = "background-color: #064e3b; padding: 70px 20px; text-align: center; color: white;"
                h1_style = "font-size: 3rem; margin: 0;"

            # Render template
            html = SUBPAGE_TEMPLATE.replace("{id}", cat_id).replace("{title}", cat_title)
            html = html.replace("{header_style}", header_style).replace("{h1_style}", h1_style)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
                
            # Update all navbars and index page subjects grid
            update_navbars()
            cat_desc = data.get("description", "").strip()
            update_index_subjects_grid(cat_id, cat_title, cat_desc)
            
            self.send_json_response(200, {"success": True})
            
        elif url.path == "/api/create-leaf-page":
            cat_id = data.get("category").strip().lower()
            filename = data.get("filename").strip()
            if not filename.endswith(".html"):
                filename += ".html"
            title = data.get("title").strip()
            icon = data.get("icon", "📝").strip()
            section_title = data.get("section_title", "বিস্তারিত").strip()
            items = data.get("items", []) # array of {arabic, english, bangla, reference}
            
            if not cat_id or not filename or not title:
                self.send_json_response(400, {"error": "Missing parameters"})
                return
                
            leaf_dir = os.path.join("leaf", cat_id)
            os.makedirs(leaf_dir, exist_ok=True)
            
            # 1. Generate Content sections HTML
            content_sections = []
            for item in items:
                sect_html = f'        <div class="dua-card">\n'
                if item.get("arabic"):
                    sect_html += f'            <div class="section arabic-verse">{item.get("arabic")}</div>\n'
                if item.get("english"):
                    sect_html += f'            <div class="section english-translation">{item.get("english")}</div>\n'
                if item.get("bangla"):
                    sect_html += f'            <div class="section bangla-translation">{item.get("bangla")}</div>\n'
                if item.get("reference"):
                    sect_html += f'            <div class="reference-bar">{item.get("reference")}</div>\n'
                sect_html += "        </div>"
                content_sections.append(sect_html)
                
            content_html = "\n\n".join(content_sections)
            
            # 2. Render and save leaf page
            html = LEAF_TEMPLATE.replace("{title}", title).replace("{section_title}", section_title)
            html = html.replace("<!-- CONTENT_PLACEHOLDER -->", content_html)
            
            leaf_file_path = os.path.join(leaf_dir, filename)
            with open(leaf_file_path, "w", encoding="utf-8") as f:
                f.write(html)
                
            # 3. Add card to the sub page list (sub/<category>.html)
            sub_file_path = os.path.join("sub", f"{cat_id}.html")
            if os.path.exists(sub_file_path):
                with open(sub_file_path, "r", encoding="utf-8") as f:
                    sub_content = f.read()
                    
                start_tag = '<div class="topics-grid">'
                start_idx = sub_content.find(start_tag)
                if start_idx != -1:
                    content_start = start_idx + len(start_tag)
                    end_idx = find_matching_div_end(sub_content, start_idx)
                    inner_grid = sub_content[content_start:end_idx]
                    
                    # Find count of links currently
                    existing_cards = re.findall(r"<a href=.*?class=\"topic-card\"", inner_grid)
                    index_num = len(existing_cards) + 1
                    
                    # Convert to Bengali numbers
                    bengali_digits = {"0":"০", "1":"১", "2":"২", "3":"৩", "4":"৪", "5":"৫", "6":"৬", "7":"৭", "8":"৮", "9":"৯"}
                    index_str = "".join(bengali_digits.get(char, char) for char in str(index_num))
                    
                    new_card = f'\n            <a href="../leaf/{cat_id}/{filename}" class="topic-card">\n'
                    new_card += f'                <div class="topic-index">{index_str}</div>\n'
                    new_card += f'                <div class="topic-icon">{icon}</div>\n'
                    new_card += f'                <div class="topic-text">{title}</div>\n'
                    new_card += '            </a>\n        '
                    
                    new_inner_grid = inner_grid + new_card
                    sub_content = sub_content[:content_start] + new_inner_grid + sub_content[end_idx:]
                    
                    with open(sub_file_path, "w", encoding="utf-8") as f:
                        f.write(sub_content)
                        
            self.send_json_response(200, {"success": True})

        elif url.path == "/api/delete-sub-page":
            cat_id = data.get("id", "").strip().lower()
            if not cat_id:
                self.send_json_response(400, {"error": "Missing parameters"})
                return
            sub_file = os.path.join("sub", f"{cat_id}.html")
            if os.path.exists(sub_file):
                os.remove(sub_file)
            leaf_dir = os.path.join("leaf", cat_id)
            if os.path.exists(leaf_dir):
                import shutil
                shutil.rmtree(leaf_dir)
            update_navbars()
            update_index_subjects_grid()
            self.send_json_response(200, {"success": True})

        elif url.path == "/api/delete-leaf-page":
            cat_id = data.get("category", "").strip().lower()
            filename = data.get("filename", "").strip()
            if not cat_id or not filename:
                self.send_json_response(400, {"error": "Missing parameters"})
                return
            leaf_file = os.path.join("leaf", cat_id, filename)
            if os.path.exists(leaf_file):
                os.remove(leaf_file)
            sub_file_path = os.path.join("sub", f"{cat_id}.html")
            if os.path.exists(sub_file_path):
                with open(sub_file_path, "r", encoding="utf-8") as f:
                    sub_content = f.read()
                
                start_tag = '<div class="topics-grid">'
                start_idx = sub_content.find(start_tag)
                if start_idx != -1:
                    content_start = start_idx + len(start_tag)
                    end_idx = find_matching_div_end(sub_content, start_idx)
                    inner_grid = sub_content[content_start:end_idx]
                    
                    card_pattern = r"(<a href=\"\.\./leaf/[^\"]+/[^\"]+\"[^>]*>.*?</a>)"
                    all_cards = re.findall(card_pattern, inner_grid, flags=re.DOTALL)
                    target_href = f'../leaf/{cat_id}/{filename}'
                    filtered_cards = [c for c in all_cards if target_href not in c]
                    bengali_digits = {"0":"০", "1":"১", "2":"২", "3":"৩", "4":"৪", "5":"৫", "6":"৬", "7":"৭", "8":"৮", "9":"৯"}
                    indexed_cards = []
                    for idx, card in enumerate(filtered_cards, 1):
                        idx_str = "".join(bengali_digits.get(c, c) for c in str(idx))
                        card_reindexed = re.sub(r'(<div class="topic-index">)(.*?)(</div>)', f'\\1{idx_str}\\3', card, flags=re.DOTALL)
                        indexed_cards.append(card_reindexed)
                    new_inner_grid = "\n            " + "\n            ".join(indexed_cards) + "\n        "
                    sub_content = sub_content[:content_start] + new_inner_grid + sub_content[end_idx:]
                    with open(sub_file_path, "w", encoding="utf-8") as f:
                        f.write(sub_content)
            self.send_json_response(200, {"success": True})

        else:
            self.send_error(404, "Endpoint not found")

    def send_json_response(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    print(f"Starting local admin server on http://localhost:{PORT}")
    server = HTTPServer(("0.0.0.0", PORT), AdminRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Stopping admin server.")
