from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# MariaDB 데이터베이스 연결 설정
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='mlind',
            password='123',
            database='mlind',
            port=3306
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# SELECT 쿼리 실행 함수
def tbSelect(query, params=None):
    # DB 연결
    connection = get_db_connection()
    if connection is None:
        return {'status': 'error', 'message': 'DB connection failed'}
        
    try:
        # cursor 생성 및 실행
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        res = cursor.fetchall()

        if res:
            response = {'status': 'success', 'res': res}
        else:
            response = {'status': 'error', 'message': 'No data found'}
        return response

    except Error as e:
        print(f"Error: {e}")
        return {'status': 'error', 'message': 'DB query failed'}
    
    finally:
        # cursor, DB 안전하게 닫기
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# INSERT 쿼리 실행 함수
def tbInsert(query, params):
    # DB 연결
    connection = get_db_connection()
    if connection is None:
        return {'status': 'error', 'message': 'DB connection failed'}

    try:
        # cursor 생성 및 실행
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return {'status': 'success'}

    except Error as e:
        print(f"Error: {e}")
        return {'status': 'error', 'message': 'DB insert failed'}
    
    finally:
        # cursor, DB 안전하게 닫기
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route('/Theme', methods=['GET'])
def Theme():
    query = "SELECT * FROM tb_Theme WHERE theme = 'Minty'"
    response = tbSelect(query)
    return jsonify(response)  # 반환 값을 JSON으로 변환하여 반환

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('loginID')
    user_pw = data.get('loginPW')

    if not user_id or not user_pw:
        return jsonify({'status': 'error', 'message': 'ID, PW required'}), 400

    # DB 쿼리
    query = "SELECT * FROM tb_user WHERE user_id = %s AND user_pw = %s"
    response = tbSelect(query, (user_id, user_pw))

    if response['status'] == 'success' and response['res']:
        user = response['res'][0]
        response = {'status': 'success', 'user_id': user['id'], 'user_name': user['name'], 'user_img': user['img']}
    elif response['status'] == 'success':
        response = {'status': 'error', 'message': 'Invalid ID or password'}
    return jsonify(response)

@app.route('/signUp', methods=['POST'])
def signUp():
    data = request.json
    user_id = data.get('signUpID')
    user_pw = data.get('signUpPW')
    user_name = data.get('signUpName')

    if not user_id or not user_pw or not user_name:
        return jsonify({'status': 'error', 'message': 'ID, PW, Name required'}), 400

    # Check if user ID already exists
    query = "SELECT * FROM tb_user WHERE user_id = %s"
    response = tbSelect(query, (user_id,))

    if response['status'] == 'success' and response['res']:
        response = {'status': 'error', 'message': 'User ID already exists'}
    else:
        # Insert new user
        query = "INSERT INTO tb_user (user_id, user_pw, name ) VALUES (%s, %s, %s)"
        response = tbInsert(query, (user_id, user_pw, user_name))
    
    return jsonify(response)

# @app.route('/profileload', methods=['POST'])
# def profileload():
#     data = request.json
#     user_id = data.get('user_id')

#     if not user_id :
#         return jsonify({'status': 'error', 'message': 'user_id required'}), 400

#     # Check if user ID already exists
#     query = "SELECT * FROM tb_user WHERE user_id = %s"
#     response = tbSelect(query, (user_id,))

#     return jsonify(response)

@app.route('/UploadFile', methods=['POST'])
def UploadFile():
    # 파일 크기 제한 (16MB)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    
    if file:
        # 파일 저장 경로 설정
        upload_folder = '../front/src/assets/img'
        os.makedirs(upload_folder, exist_ok=True)
        
        filename = file.filename
        file_path = os.path.join(upload_folder, filename)
        
        # 파일 저장
        file.save(file_path)
        
        # 이미지 품질 조절
        with Image.open(file_path) as img:
            # 이미지가 RGBA 모드일 경우 RGB 모드로 변환
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            # 이미지 품질 낮추기
            img.save(file_path, format='JPEG', quality=75)
        
        return jsonify({'success': True, 'filename': filename})
    
    return jsonify({'success': False, 'message': 'File upload failed'})



