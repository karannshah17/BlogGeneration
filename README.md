# BlogGeneration

> **FastAPI + Graph-Orchestrated LLM for Multilingual Blog Generation**

BlogGeneration is a **FastAPI web API** that generates entire blog posts—title, detailed content, and optional translation—using a **graph-based Large Language Model (LLM) pipeline**.

Provide a **topic** and (optionally) a **target language**, and the service orchestrates a series of LLM-powered nodes to produce a polished, multilingual blog.

---

## ✨ Features

* 🌍 **Multilingual Output** – Generate blogs in English by default or automatically translate into languages such as German, French.
* 🧠 **LLM-Powered** – Uses a Groq-backed LLM (via `GroqLLM`) for all steps:

  * **Title Creation** – SEO-friendly, creative blog title
  * **Content Generation** – At least 2000 characters of in-depth, insightful content
  * **Translation** – Accurate translation into the requested language with cultural adaptation
* ⚡ **Graph-Based Workflow** – A modular architecture built on:

  * `graphs/` – Orchestrates nodes into topic or language-specific pipelines
  * `nodes/` – Encapsulates each processing step (e.g., `GenerateBlog`)
  * `state/` – Manages data shared between nodes
  * `llms/` – LLM integrations and abstractions
* 🔗 **FastAPI REST API** – Single endpoint (`POST /generate_blog`) for easy integration with front-ends or CMSs.

---

## 📂 Project Structure

```
BlogGeneration/
├── app.py                    # FastAPI application
├── src/
│   ├── graphs/
│   │   └── GraphBuilder.py   # Builds topic & language graphs
│   ├── llms/
│   │   └── llm.py            # GroqLLM wrapper
│   ├── nodes/
│   │   └── generateblog.py   # GenerateBlog node: Title, Content, Translation, Routing
│   ├── state/
│   │   └── state.py          # State model (includes Blog dataclass)
│   └── __init__.py
├── requirements.txt
├── .env                       # Environment variables (API keys)
└── README.md
```

---

## ⚙️ Node Logic (`GenerateBlog`)

The **`GenerateBlog`** class (`src/nodes/generateblog.py`) contains the core logic:

* **TitleCreation**
  Generates a **single, SEO-optimized blog title** based on the provided topic.

* **ContentCreation**
  Produces **at least 2000 characters** of detailed blog content.

* **Translation**
  Translates the generated blog into the requested language, returning **JSON only**:

```json
{
  "title": "<translated title>",
  "content": "<translated content>"
}
```

* **Routing (`route`, `route_decision`)**
  Determines which language-specific path to follow (German, French, etc.).

---

## 🛠️ Getting Started

### Prerequisites

* **Python 3.9+**
* Git
* API keys:

  * `LANGCHAIN_API_KEY` (used as `LANGSMITH_API_KEY` internally)
  * Any keys required by `GroqLLM` for LLM access

### Installation

```bash
git clone https://github.com/karannshah17/BlogGeneration.git
cd BlogGeneration

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
LANGCHAIN_API_KEY=your_langchain_key
GROQ_API_KEY=your_groq_key        # if required by GroqLLM
```

`app.py` automatically loads these using `python-dotenv`.

---

## ▶️ Running the FastAPI Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📝 API Usage

### Endpoint

`POST /generate_blog`

### Request Body

```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "language": "German"
}
```

| Field    | Type   | Required | Description                               |
| -------- | ------ | -------- | ----------------------------------------- |
| topic    | string | ✅        | Blog topic or headline                    |
| language | string | ❌        | Target output language (default: English) |

### Behavior

* If **language** is provided → uses the *language graph* to **translate** after content generation.
* If only **topic** is provided → uses the *topic graph* (English output).

### Example Response

```json
{
  "title": "Künstliche Intelligenz im Gesundheitswesen",
  "content": "Künstliche Intelligenz (KI) transformiert das Gesundheitswesen..."
}
```

---

## 🔗 Example `curl` Request

```bash
curl -X POST "http://127.0.0.1:8000/generate_blog" \
     -H "Content-Type: applic
```
