

```markdown
# MAG7 Financial SEC Filings Q&A Agent

**Author:** Sachin Kumar Singh  
**Assignment Window:** 19.06.2025 – 22.06.2025  
**Submission:** Uniqus AI Engineering Take-Home Assignment

---

## 🚀 Project Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline for financial Q&A on SEC 10-K and 10-Q filings of the "Magnificent 7" tech companies (AAPL, NVDA, TSLA). The system scrapes filings, extracts and chunks their text, creates semantic embeddings, and answers user queries via a conversational agent.

**Current Status:**  
- Supports filings from 2015–2019 (inclusive), limited by SEC's migration to XBRL after 2019-01-30.
- Works fully for Apple, Nvidia, and Tesla. (Data issues for other MAG7 stocks noted.)
- Uses OpenAI (GPT) for Q&A. Code structure allows easy addition of Groq, Gemini, Claude, or other LLMs in future.

---

## 🏗️ Tech Stack

- **Python 3.10+**
- **LangChain** for agentic pipeline, document loaders, and vector search
- **BeautifulSoup4** for HTML parsing
- **HuggingFace** `all-MiniLM-L6-v2` model for document embeddings (free)
- **FAISS** for vector storage and retrieval (free)
- **OpenAI GPT** (via API key) for LLM Q&A (free/demo tier used)
- **Docker** for reproducible deployment

---

## 📦 Directory Structure

```

.
├── app.py                 # Main application (CLI or web)
├── filings/               # Downloaded SEC filings (HTML)
├── mag7\_filing\_metadata.json # Metadata for filings
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container build instructions
├── .env.example           # Example environment config (no secrets)
├── README.md              # This file
└── (output/, models/, etc. as needed)

````

---

## ⚡ Usage

### 1. **Clone and Setup**
```sh
git clone <your-repo-url>
cd mag7-financial-Agentic_RAGchatbot
````

### 2. **Add API Keys**

* Copy `.env.example` to `.env`
* Add your OpenAI API key:

  ```
  OPENAI_API_KEY=sk-...
  ```

### 3. **Build and Run with Docker**

```sh
make setup && make run
# or, manually:
docker build -t mag7_app .
docker run -it --env-file .env -p 8501:8501 mag7_app
```

### 4. **Interact**

* If CLI: type your questions at the prompt
* If web: open [http://localhost:8501](http://localhost:8501) (if using Streamlit)

---

## 🔑 LLMs & Extensibility

* **Current:** Uses OpenAI GPT for Q\&A (cheapest/free plan).
* **Extensible:** Codebase is structured to easily swap to or add support for [Groq](https://console.groq.com/), [Google Gemini](https://makersuite.google.com/app/apikey), or [Anthropic Claude](https://console.anthropic.com/account/keys) using their free tiers—simply add the key to `.env` and update the LLM provider in `app.py`.

---

## ⚠️ Known Limitations

* Data after 2019-01-30 is XBRL-only and not parsed by this pipeline.
* Some MAG7 stocks (MSFT, AMZN, META, GOOGL) had incomplete or missing filings in the available range.

---

## 🧑‍💻 Developer Notes

* All major libraries are open-source and work in any Linux/Mac/Python 3.10+ environment.
* FAISS and all embeddings are free (no paid tier needed).
* OpenAI is used only for Q\&A (can run locally for embedding/search).
* All code is containerized for easy reproduction and review.

---

## 🚀 Next Steps (Future Work)

* Add support for Groq, Gemini, Claude, and other open/free LLM APIs.
* Extend parser for XBRL filings (post-2018 SEC format).
* Add a web front-end (e.g., Streamlit, Gradio) for broader usability.

---

## 📄 License

For academic review/demo only.
No proprietary or sensitive data included.

---

**Questions?**
Contact: Sachin Kumar Singh

```
