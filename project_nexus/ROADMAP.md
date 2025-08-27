# Project Nexus: Subsequent Development Roadmap

This document outlines the subsequent tasks to expand Project Nexus from its current scaffolding into a fully featured, interactive learning platform.

The roadmap is divided into three main phases: **Backend Core Functionality**, **Frontend Visualization & Interaction**, and **Platform Enhancement & Content Expansion**.

---

### Phase 1: Backend Core Functionality

The goal of this phase is to build a robust backend capable of safely executing user commands and verifying the results.

1.  **Implement Python Sandbox Environment:**
    *   **Task:** Create a secure, isolated environment for executing user-submitted Python scripts (like `ddns_update.py`).
    *   **Technology Options:**
        *   **High-Isolation:** Use Docker to create ephemeral, restricted containers per user session or execution.
        *   **Lightweight:** Integrate WebAssembly-based technologies like Pyodide or JupyterLite to run Python in the browser or a lightweight backend service.

2.  **Develop Task Orchestrator:**
    *   **Task:** Build a core API service to receive instructions from the frontend, execute network commands (`dig`, `curl`, `ping`) within the sandbox, and validate the correctness of each step.
    *   **Features:**
        *   Provide API endpoints like `/api/execute/dig` or `/api/validate/dns`.
        *   Manage user progress, unlocking the next step only after successful validation.
        *   Push execution results and logs to the frontend in real-time.

3.  **Build Cloud API Proxy:**
    *   **Task:** Create a secure proxy service to forward calls to cloud provider APIs (e.g., Alibaba Cloud).
    *   **Purpose:** To avoid exposing sensitive user API keys on the frontend. All secrets will be managed securely by the backend.

---

### Phase 2: Frontend Visualization & Interaction

This phase focuses on creating an intuitive and engaging user interface that visualizes networking concepts.

1.  **Build Dynamic Network Topology Graph:**
    *   **Task:** Implement an interactive network topology graph as the central UI component.
    *   **Technology Options:** Use libraries like D3.js, Vis.js, or Cytoscape.js.
    *   **Features:**
        *   Dynamically display nodes like **[Local Device]**, **[Public Server]**, and DNS based on backend state.
        *   Update icons and connection statuses when services (like Nginx, frps) are started or stopped.

2.  **Develop Step-by-Step Mission UI:**
    *   **Task:** Convert the `README.md` guide into an interactive task list.
    *   **Features:**
        *   Each step includes clear instructions and code/config input boxes.
        *   "Execute" and "Validate" buttons that communicate with the backend Task Orchestrator.
        *   An integrated web terminal and log window to display real-time command output.

3.  **Implement Data-Flow Animation:**
    *   **Task:** Animate the flow of data on the topology graph for key operations.
    *   **Examples:**
        *   **DNS Resolution:** Animate the query path from the user to the DNS server and back to the target IP.
        *   **Nginx Proxying:** Clearly show data packets flowing from the user to the Nginx server, then through the frp tunnel to the local device.

---

### Phase 3: Platform Enhancement & Content Expansion

This phase aims to enrich the learning content and improve the overall user experience.

1.  **Add New Learning Modules:**
    *   **Task:** Design and develop new experiment modules on the established platform.
    *   **Module Ideas:**
        *   **HTTPS & Certificates:** How to secure your service with a free SSL certificate from Let's Encrypt.
        *   **Load Balancing:** Use Nginx to implement simple load balancing between two local services.
        *   **Firewall Configuration:** Learn to secure your public server using `iptables` or `ufw`.
        *   **Container Networking:** Introduction to Docker networking by containerizing the local service.

2.  **Implement User Accounts:**
    *   **Task:** Add user registration/login functionality to save progress and configurations.

3.  **Foster Community & Sharing:**
    *   **Task:** Allow users to share their successful configurations or ask questions, building a learning community around the platform.
