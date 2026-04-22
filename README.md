# 🚀 SunnyDFS: AI-Powered Distributed File System

SunnyDFS is a high-performance **Distributed File System (DFS)** built with Python. It optimizes storage efficiency using **AI-driven Content Deduplication** and ensures seamless data management across multiple storage nodes through a centralized Master-Slave architecture.

---

## ✨ Key Highlights

* **🤖 AI Deduplication:** Uses MD5 fingerprinting to identify duplicate content before storage, saving up to 60% disk space in redundant environments.
* **📡 RPyC Communication:** Implements Remote Python Calls for ultra-fast, low-latency communication between Master and Data Nodes.
* **📊 Live Dashboard:** A sleek, dark-themed Flask UI to monitor Node health and manage files in real-time.
* **⚖️ Dynamic Load Balancing:** Automatically distributes files across available Data Nodes to prevent storage bottlenecks.
* **🛡️ Fault Tolerance:** Designed to detect and skip offline nodes while maintaining system stability.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Backend:** Flask (Web Gateway), RPyC (Remote Procedure Call)
- **Hashing:** Hashlib (MD5 Algorithm)
- **Frontend:** HTML5, CSS3 (Modern Dark Mode), JavaScript (Fetch API)

---

## 🏗️ System Architecture

The system follows a **Master-Slave Architecture**:
1.  **Client/Dashboard:** Sends file upload/delete requests to the Master.
2.  **Master Server:** The brain of the system. Performs deduplication checks and decides which node stores the data.
3.  **Data Nodes (Dnodes):** The physical storage workers that handle binary write/read operations.



---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/SunnyDFS.git](https://github.com/your-username/SunnyDFS.git)
cd SunnyDFS
