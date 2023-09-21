from flask import Flask, request, abort, jsonify
import socket, logging

logging.basicConfig(level=logging.INFO, filename="server_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)
maked_cmds = 0

@app.route('/')
def index():
    return f"""<title>Sapbot Command Services</title>
<p>Today maked {maked_cmds} commands</p>"""

@app.route('/run', methods=['POST'])
def run_command():
    global maked_cmds
    if not request.json or not 'name' in request.json:
        abort(400)
    elif not request.json or not 'args' in request.json:
        abort(400)
    #RUN
    cmd = request.json["name"]
    args = request.json["args"]
    logging.info("Running command " + cmd)
    response = None
    if cmd == 'helloworld':
        response = 'Hello World!'
    elif cmd == 'echo':
        response = args[0]
    elif cmd == 'plus':
        response = args[0] + args[1]
    elif cmd == 'get_maked':
        response = maked_cmds
    elif cmd == 'fibonacci':
        i = 0
        n = args[0]
        fib1 = 1
        fib2 = 1
        while i < n - 2:
            fib_sum = fib1 + fib2
            fib1 = fib2
            fib2 = fib_sum
            i = i + 1
        response = fib2
    #RETURN
    if response == None:
        code = 400
        logging.warning("Command " + cmd + " not found")
    else:
        code = 201
    maked_cmds += 1
    return jsonify({'response':response}), code

if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()), debug=False)