@app.route('/profileChange', methods=['POST'])
def profileChange():
    data = request.json
    img_name = data.get('img_name')
    user_id = data.get('user_id')
    name = data.get('user_name')


    if not img_name:
        return jsonify({'status': 'error', 'message': 'img_name required'}), 400

    query = "UPDATE tb_user set img = %s, name = %s where user_id = %s"
    response = tbInsert(query, (img_name, name, user_id))
    
    return jsonify(response)

@app.route('/pwChange', methods=['POST'])
def pwChange():
    data = request.json
    user_id = data.get('user_id')
    user_pw = data.get('user_pw')


    if not user_pw or not user_id:
        return jsonify({'status': 'error', 'message': 'user_pw, user_id required'}), 400

    query = "UPDATE tb_user set user_pw = %s where user_id = %s"
    response = tbInsert(query, (user_pw, user_id))
    
    return jsonify(response)


@app.route('/category', methods=['GET'])
def category():
    query = "SELECT * FROM tb_board_category order by id"
    response = tbSelect(query)
    return jsonify(response)  # 반환 값을 JSON으로 변환하여 반환

@app.route('/boardList', methods=['GET'])
def boardList():
    category_id = request.args.get('category_id')
    page = int(request.args.get('page', 1))  # 기본값으로 페이지 1
    per_page = int(request.args.get('per_page', 10))  # 기본값으로 페이지당 10개 게시글
    
    if not category_id:
        return jsonify({'status': 'error', 'message': 'category_id required'}), 400
    
    # 기본 쿼리 작성
    query = """
        SELECT
            p.id AS board_id,
            p.title,
            p.content,
            p.create_date AS create_date,
            p.update_date AS update_date,
            c.name AS category_name,
            u.id AS user_id,
            u.user_id AS user_username,
            COALESCE(view_count.view_count, 0) AS view_count,
            COALESCE(comment_counts.comment_count, 0) AS comment_count
        FROM
            tb_board p
        JOIN
            tb_board_category c ON p.category_id = c.id
        JOIN
            tb_user u ON p.user_id = u.id
        LEFT JOIN
            (
                SELECT
                    board_id,
                    COUNT(*) AS view_count
                FROM
                    tb_board_view
                GROUP BY
                    board_id
            ) view_count ON p.id = view_count.board_id
        LEFT JOIN (
            SELECT
                board_id,
                COUNT(*) AS comment_count
            FROM
                tb_board_comment
            WHERE
                is_set = 'Y'
            GROUP BY
                board_id
        ) comment_counts ON p.id = comment_counts.board_id
    """
    
    params = []
    
    # category_id가 있을 경우에만 WHERE 절 추가
    if category_id != '0':
        query += " WHERE p.category_id = %s"
        params.append(category_id)
    
    # 페이징을 위한 LIMIT 및 OFFSET 추가
    query += " LIMIT %s OFFSET %s"
    offset = (page - 1) * per_page
    params.extend([per_page, offset])
    
    # tbSelect 함수 호출
    posts = tbSelect(query, params)

    return jsonify(posts)

@app.route('/boardListPage', methods=['GET'])
def boardListPage():
    category_id = request.args.get('category_id')

    if not category_id:
        return jsonify({'status': 'error', 'message': 'category_id required'}), 400

    query = """
        SELECT COUNT(*) AS total_posts
        FROM tb_board
    """
    params = []
    
    # category_id가 있을 경우에만 WHERE 절 추가
    if category_id != '0':
        query += " WHERE category_id = %s"
        params.append(category_id)
    
    # tbSelect 함수 호출
    result = tbSelect(query, params)

    return jsonify(result)


@app.route('/boardPostting',methods=['POST'])
def boardPostting():
    data = request.json
    content = data.get('content')
    title = data.get('title')
    category_id = data.get('category')
    user_id = data.get('user_id')

    if not content or not title or not category_id or not user_id:
        return jsonify({'status': 'error', 'message': 'content, title, category_id, user_id required'}), 400

    query = """
        INSERT INTO tb_board (category_id, title, content, user_id) VALUES (%s, %s, %s, %s)
    """

    response = tbInsert(query, (category_id, title, content, user_id))

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
