import os
import json
# Import LangChain modules (community versions as per latest best practices)
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

# Set up directory and embeddings for vector search
OUTPUT_DIR = "output"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# to add you own embedding use ipython notebook, copy the commented code from there

# Load FAISS vector store for document retrieval
try:
    vector_store = FAISS.load_local(
        os.path.join(OUTPUT_DIR, 'faiss_mag7'),
        embeddings,
        allow_dangerous_deserialization=True
    )
except Exception as e:
    print("Error: Could not load vector store. Please follow README setup instructions.")
    print(e)
    exit(1)


#  Define the output schema (answer, sources, confidence) for structured responses
answer_schema = ResponseSchema(
    name="answer",
    description="The final answer to the user's question, with step-by-step reasoning if needed."
)
sources_schema = ResponseSchema(
    name="sources",
    description="A list of dicts with keys: company, filing, period, snippet, url, showing where info came from."
)
confidence_schema = ResponseSchema(
    name="confidence",
    description="A float between 0 and 1 expressing confidence in the answer."
)
output_parser = StructuredOutputParser.from_response_schemas(
    [answer_schema, sources_schema, confidence_schema]
)

# Create the LLM prompt template with clear instructions
prompt_template = PromptTemplate(
    input_variables=["chat_history", "context", "query"],
    template="""You are a financial Q&A AI agent for the Magnificent 7 (AAPL, MSFT, AMZN, GOOGL, META, NVDA, TSLA).
Your instructions:
- Accept and answer all user queries, including complex, comparative, or trend questions.
- Auto-correct obvious typos (e.g., 'Q1 20218' → 'Q1 2018'). If unsure, clarify.
- Use the chat history to interpret follow-ups.
- Only answer using the provided context (from SEC filings); never guess or hallucinate data.
- For comparative, trend, or multi-step queries, reason step by step in the 'answer' field.
- Always cite your sources in a list of dicts with company, filing, period, snippet, and url.
- If context is missing, state so clearly.
- Output ONLY valid JSON with these fields: answer, sources, confidence.

{format_instructions}

Chat history:
{chat_history}

Context from SEC filings:
{context}

User question: {query}
""",
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)

# Set up the LLM (uses OpenAI GPT-4 Mini, but you can change the model)
# Make sure OPENAI_API_KEY is set in your environment (or .env file)!
model = ChatOpenAI(model="gpt-4.1-mini")  # Or your OpenAI API/model

# In-memory chat history for context-aware dialogue (multi-turn support)
chat_history = []

def conversational_get_answer(query, k=5, snippet_len=500):
    # Step 1: Retrieve top-k relevant document chunks from the vector store
    hits = vector_store.similarity_search(query, k=k)
    context = "\n".join([hit.page_content[:snippet_len] for hit in hits])
    # Step 2: Prepare sources metadata for citations
    sources = []
    for hit in hits:
        meta = hit.metadata.copy()
        sources.append({
            "company": meta.get("company"),
            "filing": meta.get("form"),
            "period": meta.get("date") or meta.get("year"),
            "snippet": hit.page_content[:snippet_len],
            "url": meta.get("url", meta.get("source"))
        })
        
    # Step 3: Build chat history for prompt (for follow-ups)
    chat_history_str = ""
    for q, a in chat_history[-6:]:
        chat_history_str += f"User: {q}\nAgent: {a}\n"
    
    # Step 4: Compose the prompt for the LLM
    prompt = prompt_template.format(
        chat_history=chat_history_str,
        context=context,
        query=query,
    )
    # Step 5: Get model output and parse as structured JSON
    raw_output = model.invoke(prompt)
    if hasattr(raw_output, "content"):
        raw_output = raw_output.content
    try:
        parsed = output_parser.parse(raw_output)
        if not parsed.get("sources"):
            parsed["sources"] = sources
        # Convert confidence to float if needed
        parsed["confidence"] = float(parsed.get("confidence", 0.85))
    except Exception:
        parsed = {"answer": raw_output, "sources": sources, "confidence": 0.7}

    # Step 6: Update chat history for future context
    chat_history.append((query, parsed["answer"]))
    return parsed

# Command-line interface loop
if __name__ == "__main__":
    print("🔷 MAG7 Conversational Agent (multi-turn, typo-tolerant, step-by-step). Type 'exit' to quit.\n")
    while True:
        user_query = input("User: ")
        if user_query.strip().lower() in ["exit", "quit"]:
            break
        print(f"\nUser: {user_query}\n")
        print("System: Searching relevant sections from 10-K/Q filings...\n")
        response = conversational_get_answer(user_query)
        print("Response:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("\n---\n")
