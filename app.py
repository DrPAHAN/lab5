import os
from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            host='lab5-db',
            database=os.getenv('DB_NAME', 'labdb'),
            user=os.getenv('DB_USER', 'labuser'),
            password=os.getenv('DB_PASS', 'labpass123')
        )
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"status": "ok", "db_version": db_version}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)