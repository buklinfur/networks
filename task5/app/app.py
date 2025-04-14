from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


DB_CONFIG = {
    "dbname": "url_db",
    "user": "docker_user",
    "password": "docker_password",
    "host": "db",
    "port": "5432"
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.route('/parse')
def save_url():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO urls (url) VALUES (%s)", (url,))
        conn.commit()
        return jsonify({'message': 'URL saved successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/data')
def get_urls():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, url FROM urls")
        urls = [{'id': row[0], 'url': row[1]} for row in cur.fetchall()]
        return jsonify(urls)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
