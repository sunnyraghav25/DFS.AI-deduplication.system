import os
import rpyc
from rpyc.utils.server import ThreadedServer

# --- CONFIGURATION ---
IP = "127.0.0.1"
PORT = 8888
# EXACT PATH: This is where files will be physically stored on your PC
STORAGE_PATH = os.path.dirname(os.path.abspath(__file__))

# Create folder if it doesn't exist
if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

class DNServer(rpyc.Service):
    class exposed_DNode():
        @staticmethod
        def exposed_filequery():
            """Returns metadata of all files for the Dashboard"""
            filelist = []
            try:
                if os.path.exists(STORAGE_PATH):
                    for filename in os.listdir(STORAGE_PATH):
                        file_path = os.path.join(STORAGE_PATH, filename)
                        filelist.append({
                            "Name": filename,
                            "Size": os.path.getsize(file_path),
                            "Status": "Active",
                            "Node": "DNode1 (8888)"
                        })
                return filelist
            except Exception as e:
                print(f"Error scanning directory: {e}")
                return []

        @staticmethod
        def exposed_put(filename, data):
            """Saves the uploaded file to the physical C: drive"""
            try:
                full_destination = os.path.join(STORAGE_PATH, filename)
                with open(full_destination, 'wb') as f:
                    f.write(data)
                print(f"\n[SUCCESS] File physically saved at: {full_destination}")
                return True
            except Exception as e:
                print(f"\n[ERROR] Failed to save file: {e}")
                return False

        @staticmethod
        def exposed_delete(filename):
            """Removes file from the C: drive"""
            try:
                full_path = os.path.join(STORAGE_PATH, filename)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    print(f"[DELETE] Removed: {filename}")
                    return True
                return False
            except Exception as e:
                return False

if __name__ == "__main__":
    print(f"DNode-1 is LIVE on {IP}:{PORT}")
    print(f"Storage Location: {STORAGE_PATH}")
    server = ThreadedServer(DNServer, port=PORT, protocol_config={'allow_public_attrs': True})
    server.start()