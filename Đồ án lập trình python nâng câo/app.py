from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Thông tin kết nối
host = "localhost"
database = "postgres"
user = "postgres"
password = "123456"

# Kết nối với cơ sở dữ liệu
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

# Tạo cursor
cur = conn.cursor()

# Tạo bảng users (nếu chưa có)
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY, 
        username TEXT, 
        email TEXT, 
        password TEXT
    )
''')

# Tạo bảng posts (nếu chưa có)
cur.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY, 
        title TEXT, 
        content TEXT, 
        user_id INTEGER, 
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()

# Trang chính
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user=session['user_name'])
    else:
        return redirect(url_for('login'))

# Đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            conn.commit()
            return redirect(url_for('login'))
        except psycopg2.Error as e:
            conn.rollback()
            error = "Error occurred while registering. Please try again."
            return render_template('register.html', error=error)

    return render_template('register.html')

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('index'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('index'))

# Tạo bài viết
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            try:
                cur.execute("INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s)", (title, content, session['user_id']))
                conn.commit()
                return redirect(url_for('index'))
            except psycopg2.Error as e:
                conn.rollback()
                error = "Error occurred while creating post. Please try again."
                return render_template('create_post.html', error=error)
        return render_template('create_post.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

# Đừng quên đóng kết nối khi ứng dụng dừng lại
@app.teardown_appcontext
def close_connection(exception):
    if conn:
        conn.close()