from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt', '')
    html_output = f"<html><body><h1>{prompt}</h1></body></html>"
    return jsonify({'html': html_output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
