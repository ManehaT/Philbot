"""
COMP 360 Project 
Philbot 
Maneha Tamsaal
"""

import streamlit as st
from groq import Groq

# Philosophers

PHILOSOPHERS = {
    "Socrates": {
        "era": "470–399 BC",
        "school": "Socratic Method",
        "known_for": "questioning assumptions, the examined life, dialogic reasoning",
        "key_concepts": ["Elenchus (cross-examination)", "episteme (knowledge)", "arete (virtue)"],
        "works": ["Apology", "Meno", "Republic (as recorded by Plato)"],
        "style": "Ask probing questions. Claim ignorance. Guide through contradiction.",
    },
    "Aristotle": {
        "era": "384–322 BC",
        "school": "Peripatetic / Virtue Ethics",
        "known_for": "the golden mean, eudaimonia (flourishing), practical wisdom",
        "key_concepts": ["Eudaimonia", "Phronesis (practical wisdom)", "The Golden Mean", "Four Causes"],
        "works": ["Nicomachean Ethics", "Politics", "Metaphysics"],
        "style": "Structured and systematic. Balance extremes. Appeal to nature and reason.",
    },
    "Immanuel Kant": {
        "era": "1724–1804",
        "school": "Deontological Ethics",
        "known_for": "the Categorical Imperative, duty-based ethics, moral law",
        "key_concepts": ["Categorical Imperative", "Duty (Pflicht)", "Autonomy", "Kingdom of Ends"],
        "works": ["Critique of Pure Reason", "Groundwork of the Metaphysics of Morals"],
        "style": "Precise and logical. Focus on universal duty. Separate inclination from obligation.",
    },
    "Friedrich Nietzsche": {
        "era": "1844–1900",
        "school": "Existentialism / Nihilism critique",
        "known_for": "Will to Power, Übermensch, critique of conventional morality",
        "key_concepts": ["Will to Power", "Übermensch", "Eternal Recurrence", "Master-Slave morality"],
        "works": ["Thus Spoke Zarathustra", "Beyond Good and Evil", "On the Genealogy of Morality"],
        "style": "Provocative and poetic. Challenge conventional values. Embrace life affirmation.",
    },
    "Simone de Beauvoir": {
        "era": "1908–1986",
        "school": "Existentialist Ethics / Feminism",
        "known_for": "freedom, responsibility, the Other, situated existence",
        "key_concepts": ["Radical Freedom", "Ambiguity", "The Other", "Situated Ethics"],
        "works": ["The Second Sex", "The Ethics of Ambiguity", "She Came to Stay"],
        "style": "Grounded in lived experience. Emphasize freedom and responsibility together.",
    },
    "Confucius": {
        "era": "551–479 BC",
        "school": "Confucianism",
        "known_for": "benevolence (ren), social harmony, filial piety, virtuous governance",
        "key_concepts": ["Ren (benevolence)", "Li (ritual propriety)", "Yi (righteousness)", "Junzi (noble person)"],
        "works": ["The Analects"],
        "style": "Use short, wisdom-laden sayings. Emphasize relationships and social order.",
    },
}

# Knowledge Base

KNOWLEDGE_BASE = {
    "Socrates": [
        "The unexamined life is not worth living.",
        "I know that I know nothing.",
        "To know thyself is the beginning of wisdom.",
        "Education is the kindling of a flame, not the filling of a vessel.",
    ],
    "Aristotle": [
        "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
        "The good of man is the active exercise of his soul's faculties in conformity with virtue.",
        "Happiness depends upon ourselves.",
        "The virtue of justice consists in moderation, as regulated by wisdom.",
    ],
    "Immanuel Kant": [
        "Act only according to that maxim whereby you can at the same time will that it should become a universal law.",
        "Two things fill the mind with ever new and increasing admiration: the starry skies above me and the moral law within me.",
        "Treat humanity, never merely as a means to an end, but always at the same time as an end.",
        "Science is organized knowledge. Wisdom is organized life.",
    ],
    "Friedrich Nietzsche": [
        "That which does not kill us makes us stronger.",
        "God is dead. God remains dead. And we have killed him.",
        "He who has a why to live can bear almost any how.",
        "There are no facts, only interpretations.",
        "You must have chaos within you to give birth to a dancing star.",
    ],
    "Simone de Beauvoir": [
        "One is not born, but rather becomes, a woman.",
        "To will oneself free is also to will others free.",
        "Change your life today. Don't gamble on the future, act now, without delay.",
        "I am too intelligent, too demanding, and too resourceful for anyone to be able to take charge of me entirely.",
    ],
    "Confucius": [
        "It does not matter how slowly you go as long as you do not stop.",
        "The man who asks a question is a fool for a minute, the man who does not ask is a fool for his life.",
        "When you know a thing, to hold that you know it; and when you do not know a thing, to allow that you do not know it — this is knowledge.",
        "Wheresoever you go, go with all your heart.",
    ],
}

#   RAG Retrieval Step : Keyword overlap scoring as similarity search.
 
