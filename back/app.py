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

        inserted_id = cursor.lastrowid

        return {'status': 'success', 'inserted_id': inserted_id}

    except Error as e:
        print(f"Error: {e}")
        return {'status': 'error', 'message': 'DB insert failed'}
    
    finally:
        # cursor, DB 안전하게 닫기
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

# Theme 목록
@app.route('/themeList', methods=['POST'])
def themeList():
    query = """
        SELECT theme
        FROM tb_theme
        order by id
    """
    response = tbSelect(query)
    return jsonify(response)  # 반환 값을 JSON으로 변환하여 반환

# Theme 적용
@app.route('/Theme', methods=['POST'])
def Theme():
    data = request.json
    user_id_temp = data.get('user_id')

    query = """
        SELECT t.url
        FROM tb_user_detail d
        LEFT JOIN tb_theme t ON d.theme_id = t.id
        where user_id = %s
    """

    if not user_id_temp:
        user_id = 10
        query = """
            SELECT url
            FROM tb_theme
            where id = %s
        """
    else:
        user_id = user_id_temp
        query = """
            SELECT t.url
            FROM tb_user_detail d
            LEFT JOIN tb_theme t ON d.theme_id = t.id
            where user_id = %s
        """

    response = tbSelect(query,(user_id,))
    return jsonify(response)  # 반환 값을 JSON으로 변환하여 반환

# User 마다 Theme 셋팅
@app.route('/selectTheme', methods=['POST'])
def selectTheme():
    data = request.json
    user_id = data.get('user_id')
    theme_id = data.get('theme_id')

    if not user_id or not theme_id:
        return jsonify({'status': 'error', 'message': 'theme_id, user_id required'}), 400

    query = "UPDATE tb_user_detail set theme_id = %s where user_id = %s"
    response = tbInsert(query, (theme_id, user_id))
    
    return jsonify(response)

@app.route('/userList', methods=['GET'])
def userList():

    page = int(request.args.get('page', 1))  # 기본값으로 페이지 1
    per_page = int(request.args.get('per_page', 10))  # 기본값으로 페이지당 10개 게시글

    query = """
        SELECT * 
        FROM tb_user u, tb_user_detail d 
        WHERE u.id = d.user_id
    """
    params = []
    
    # 페이징을 위한 LIMIT 및 OFFSET 추가
    query += " order by u.id desc LIMIT %s OFFSET %s"
    offset = (page - 1) * per_page
    params.extend([per_page, offset])
    
    # tbSelect 함수 호출
    response = tbSelect(query, params)

    return jsonify(response)


@app.route('/userListPage', methods=['GET'])
def userListPage():
    query = """
        SELECT COUNT(*) AS total_photos
        FROM tb_user u, tb_user_detail d 
        WHERE u.id = d.user_id
    """

    # tbSelect 함수 호출
    result = tbSelect(query)

    return jsonify(result)



@app.route('/profileLoad', methods=['POST'])
def profileLoad():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'status': 'error', 'message': 'user_id required'}), 400

    query = """
        SELECT * 
        FROM tb_user u, tb_user_detail d 
        WHERE u.id = d.user_id
        AND u.id =  %s
    """
    response = tbSelect(query,(user_id,))
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

        query = "INSERT INTO tb_user_detail (user_id ) VALUES (%s)"
        response = tbInsert(query, (response['inserted_id'],))
    
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
    birth = data.get('user_birth')
    gender = data.get('user_gender')
    addr = data.get('user_addr')
    intro = data.get('user_intro')

    if not img_name:
        return jsonify({'status': 'error', 'message': 'img_name required'}), 400

    # 첫 번째 쿼리 (tb_user 테이블 업데이트)
    query1 = "UPDATE tb_user SET img = %s, name = %s WHERE id = %s"
    # 두 번째 쿼리 (tb_user_detail 테이블 업데이트)
    query2 = "UPDATE tb_user_detail SET birth = %s, gender = %s, addr = %s, intro = %s WHERE user_id = %s"

    try:
        # 첫 번째 쿼리 실행
        response1 = tbInsert(query1, (img_name, name, user_id))
        
        # 두 번째 쿼리 실행
        response2 = tbInsert(query2, (birth, gender, addr, intro, user_id))
        
        # 응답 반환
        if response1['status'] == 'success' and response2['status'] == 'success':
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Update failed'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'Update failed', 'details': str(e)}), 500

    
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
            c.id as category_id,
            c.name AS category_name,
            u.id AS user_id,
            u.name AS user_username,
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
        where p.is_set='Y'
    """
    
    params = []
    
    # category_id가 있을 경우에만 WHERE 절 추가
    if category_id != '0':
        query += " And p.category_id = %s"
        params.append(category_id)
    
    # 페이징을 위한 LIMIT 및 OFFSET 추가
    query += " order by create_date desc LIMIT %s OFFSET %s"
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
        where is_set='Y'
    """
    params = []
    
    # category_id가 있을 경우에만 WHERE 절 추가
    if category_id != '0':
        query += " And category_id = %s"
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

