from flask import Flask, request, abort, jsonify
import socket, logging

logging.basicConfig(level=logging.INFO, filename="server_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)
maked_cmds = 0
ip = '0.0.0.0'

@app.route('/')
def index():
    return """<!DOCTYPE html>
<html>
<head>
  <title>API GUI</title>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
  <h1>API GUI</h1>

  <div>
    <h3>Today maked <span id="makedCmds">0</span> commands</h3>
  </div>

  <div>
    <h3>Run Command:</h3>
    <label for="cmd">Command:</label>
    <input type="text" id="cmd" name="cmd">
    <br>
    <label for="args">Arguments:</label>
    <input type="text" id="args" name="args">
    <br>
    <button onclick="runCommand()">Run</button>
  </div>

  <div>
    <h3>Response:</h3>
    <pre id="response"></pre>
  </div>

  <script>
    const apiUrl = 'http://{ipgugu}:5000/run'; // Replace with your API URL

    function runCommand() {
      const cmd = document.getElementById('cmd').value;
      const args = document.getElementById('args').value.split(',');

      const requestData = {
        name: cmd,
        args: args
      };

      $.ajax({
        url: apiUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function(response) {
          document.getElementById('response').innerText = JSON.stringify(response, null, 2);
        },
        error: function(xhr, status, error) {
          document.getElementById('response').innerText = 'Error: ' + error;
        }
      });
    }

    // Fetch the maked_cmds value on page load
    $.ajax({
      url: '/',
      type: 'GET',
      success: function(response) {
        document.getElementById('makedCmds').innerText = response.maked_cmds;
      },
      error: function(xhr, status, error) {
        console.log('Error fetching maked_cmds:', error);
      }
    });
  </script>
</body>
</html>
""".format(ipgugu=ip)

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
    elif cmd == 'multiply':
        response = args[0] * args[1]
    elif cmd == 'execute_py':
        response = exec(args[0])
    #RETURN
    if response == None:
        code = 400
        logging.warning("Command " + cmd + " not found")
    else:
        code = 201
    maked_cmds += 1
    return jsonify({'response':response}), code

if __name__ == '__main__':
    app.run(host=ip, debug=False)
