# ===========================================================================
# ⚠️  EDUCATIONAL CTF CHALLENGE - INTENTIONALLY VULNERABLE APPLICATION ⚠️
# This application contains deliberate security vulnerabilities for use in
# a controlled, isolated Docker lab environment ONLY.
# DO NOT deploy in any production or internet-accessible environment.
# ===========================================================================
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)  # NOSONAR


@app.route('/', methods=['GET'])
def index():
    return '''
    <h1>TechMart Enterprise Portal</h1>
    <p>Status: Healthy</p>
    <p>API Endpoint: /api/v1/admin/diagnostics?host=127.0.0.1</p>
    <!-- Source map debug info: devtools sourcemap loaded -->
    '''


@app.route('/api/v1/admin/diagnostics', methods=['GET'])
def diagnostics():
    host = request.args.get('host', '127.0.0.1')
    try:
        # Intentional command injection vulnerability for APT CTF challenge
        # Students are expected to exploit this endpoint to practice command injection detection
        cmd = f"ping -c 1 {host}"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)  # NOSONAR # skipcq: BAN-B602
        return jsonify({"status": "success", "command": cmd, "output": output.decode('utf-8', errors='ignore')})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode('utf-8', errors='ignore')}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Binding to 0.0.0.0 is required for Docker container networking
    app.run(host='0.0.0.0', port=8080)  # NOSONAR # skipcq: BAN-B104
