import psycopg2

# Thông tin kết nối
host = "localhost"  # Địa chỉ máy chủ
port = "5432"       # Cổng mặc định của PostgreSQL
dbname = "postgres"  # Tên cơ sở dữ liệu
user = "postgres"    # Tên người dùng
password = "123456"  # Mật khẩu

try:
    # Kết nối đến cơ sở dữ liệu
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    print("Kết nối thành công đến PostgreSQL")

    # Tạo bảng
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS my_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
    '''
    
    cursor = connection.cursor()  # Tạo cursor để thực hiện truy vấn
    cursor.execute(create_table_query)  # Thực thi câu lệnh tạo bảng
    connection.commit()  # Xác nhận thay đổi
    print("Bảng đã được tạo thành công")

    # Thêm dữ liệu vào bảng
    insert_data_query = '''
    INSERT INTO my_table (name, age) VALUES (%s, %s)
    '''
    data_to_insert = [("Alice", 30), ("huan", 25), ("Charlie", 35)]
    cursor.executemany(insert_data_query, data_to_insert)
    connection.commit()  # Xác nhận việc thêm dữ liệu
    print("Dữ liệu đã được thêm thành công")

    # Xóa dữ liệu từ bảng
    delete_query = '''
    DELETE FROM my_table WHERE name = %s
    '''
    cursor.execute(delete_query, ("Alice",))  # Xóa bản ghi có tên "huan"
    connection.commit()  # Xác nhận việc xóa dữ liệu
    print("Dữ liệu đã được xóa thành công")

    # Truy vấn dữ liệu từ bảng
    select_query = "SELECT * FROM my_table"
    cursor.execute(select_query)
    records = cursor.fetchall()  # Lấy tất cả các bản ghi

    print("Thông tin trong bảng my_table:")
    for row in records:
        print("ID:", row[0], "Name:", row[1], "Age:", row[2])

except Exception as error:
    print("Lỗi khi kết nối hoặc thao tác với bảng:", error)

finally:
    # Đảm bảo rằng kết nối được đóng lại
    if 'cursor' in locals():
        cursor.close()  # Đóng cursor
    if 'connection' in locals():
        connection.close()  # Đóng kết nối
        print("Kết nối đã được đóng")