from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# In-memory site state for all sections
site_state = {}

# Route: Serve the editor UI
@app.route("/")
def index():
    return render_template("index.html")

# Route: Receive updates from frontend
@app.route("/update", methods=["POST"])
def update_section():
    data = request.get_json()
    section_id = data.get("id")
    new_content = data.get("content")

    if not section_id or not new_content:
        return jsonify({"error": "Missing id or content"}), 400

    # Save content to state
    site_state[section_id] = new_content

    print(f"[UPDATE] {section_id}: {new_content[:50]}...")  # Trim for console
    return jsonify({"html": new_content})

# Route: Return current saved state
@app.route("/state")
def get_state():
    return jsonify(site_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
