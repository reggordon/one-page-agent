from flask import Flask, request, render_template_string, redirect, url_for
from backend.main import build_page
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            return "⚠️ Please enter a prompt.", 400
        build_page(prompt)
        return redirect(url_for("preview"))

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>One-Pager Generator</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="p-8 font-sans bg-gray-100">
        <div class="max-w-2xl mx-auto bg-white p-6 rounded shadow">
            <h1 class="text-2xl font-bold mb-4">Generate a One-Pager</h1>
            <form method="POST">
                <textarea name="prompt" rows="5" class="w-full border p-2 rounded mb-4" placeholder="Describe your page..."></textarea>
                <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Generate</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route("/preview")
def preview():
    output_path = "frontend/output.html"
    if not os.path.exists(output_path):
        return "⚠️ No output file found. Please submit a prompt first.", 404

    with open(output_path, "r") as f:
        content = f.read()

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Generated One-Pager</title>
    </head>
    <body class="bg-gray-50 font-sans">
        {content}
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
