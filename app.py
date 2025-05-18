from flask import Flask, request, jsonify, render_template, send_file
import json
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import zipfile
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route: Serve the editor UI
@app.route("/")
def index():
    return render_template("index.html")

# Route: Save the Editor.js content + CSS
@app.route('/save', methods=['POST'])
def save():
    site = request.args.get('site','default')
    data = request.get_json()
    os.makedirs('data', exist_ok=True)
    with open(f'data/{site}.json', 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "saved"})

# Route: Load saved content + CSS
@app.route('/load', methods=['GET'])
def load():
    site = request.args.get('site','default')
    try:
        with open(f'data/{site}.json') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"blocks": [], "css": ""})

# Route: Handle image uploads
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'success': 0, 'message': 'No image file'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': 0, 'message': 'Empty filename'}), 400

    filename = secure_filename(file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({
        'success': 1,
        'file': { 'url': f'/static/uploads/{filename}' }
    })

# Route: Download full website as zip
@app.route('/downloadZip', methods=['GET'])
def download_zip():
    site = request.args.get('site', 'default')
    data_path = f'data/{site}.json'

    if not os.path.exists(data_path):
        return jsonify({'error': f'Site "{site}" not found'}), 404

    # Load saved content
    with open(data_path) as f:
        site_data = json.load(f)

    blocks = site_data.get('blocks', [])
    css = site_data.get('css', '')
    framework = site_data.get('framework', '')

    # Render HTML
    html = render_blocks_to_html(blocks, framework)

    # Collect used image filenames
    used_images = set()
    for block in blocks:
        if block.get("type") == "image":
            file_info = block.get("data", {}).get("file", {})
            url = file_info.get("url", "")
            if url.startswith("/static/uploads/"):
                used_images.add(os.path.basename(url))

    # Prepare zip in memory
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        zf.writestr("index.html", html)
        zf.writestr("style.css", css or "body { font-family: sans-serif; padding: 2rem; text-align: center; }")

        uploads_dir = 'static/uploads'
        for fname in used_images:
            src = os.path.join(uploads_dir, fname)
            if os.path.exists(src):
                zf.write(src, arcname=f'assets/{fname}')

        # Add manifest
        manifest = {
            "site": site,
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "framework": framework,
            "files": ["index.html", "style.css"] + [f"assets/{f}" for f in used_images]
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))

    mem_zip.seek(0)
    return send_file(
        mem_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{site}.zip'
    )



def render_blocks_to_html(blocks, framework=''):

    body_html = []

    framework_cdn = {
        "bootstrap": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
        "tailwind": "https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/dist/tailwind.min.css",
        "simple": "https://cdn.jsdelivr.net/npm/simpledotcss@1.0.0/simple.min.css"
    }
    framework_link = framework_cdn.get(framework, '')
    head_extra = f'<link rel="stylesheet" href="{framework_link}">' if framework_link else ''

    for block in blocks:
        t = block.get('type')
        d = block.get('data', {})

        if t == 'header':
            body_html.append(f"<h{d['level']}>{d['text']}</h{d['level']}>")
        elif t == 'paragraph':
            body_html.append(f"<p>{d['text']}</p>")
        elif t == 'list':
            tag = 'ol' if d['style'] == 'ordered' else 'ul'
            items = ''.join(f"<li>{item}</li>" for item in d['items'])
            body_html.append(f"<{tag}>{items}</{tag}>")
        elif t == 'quote':
            body_html.append(f"<blockquote><p>{d['text']}</p><footer>— {d['caption']}</footer></blockquote>")
        elif t == 'delimiter':
            body_html.append("<hr>")
        elif t == 'image':
            img_url = f"assets/{os.path.basename(d['file']['url'])}"
            alt = d.get('caption', '')
            caption_html = f"<p style='text-align:center'>{alt}</p>" if alt else ""
            body_html.append(f"<div><img src='{img_url}' alt='{alt}' />{caption_html}</div>")

    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Exported Site</title>
    {head_extra}
    <link rel="stylesheet" href="style.css">
    </head>
    <body>
    <div class="site-preview-root">
        {''.join(body_html)}
    </div>
    </body>
    </html>"""



if __name__ == '__main__':
    app.run(debug=True, port=5050)