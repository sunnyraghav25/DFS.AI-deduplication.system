import rpyc
import hashlib
from rpyc.utils.server import ThreadedServer

class MasterServer(rpyc.Service):
    class exposed_Master():
        # Registry of Data Nodes (IP and Port)
        DN_LIST = [["127.0.0.1", 8888], ["127.0.0.1", 8000]]
        
        # In-memory storage to track file hashes for AI Deduplication
        file_metadata = {} 

        @staticmethod
        def exposed_filemap():
            """Gathers file lists from all active Data Nodes for the Dashboard"""
            filetable = []
            for DN in MasterServer.exposed_Master.DN_LIST:
                try:
                    # Establish connection with the Data Node
                    dcon = rpyc.connect(DN[0], DN[1], config={'allow_public_attrs': True})
                    
                    # Fetching the remote file list
                    remote_files = dcon.root.DNode().filequery()
                    
                    # CRITICAL FIX: Convert RPyC Network References to local Python dictionaries.
                    # This prevents '500 Internal Server Error' during JSON serialization in Flask.
                    node_files = [dict(f) for f in remote_files]
                    
                    for f in node_files:
                        # Tagging which node the file belongs to for UI clarity
                        f['Node'] = f"Node-{DN[1]}"
                        filetable.append(f)
                        
                    dcon.close() # Close connection after data retrieval
                except Exception as e:
                    print(f"[NODE OFFLINE] Port {DN[1]}: {e}")
                    continue 
            return filetable

        @staticmethod
        def exposed_put(filename, data):
            """AI Deduplication Logic: Checks if file content already exists in the cluster"""
            if not data:
                return "Error: Received empty file data"

            # Generate MD5 hash of the file content
            f_hash = hashlib.md5(data).hexdigest()
            
            # Check for existing hash (Deduplication)
            if f_hash in MasterServer.exposed_Master.file_metadata:
                return f"Deduplication Triggered: Content exists as '{MasterServer.exposed_Master.file_metadata[f_hash]}'"

            # Load Balancing: Try to store on available nodes
            for DN in MasterServer.exposed_Master.DN_LIST:
                try:
                    dcon = rpyc.connect(DN[0], DN[1], config={'allow_public_attrs': True})
                    success = dcon.root.DNode().put(filename, data)
                    dcon.close()
                    
                    if success:
                        # Update metadata after successful storage
                        MasterServer.exposed_Master.file_metadata[f_hash] = filename
                        return f"Successfully stored on Node {DN[1]}"
                except Exception as e:
                    print(f"Failed to connect to Node {DN[1]}: {e}")
                    continue
            
            return "Error: No storage nodes available"

        @staticmethod
        def exposed_delete(filename):
            """Propagates delete command to all nodes in the cluster"""
            deletion_status = False
            for DN in MasterServer.exposed_Master.DN_LIST:
                try:
                    dcon = rpyc.connect(DN[0], DN[1])
                    result = dcon.root.DNode().delete(filename)
                    dcon.close()
                    if result: deletion_status = True
                except:
                    continue
            return f"Delete command executed for: {filename}"

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("Master Server (Brain) is LIVE on Port 18812")
    print("AI Deduplication & Load Balancing: ENABLED")
    print("--------------------------------------------------")
    
    server = ThreadedServer(MasterServer, port=18812, protocol_config={'allow_public_attrs': True})
    server.start()