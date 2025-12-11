
# EX2 — Application Layer Lab (Network Programming)

A robust implementation of a custom Application Layer protocol using TCP Sockets in Python.
This project demonstrates Client-Server architecture, Transparent Proxying, Caching mechanisms (LRU), and integration with Generative AI APIs.

## 🚀 Key Features

### 1. Advanced TCP Server (`server.py`)
* **Persistent Connections:** Supports handling multiple requests from the same client without closing the socket (Keep-Alive approach).
* **Scientific Calculator:** A secure, expanded math evaluator (`safe_eval_expr`) supporting:
    * Trigonometry (`sin`, `cos`, `tan`)
    * Logarithms & Powers (`log`, `pow`, `sqrt`)
    * Constants (`pi`, `e`)
    * **Security:** Input length validation and specific error handling (DivisionByZero, SyntaxError) to prevent DoS.
* **Generative AI Integration:** Replaced the default stub with **Google Gemini AI** (via `google.generativeai`) for real-time responses to text prompts.
* **LRU Cache:** Caches results to optimize performance and reduce API costs.

### 2. Smart Proxy (`proxy.py`)
* **Transparent Proxying:** Intercepts traffic between client and server.
* **Local Caching:** Implements an LRU cache. If a request is found in the proxy's cache, it returns the response immediately without contacting the server ("Cache Hit").
* **Robust Buffering:** Properly handles TCP stream fragmentation to ensure full JSON messages are received before processing.
* **Resilience:** Can serve cached responses even if the main server is offline.

### 3. Interactive Client (`client.py`)
* **Modes:** Supports both One-Shot (single command) and Interactive Shell mode.
* **Protocol:** Communicates using line-delimited JSON.

---

## 🛠️ Installation & Setup

1.  **Clone the repository**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key (Optional for AI):**
    To enable the Google Gemini AI features, create a `.env` file in the root directory and add your key:
    ```env
    GOOGLE_API_KEY=your_actual_google_api_key_here
    ```
    *(Note: If no key is provided, the server will print a warning but the calculator mode will still work.)*

---

## 🏃‍♂️ Usage Guide

### 1. Run the Server
Starts the server on port 5555.
```bash
python server.py --host 127.0.0.1 --port 5555
````

### 2\. Run the Proxy (Optional)

Starts the proxy on port 5554, forwarding to server on 5555.

```bash
python proxy.py --listen-port 5554 --server-port 5555
```

### 3\. Run the Client

#### Option A: Interactive Mode (Recommended)

Connects and keeps the session open for multiple queries.

```bash
python client.py --host 127.0.0.1 --port 5555
# Or connect to proxy:
python client.py --host 127.0.0.1 --port 5554
```

#### Option B: One-Shot Command

**Math Calculation:**

```bash
python client.py --host 127.0.0.1 --port 5555 --mode calc --expr "pow(2, 10) + sqrt(100)"
```

**AI Prompt:**

```bash
python client.py --host 127.0.0.1 --port 5555 --mode gpt --prompt "Explain TCP vs UDP in one sentence"
```

-----

## 📡 Protocol Specification

The communication is based on **Line-Delimited JSON**.

**Request (Client -\> Server):**

```json
{
  "mode": "calc", 
  "data": { "expr": "1+1" }, 
  "options": { "cache": true }
}
```

**Response (Server -\> Client):**

```json
{
  "ok": true, 
  "result": 2, 
  "meta": { "from_cache": false, "took_ms": 1 }
}
```

-----

## 🧪 Testing

Run the smoke test to verify basic functionality:

```bash
python tests/test_smoke.py
```

```
```
