import os
import rpyc
from rpyc.utils.server import ThreadedServer

# --- CONFIGURATION ---
IP = "127.0.0.1"
PORT = 8000
# EXACT PATH: Separate folder for the second node
STORAGE_PATH = os.path.dirname(os.path.abspath(__file__))


if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

class DNServer(rpyc.Service):
    class exposed_DNode():
        @staticmethod
        def exposed_filequery():
            """Gathers file list for Dashboard refresh"""
            filelist = []
            try:
                if os.path.exists(STORAGE_PATH):
                    for filename in os.listdir(STORAGE_PATH):
                        file_path = os.path.join(STORAGE_PATH, filename)
                        filelist.append({
                            "Name": filename,
                            "Size": os.path.getsize(file_path),
                            "Status": "Active",
                            "Node": "DNode2 (8000)"
                        })
                return filelist
            except Exception as e:
                return []

        @staticmethod
        def exposed_put(filename, data):
            """Saves binary data to DNode2 storage"""
            try:
                full_destination = os.path.join(STORAGE_PATH, filename)
                with open(full_destination, 'wb') as f:
                    f.write(data)
                print(f"\n[SUCCESS] File physically saved at: {full_destination}")
                return True
            except Exception as e:
                return False

        @staticmethod
        def exposed_delete(filename):
            """Permanent deletion from DNode2"""
            try:
                full_path = os.path.join(STORAGE_PATH, filename)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    return True
                return False
            except Exception as e:
                return False

if __name__ == "__main__":
    print(f"DNode-2 is LIVE on {IP}:{PORT}")
    print(f"Storage Location: {STORAGE_PATH}")
    server = ThreadedServer(DNServer, port=PORT, protocol_config={'allow_public_attrs': True})
    server.start()