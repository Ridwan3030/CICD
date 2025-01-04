from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='database',
        user='root',
        password='examplepassword',
        database='mydb'
    )
    return connection

@app.route('/products')
def products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