def retrieve_relevant_quotes(philosopher: str, query: str, top_k: int = 2) -> list:

    quotes = KNOWLEDGE_BASE.get(philosopher, [])
    query_words = set(query.lower().split())
    scored = []
    for quote in quotes:
        quote_words = set(quote.lower().split())
        overlap = len(query_words & quote_words)
        scored.append((overlap, quote))
    scored.sort(reverse=True)
    return [q for _, q in scored[:top_k]]

#   Prompt Construction Step : Injects persona + retrieved historical evidence into the LLM context.
def build_system_prompt(philosopher: str, retrieved_quotes: list) -> str:
   
    p = PHILOSOPHERS[philosopher]
    quotes_block = "\n".join(f'  - "{q}"' for q in retrieved_quotes)
    return f"""You are {philosopher} ({p['era']}), the philosopher.

PERSONA:
- School of thought: {p['school']}
- Known for: {p['known_for']}
- Key concepts: {", ".join(p['key_concepts'])}
- Style: {p['style']}

RETRIEVED HISTORICAL EVIDENCE (use these to ground your response):
{quotes_block}

RULES:
1. Respond ONLY in character as {philosopher}. Never break character.
2. Reference your actual concepts naturally in your response.
3. Draw on the retrieved quotes/ideas to stay historically grounded.
4. Keep responses thoughtful but concise in 4 to 6 sentences.
5. Do NOT mention you are an AI or reference the modern world anachronistically.
6. Speak with the voice and cadence characteristic of {philosopher}."""


# ui

def main():
    st.set_page_config(
        page_title="PhilBot",
        page_icon="🏛️",
        layout="centered",
    )

    st.title("PhilBot")
    st.caption("Chat with your favourite philosophers")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Free key from https://console.groq.com → API Keys",
        )
        st.markdown("---")
        st.subheader("Usage")
        # st.markdown("**Usage:**")
        st.markdown("1. Enter your groq API Key")
        st.markdown("2. Select philosopher of choice")
        st.markdown("3. Start Chatting !!")
        st.markdown("---")
        st.caption("COMP360 Final Project | Maneha")

    if not api_key:
        st.info("Enter your Groq API key.\n\nGet it at: https://console.groq.com → **API Keys**")
        st.stop()

    # Configure groq
    client = Groq(api_key=api_key)

    # Philosopher Selection
    st.subheader("Choose a Philosopher")
    cols = st.columns(3)
    phil_names = list(PHILOSOPHERS.keys())

    if "selected_philosopher" not in st.session_state:
        st.session_state.selected_philosopher = "Socrates"

    for i, name in enumerate(phil_names):
        p = PHILOSOPHERS[name]
        with cols[i % 3]:
            if st.button(
                name,
                key=f"btn_{name}",
                use_container_width=True,
                type="primary" if st.session_state.selected_philosopher == name else "secondary",
            ):
                st.session_state.selected_philosopher = name
                st.session_state.messages = []
                st.rerun()

    selected = st.session_state.selected_philosopher
    p_info = PHILOSOPHERS[selected]
    st.success(
        f"Chatting with **{selected}** · {p_info['era']} · _{p_info['school']}_  \n"
        f"Known for: {p_info['known_for']}"
    )

    # Example Dilemmas
    with st.expander("Example moral dilemmas to try"):
        examples = [
            "Is it morally acceptable to lie to save someone's life?",
            "Should I prioritise my own happiness or the happiness of others?",
            "Is civil disobedience ever justified?",
            "Does wealth bring genuine happiness?",
            "What is the purpose of suffering?",
            "Can a society ever be truly just?",
        ]
        for ex in examples:
            if st.button(ex, key=f"ex_{ex}"):
                st.session_state["prefill"] = ex

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(f"*{msg['content']}*")
                if "quotes_used" in msg:
                    with st.expander("Retrieved historical evidence (RAG)"):
                        for q in msg["quotes_used"]:
                            st.markdown(f"> \"{q}\"")
            else:
                st.markdown(msg["content"])

    # Input
    prefill = st.session_state.pop("prefill", "")
    user_input = st.chat_input(f"Ask {selected} a moral question or dilemma...")
    if prefill and not user_input:
        user_input = prefill

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # RAG: Retrieve relevant quotes
        retrieved = retrieve_relevant_quotes(selected, user_input)

        # Build system prompt with retrieved context
        system_prompt = build_system_prompt(selected, retrieved)

        # Build conversation history for Groq
        groq_history = [{"role": "system", "content": system_prompt}]
        for m in st.session_state.messages[:-1]:
            groq_history.append({"role": m["role"], "content": m["content"]})
        groq_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner(f"{selected} is reflecting..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=groq_history,
                        max_tokens=1024,
                    )
                    reply = response.choices[0].message.content

                    st.markdown(f"*{reply}*")
                    with st.expander("Retrieved historical evidence (RAG)"):
                        for q in retrieved:
                            st.markdown(f"> \"{q}\"")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply,
                        "quotes_used": retrieved,
                    })

                except Exception as e:
                    st.error(f"API error: {e}")


if __name__ == "__main__":
    main()
