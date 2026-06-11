# Admin CMS Dashboard System Walkthrough

I have completed the implementation of the local Admin CMS page generation system, including deletion features.

### Components Created

1. **[admin_server.py](file:///home/tahsin/Documents/code/i/admin_server.py)**
   - Local Python-based HTTP dev server running on port `8000`.
   - Supports GET endpoints to retrieve categories and pages.
   - Supports POST endpoints to dynamically generate sub-pages (categories) and leaf-pages (content files containing verses/cards).
   - Automatically parses all existing HTML files on the site and synchronizes desktop and mobile dropdown navigation bars with any new categories created.
   - **Deletion API**: Added `/api/delete-sub-page` and `/api/delete-leaf-page` to clean up folders/files and keep navbars, indices, and grid lists updated when components are deleted.

2. **[admin.html](file:///home/tahsin/Documents/code/i/admin.html)**
   - Clean, dark-green themed admin panel.
   - Form to create new subpage categories.
   - Dynamic list input forms to create content leafpages, with fields to add as many card sections (containing Arabic text, Bangla/English translation, and Reference sources) as needed.
   - **Deletion buttons**: Incorporated buttons next to categories and leaf pages in the current site structure column to delete them immediately with a confirmation modal.

### Running the CMS
To run the CMS locally:
```bash
python3 admin_server.py
```
Then visit **`http://localhost:8000/admin.html`** in your browser.
