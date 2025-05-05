from flask import Flask, request, jsonify
from flask_cors import CORS

responses = {}
app = Flask(__name__)
CORS(app)

@app.route("/check-response", methods=["GET"])
def check_response():
    phone = request.args.get("phone")
    status = responses.get(phone)
    print(f"[CHECK] phone: {phone}, status: {status}")
    return jsonify({"status": status or "waiting"})

@app.route("/set-response", methods=["POST"])
def set_response():
    data = request.json
    phone = data.get("phone")
    result = data.get("result")
    responses[phone] = result
    print(f"[SET] phone: {phone}, result: {result}")
    return jsonify({"success": True})

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

    
