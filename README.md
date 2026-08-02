# PhilBot — AI Philosophical Chatbot
**COMP360 Final Project | Maneha Tamsaal | Spring 2026**

---

## What is PhilBot?

PhilBot is a conversational AI agent that lets users discuss moral dilemmas or just have normal everyday conversations with  historical philosophers. It uses **Prompt Engineering + Retrieval-Augmented Generation (RAG)** to ensure each philosopher's response is grounded in their actual texts and ideas.

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Groq API Key

Sign up at https://console.groq.com/keys and create an API key.

### 3. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

### 4. Use the app

1. Enter your API key in the sidebar
2. Select a philosopher
3. Type a moral dilemma or question
4. The philosopher responds in their authentic voice, with retrieved historical quotes shown

---

## Project Architecture

```
User Question
     │
     ▼
Vector Embedding (semantic encoding)
     │
     ▼
Similarity Search → Knowledge Base (philosophical quotes)
     │
     ▼
Retrieved Quotes (top-k (2) relevant passages)
     │
     ▼
Prompt Construction (persona + retrieved evidence injected)
     │
     ▼
LLM Synthesis (Claude via Anthropic API)
     │
     ▼
Philosopher Dialogue Response
```

---

## Philosophers Included

| Philosopher | Era | School |
|---|---|---|
| Socrates | 470–399 BC | Socratic Method |
| Aristotle | 384–322 BC | Virtue Ethics |
| Immanuel Kant | 1724–1804 | Deontological Ethics |
| Friedrich Nietzsche | 1844–1900 | Existentialism |
| Simone de Beauvoir | 1908–1986 | Existentialist Feminism |
| Confucius | 551–479 BC | Confucianism |

---

## Dataset Sources

- **Project Gutenberg** — public domain philosophical texts (https://www.gutenberg.org)
- **EthicsNet / Moral Machine** — structured moral dilemma datasets
- **UNESCO AI Ethics Recommendation** — framework reference

The `KNOWLEDGE_BASE` in `app.py` contains verified quotes from each philosopher's published works. In a production system, this would be replaced by a full vector database (e.g., ChromaDB or FAISS) with embeddings from `text-embedding-3-small`.

---

## AI Technique Justification

| Technique | Why Used |
|---|---|
| **Prompt Engineering (Persona)** | Forces the LLM to stay in character using historical context |
| **RAG (Retrieval)** | Grounds responses in verified historical texts, reduces hallucination |
| **Multi-turn Memory** | Maintains conversation history for coherent dialogue |

---

## Limitations

- Knowledge base is small (simplified RAG); a full vector DB would improve retrieval
- Philosophers cannot hold views beyond their historical era
- Nuance of full philosophical texts is compressed into short responses

---

## File Structure

```
philbot/
├── app.py              ← Main application (Streamlit + RAG logic)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## AI Assistance Disclosure

Per given guidelines: Anthropic Claude was used to assist with clarity in communication and debugging. All code, design decisions, philosophical content, and project architecture are my original work.