@app.route('/boardPosttingEdit',methods=['POST'])
def boardPosttingEdit():
    data = request.json
    board_id = data.get('board_id')
    content = data.get('content')
    title = data.get('title')
    category_id = data.get('category')
    user_id = data.get('user_id')

    if not content or not title or not category_id or not user_id:
        return jsonify({'status': 'error', 'message': 'content, title, category_id, user_id required'}), 400

    query = """
        update tb_board set 
            category_id = %s, 
            title = %s,
            content = %s, 
            user_id = %s
        where id = %s
    """

    response = tbInsert(query, (category_id, title, content, user_id, board_id))

    return jsonify(response)

@app.route('/boardViewCnt',methods=['GET'])
def boardViewCnt():
    board_id = request.args.get('board_id')
    user_id = request.args.get('user_id')

    if not board_id or not user_id :
        return jsonify({'status': 'error', 'message': 'board_id, user_id required'}), 400

    query = """
        INSERT INTO tb_board_view (board_id, user_id ) VALUES (%s, %s)
    """
    response = tbInsert(query, (board_id, user_id))

    return jsonify(response)


@app.route('/commentList', methods=['GET'])
def commentList():
    board_id = request.args.get('board_id')

    if not board_id:
        return jsonify({'status': 'error', 'message': 'board_id required'}), 400

    query = """
        SELECT 
                m.id,
                m.user_id,
                m.content,
                m.create_date,
                u.name,
                u.img
        FROM tb_board_comment m
        JOIN tb_user u ON m.user_id = u.id
        WHERE m.board_id = %s 
            AND m.is_set = 'Y'
        order BY m.create_date
    """
    # tbSelect 함수 호출
    result = tbSelect(query, (board_id,))

    return jsonify(result)

@app.route('/commentAdd',methods=['GET'])
def commentAdd():
    board_id = request.args.get('board_id')
    user_id = request.args.get('user_id')
    comment = request.args.get('comment')

    if not board_id or not user_id or not comment:
        return jsonify({'status': 'error', 'message': 'board_id, user_id, comment required'}), 400

    query = """
        INSERT INTO tb_board_comment (board_id, user_id, content ) VALUES (%s, %s, %s)
    """
    # tbInsert 함수 호출
    result = tbInsert(query, (board_id, user_id, comment))

    return jsonify(result)

  
@app.route('/commentDelete', methods=['POST'])
def commentDelete():
    data = request.json
    comment_id = data.get('comment_id')

    if not comment_id:
        return jsonify({'status': 'error', 'message': 'comment_id required'}), 400

    query = """
        update tb_board_comment set is_set = 'N', update_date = NOW() where id = %s
    """
    # tbInsert 함수 호출
    result = tbInsert(query, (comment_id,))

    return jsonify(result)

@app.route('/saveCommentEdit', methods=['POST'])
def saveCommentEdit():
    data = request.json
    comment_id = data.get('comment_id')
    comment = data.get('content')

    if not comment_id or not comment:
        return jsonify({'status': 'error', 'message': 'comment_id, comment required'}), 400

    query = """
        update tb_board_comment set content = %s, update_date = NOW() where id = %s
    """
    # tbInsert 함수 호출
    result = tbInsert(query, (comment, comment_id,))

    return jsonify(result)

@app.route('/deleteBoard', methods=['POST'])
def deleteBoard():
    data = request.json
    board_id = data.get('board_id')

    if not board_id:
        return jsonify({'status': 'error', 'message': 'board_id required'}), 400

    query = """
        update tb_board set is_set = 'N', update_date = NOW() where id = %s
    """
    # tbInsert 함수 호출
    result = tbInsert(query, (board_id,))

    return jsonify(result)


@app.route('/Best', methods=['POST'])
def Best():
    query = '''SELECT 	b.id,
                        b.title,
                        b.create_date,
                        u.name,
                        u.img,
                        c.name as category_name,
                        (SELECT COUNT(*) 
                        FROM tb_board_view v 
                        WHERE b.id = v.board_id) AS view_cnt,
                        (SELECT COUNT(*) 
                        FROM tb_board_comment cm 
                        WHERE b.id = cm.board_id) AS comment_cnt
            FROM tb_board b
            LEFT JOIN tb_user u ON b.user_id = u.id
            LEFT JOIN tb_board_category c ON b.category_id = c.id 
            ORDER BY view_cnt DESC LIMIT 5;
            '''
    response = tbSelect(query)
    print(response)
    return jsonify(response)

@app.route('/todayBest', methods=['POST'])
def todayBest():
    query = '''SELECT 	b.id,
                        b.title,
                        b.create_date,
                        u.name,
                        u.img,
                        c.name as category_name,
                        (SELECT COUNT(*) 
                        FROM tb_board_view v 
                        WHERE b.id = v.board_id) AS view_cnt,
                        (SELECT COUNT(*) 
                        FROM tb_board_comment cm 
                        WHERE b.id = cm.board_id) AS comment_cnt
            FROM tb_board b
            LEFT JOIN tb_user u ON b.user_id = u.id
            LEFT JOIN tb_board_category c ON b.category_id = c.id 
            WHERE DATE(b.create_date) = "2024-08-21"
            ORDER BY view_cnt DESC LIMIT 5;
            ;
            '''
    response = tbSelect(query)
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
