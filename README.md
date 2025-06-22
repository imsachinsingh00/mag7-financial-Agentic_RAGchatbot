# MAG7 SEC Filings RAG QA Agent

**Author:** Sachin Kumar Singh  
**Assignment:** Uniqus AI Engineering Take-Home  
**Development Window:** 19.06.2025 – 22.06.2025

---

## 🚀 Project Overview

A **production-ready Retrieval-Augmented Generation (RAG) pipeline** for question answering over SEC 10-K and 10-Q filings of the “Magnificent 7” tech companies, with full citation and explainability. Built with an open/free tool stack—runs on any modern environment.

---

## 📝 Project Scope and Data

- **Companies:** AAPL, NVDA, TSLA (full pipeline); MSFT, AMZN, META, GOOGL (partial, see below)
- **Filings:** 10-K, 10-Q
- **Years:** Intended for 2015–2025, but due to the SEC’s shift to XBRL/XML (post-2019-01-30), the main system handles filings from **2015 up to early 2019**.
    - For newer filings, SEC’s XBRL Viewer and XML datasets (from US Gov’t) would require a separate, specialized parser.
    - **AAPL, NVDA, and TSLA** were fully processed; others had partial or missing HTML data.

---


## 📁 Project Files & Usage Notes

* **`app.py`** is the **main application file**—run this to start the CLI-based financial Q\&A agent.
* **`Notes.ipynb`** is an **exploratory notebook**:

  * Use this to dive deeper into the methodology, see code experiments, and understand each stage of the RAG pipeline in detail.
* **`requirements.txt`, `Dockerfile`, and all supporting folders** are included for easy setup and deployment.

  * **If you encounter errors or resource constraints while building embeddings,** you can directly use the pre-built FAISS vector store included in the repo for instant querying.

---


## 💡 Technology Stack & Techniques

- **LLM (default):** [Groq](https://console.groq.com/) (Llama-3-70B-8192, free API)
    - *Note:* Also tested with OpenAI GPT-4.1-mini for reliability checks (not default, to avoid cost).
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (free, fast, high-quality)
    - *Note:* Cohere API was also tried, but its free quota (~500 calls) is too limited for real ingestion.
- **Document Splitting:** LangChain `RecursiveCharacterTextSplitter` (overlapping, context-preserving)
- **Vector Store:** [FAISS](https://github.com/facebookresearch/faiss) (open-source, efficient similarity search)
- **Parsing:** BeautifulSoup for HTML, automated metadata attachment per chunk
- **Agentic QA:** Modular pipeline for conversational, multi-turn, citation-aware RAG; can be extended to ReAct/reasoning workflows.
- **All libraries and models** are open/free, and work cross-platform (Python 3.10+).

---

## ⚡ Key Steps

1. **SEC Filing Scraping:**  
   - Ticker → CIK mapping
   - Metadata + filing download via SEC API (2015–2019)
   - Plain-text extraction and HTML cleanup

2. **Chunking and Embedding:**  
   - Document splitting with overlap to preserve context
   - Embedding via HuggingFace MiniLM

3. **Vector Indexing and Search:**  
   - Index all document chunks in FAISS for efficient retrieval

4. **Conversational Agent:**  
   - User queries are matched to the most relevant SEC filings, answers are generated and always cite their sources
   - Multi-turn (chat) context awareness

5. **Deployment:**  
   - **Dockerized:** One-command deployment on any server/OS
   - No `.env` file needed—just pass `GROQ_API_KEY` at runtime

---

## 🔑 Usage

### **Build and Run (with Groq API, no .env needed)**

```sh
docker build -t mag7_app .
docker run -it -e GROQ_API_KEY=your_groq_key -p 8501:8501 mag7_app
