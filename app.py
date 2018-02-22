import sys
from flask import Flask, send_from_directory
from flask import request

from controller import Controller

app = Flask(__name__)

if len(sys.argv) < 3:
    print("Usage: sudo python3.6 app.py ttyACM1 ttyACM0")
else:
    slave1_name = sys.argv[1]
    slave2_name = sys.argv[2]

    controller = Controller((slave1_name, 9600), (slave2_name, 9601))
    controller.listen()


    @app.route('/api/execute', methods=['POST'])
    def execute_command():
        command = request.data.decode('ascii')
        controller.execute(command)
        return ''


    @app.route('/')
    def root():
        with open('index.html', 'r') as f:
            return '\n'.join(f.readlines())


    @app.route('/images/<path:path>')
    def send_image(path):
        return send_from_directory('images', path)


    app.run(host='0.0.0.0', port=80)
