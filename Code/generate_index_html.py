import os

docs_folder = "docs"
html_files = [f for f in os.listdir(docs_folder) if f.endswith(".html") and f != "index.html"]

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Project Documentation Index</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        ul { line-height: 1.6; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>📘 Project Documentation Index</h1>
    <p>Select a file below to view its generated documentation:</p>
    <ul>
"""

# Add each file as a list item with a hyperlink
for file in sorted(html_files):
    name = file.replace(".html", "").replace("_", " ").title()
    html_content += f'        <li><a href="{file}">{name}</a></li>\n'

html_content += """    </ul>
    <p style="margin-top: 2em; font-size: 0.9em; color: #888;">Generated automatically by generate_index_html.py</p>
</body>
</html>
"""

# Write to index.html
with open(os.path.join(docs_folder, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ docs/index.html created!")
