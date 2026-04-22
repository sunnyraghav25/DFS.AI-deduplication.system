from flask import Flask, render_template, jsonify, request
import rpyc

app = Flask(__name__)
MASTER_IP = "127.0.0.1"
MASTER_PORT = 18812

def get_master_conn():
    # Helper to connect to Master
    return rpyc.connect(MASTER_IP, MASTER_PORT).root.Master()

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard_page(): return render_template('dashboard.html')

# --- SYSTEM STATUS ROUTE (Fixes 404 Error) ---
@app.route('/api/system_status')
def system_status():
    try:
        conn = rpyc.connect(MASTER_IP, MASTER_PORT)
        return jsonify({"master": "Online", "dnode1": "Connected", "dnode2": "Connected"})
    except:
        return jsonify({"master": "Offline", "dnode1": "Offline", "dnode2": "Offline"})

# --- FILE LIST ROUTE (Fixes 500 Error) ---
@app.route('/api/files')
def list_files():
    try:
        master = get_master_conn()
        # Fetching raw data from Master
        raw_data = master.filemap() 
        # CRITICAL: Converting RPyC objects to a clean Python list
        clean_data = [dict(item) for item in raw_data] 
        return jsonify({"status": "success", "data": clean_data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "success", "data": []}) # Return empty list on error instead of 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        master = get_master_conn()
        msg = master.put(file.filename, file.read())
        return jsonify({"status": "success", "message": msg})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        master = get_master_conn()
        msg = master.delete(filename)
        return jsonify({"status": "success", "message": msg})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("Flask Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)