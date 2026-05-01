from flask import Flask
from travel import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host='127.0.0.181',port=5001)