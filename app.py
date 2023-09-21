from flask import Flask, request, abort, jsonify

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
    response = None
    if cmd == 'helloworld':
        response = 'Hello World!'
    elif cmd == 'echo':
        response = args[0]
    elif cmd == 'plus':
        response = args[0] + args[1]
    #RETURN
    if response == None:
        code = 400
    else:
        code = 201
    maked_cmds += 1
    return jsonify({'response':response}), code

if __name__ == '__main__':
    app.run(debug=True)
