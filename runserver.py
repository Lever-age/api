from leverageapi import create_app
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == "__main__":
    import sys
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 5000
    try:
        host = sys.argv[2]
    except (IndexError, ValueError):
        host = '127.0.0.1'
    app.run(debug=True, port=port, host=host)
