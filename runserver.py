from leverageapi import create_app

app = create_app()

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
    try:
      from flask_cors import CORS
      CORS(app)
    except ImportError:
      pass
    app.run(debug=True, port=port, host=host)
