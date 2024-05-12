from flask import Flask, Response, request, jsonify
from datetime import timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
from Interact_with_database import *

app = Flask(__name__)
# Настройка секретного ключа для подписи токенов
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Измените на свой секретный ключ
app.config['JSON_AS_ASCII'] = False
jwt = JWTManager(app)

# Получение токена
# curl -X POST -H "Content-Type: application/json" -d '{"login": "john@example.com", "password": "pass123"}' http://127.0.0.1:8080/login
@app.route('/login', methods=['POST'])
def login():
    try:
        login = request.json.get('login', None)
        password = request.json.get('password', None)
        
        connection = connect_to_database()
        user = authenticate_user(connection, login, password)

        if user != None:
            expires = timedelta(days=3)
            access_token = create_access_token(identity=user, expires_delta=expires)
            return jsonify(access_token=access_token), 200
        
        raise
    
    except:
        res = json.dumps({'msg': 'Неверное имя пользователя или пароль'}, ensure_ascii=False).encode('utf8')
        return Response(res, status=401)    

# Регистрация в приложении
# curl -X POST -H "Content-Type: application/json" -d '{"first_name": "Alexsand", "last_name": "Polyanskiy", "email": "Alex@gmail.com", "phone_number": "999999999", "password": "12345"}' http://localhost:8080/register 
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        response = json.dumps({'error': 'No data provided'}, ensure_ascii=False).encode('utf8')
    
    connection = connect_to_database()
    result = register_user(connection, **data)

    if result:
        response = json.dumps({'message': 'Успешно'}, ensure_ascii=False).encode('utf8')
    else:
        response = json.dumps({'error': 'Пользователь с таким номером или почтой уже существует'}, ensure_ascii=False).encode('utf8')

    return Response(response=response, status=200)

# Получить уведы для пользователя
# curl -X GET http://localhost:8080/get_notifications -H 'Authorization: Bearer '
@app.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user = get_jwt_identity()
    connection = connect_to_database()
    notifications = get_notifications_by_user_id(connection, current_user['id'])
    for notif in notifications: notif['notification_time'] = str(notif['notification_time'])
    res = json.dumps(notifications, ensure_ascii=False).encode('utf8')
    return Response(res, status=200)

@app.route('/imagebyid', methods=['GET', 'POST'])
@jwt_required()
def get_image_info_by_id():
    current_user = get_jwt_identity()
    connection = connect_to_database()
    print(current_user)
    # if current_user['role_id'] == 3:
    #     data = get_image_info_by_patient_id(connection, current_user['id'])
    # elif current_user['role_id'] in [1,2] and request.method == 'POST':
    #     data = get_image_info_by_patient_id(connection, request.get_json()['patient_id'])
    # else:
    #     data = 'Что-то не так'

    data =' ds'
    data = json.dumps(data, ensure_ascii=False).encode('utf8')
    return Response(data, status=200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)