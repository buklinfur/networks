from flask import Flask, request, jsonify
import psycopg2

from parse import parse
app = Flask(__name__)

DB_USER = 'postgres'
DB_PASSWORD = '21222005'
DB_NAME = 'servers_db'
DB_HOST = 'localhost'
DB_PORT = '5432'


def get_db_connection():
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,

        host=DB_HOST,
        port=DB_PORT
    )


@app.route('/parse')
def parse_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        parsed_data = parse(url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        for item in parsed_data:
            cur.execute(
                "INSERT INTO servers "
                "(rank, name, address, current_online, max_online, status) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (item[0], item[1], item[2], item[3], item[4], item[5])
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Data parsed and saved successfully'}), 200


@app.route('/data')
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT "
                    "rank, name, address, current_online, max_online, status "
                    "FROM servers")
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({
                'rank': row[0],
                'name': row[1],
                'address': row[2],
                'current_online': row[3],
                'max_online': row[4],
                'status': row[5]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
