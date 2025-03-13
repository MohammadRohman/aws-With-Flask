from flask import Flask, request, jsonify, render_template
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Agar API bisa diakses dari frontend

# Konfigurasi koneksi ke PostgreSQL di AWS
DB_CONFIG = {
    "host": "database-1.ctcessy8wp74.ap-southeast-2.rds.amazonaws.com",  # Ganti dengan endpoint RDS
    "port": "5432",
    "database": "postgres",  # Ganti dengan nama database
    "user": "testingAWS",  # Ganti dengan username PostgreSQL
    "password": "Moris0404"  # Ganti dengan password PostgreSQL
}

# Fungsi untuk membuat koneksi ke database
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Buat tabel jika belum ada
def initialize_db():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Database initialization error:", e)

# Jalankan fungsi inisialisasi sebelum server mulai
with app.app_context():
    initialize_db()

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        nama = data.get("nama")
        email = data.get("email")

        if not nama or not email:
            return jsonify({"error": "Nama dan Email harus diisi"}), 400

        conn = connect_db()
        cur = conn.cursor()

        # Masukkan data ke dalam tabel users
        cur.execute("INSERT INTO users (nama, email) VALUES (%s, %s)", (nama, email))
        conn.commit()
        
        cur.close()
        conn.close()

        return jsonify({"message": "Data berhasil disimpan!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
