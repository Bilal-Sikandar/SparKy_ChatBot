import streamlit as st
from streamlit.components.v1 import html
import requests

# ----- CONFIG -----
st.set_page_config(
    page_title="Sparky - Your Personal AI Assistant",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----- CSS -----
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ----- Chat History -----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----- HEADER -----
st.markdown("""
    <h1 style="text-align: center; font-family: 'Times New Roman', serif; font-weight: bold;">
        ⚡ Sparky — Your Personal AI Assistant
    </h1>
    <h3 style="text-align: center; font-family: 'Times New Roman', serif;">
        AI Assistant Built with 💡 by an AI Intern @ Code Alpha.
    </h3>
""", unsafe_allow_html=True)

# ----- Show Past Messages -----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----- Get User Prompt -----
if prompt := st.chat_input("Ask Sparky anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ----- Build Request -----
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://sparky.streamlit.app",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        "stream": False
    }

    # ----- Show Assistant Reply -----
    with st.chat_message("assistant"):
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error("⚠️ Sparky couldn't reply. Try again later.")
        except Exception as e:
            st.error(f"⚠️ API Error: {e}")

# ----- Wobble Send Button Animation -----
html("""
<script>
document.addEventListener('DOMContentLoaded', (event) => {
    const input = document.querySelector('.stChatInputContainer input');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const button = document.querySelector('.stChatInputContainer button');
                if (button) {
                    button.classList.add('wobble');
                    setTimeout(() => button.classList.remove('wobble'), 500);
                }
            }
        });
    }
});
</script>
""")
