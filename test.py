import psycopg2
from datetime import datetime, timedelta
import random

# Kết nối đến cơ sở dữ liệu PostgreSQL
conn = psycopg2.connect(
    dbname="cdc_example",
    user="minhquanhust",
    password="123987",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Tạo dữ liệu giả cho bảng transaction
def generate_fake_data():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 9, 1)
    num_records = 10000000
    num_users = 15000

    for _ in range(num_records):
        user_id = random.randint(1, num_users)
        payment = round(random.uniform(10.0, 1000.0), 2)
        time_transaction = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        # Chèn dữ liệu vào bảng
        cursor.execute("""
            INSERT INTO transaction (user_id, payment, time_transaction, age)
            VALUES (%s, %s, %s, %s);
        """, (user_id, payment, time_transaction, user_id))

        # Commit sau mỗi batch để không sử dụng quá nhiều bộ nhớ
        if _ % 1000 == 0:
            conn.commit()

    # Commit cho các bản ghi còn lại
    conn.commit()

# Gọi hàm để tạo dữ liệu
generate_fake_data()

# Đóng kết nối
cursor.close()
conn.close()
