from flask import Flask, request, jsonify, render_template, send_file
import json
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import zipfile

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
    data = request.get_json()
    os.makedirs('data', exist_ok=True)
    with open('data/website_state.json', 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "saved"})

# Route: Load saved content + CSS
@app.route('/load', methods=['GET'])
def load():
    try:
        with open('data/website_state.json') as f:
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
    with open('data/website_state.json') as f:
        site_data = json.load(f)

    blocks = site_data.get('blocks', [])
    custom_css = site_data.get('css', '')

    html_content = render_blocks_to_html(blocks)

    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        zf.writestr('index.html', html_content)
        zf.writestr('style.css', custom_css or "body { font-family: sans-serif; }")

        uploads_path = 'static/uploads'
        for fname in os.listdir(uploads_path):
            fpath = os.path.join(uploads_path, fname)
            zf.write(fpath, arcname=f'assets/{fname}')

    mem_zip.seek(0)
    return send_file(mem_zip, mimetype='application/zip', as_attachment=True, download_name='website.zip')

def render_blocks_to_html(blocks):
    body_html = []
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
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>Exported Site</title>
  <link rel=\"stylesheet\" href=\"style.css\">
</head>
<body>
{''.join(body_html)}
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True, port=5050)