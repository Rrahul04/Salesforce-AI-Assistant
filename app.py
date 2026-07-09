import streamlit as st
import requests
import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/ask"
)

CLEAR_CACHE_URL = API_URL.replace(
    "/ask",
    "/clear-cache"
)
st.set_page_config(
    page_title="Salesforce AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Custom CSS ---------------- #

st.markdown("""
<style>

.block-container{
    max-width:1100px;
    padding-top:2rem;
}

h1{
    color:#16325c;
}

.stTextInput input{
    border-radius:12px;
}

div.stButton > button{
    width:100%;
    height:48px;
    border-radius:12px;
    background:#4F9CF9;
    color:white;
    border:none;
    font-size:16px;
    font-weight:600;
    transition:0.2s;
}

div.stButton > button:hover{
    background:#2B7DE9;
    color:white;
}

.answer-card{
    background:white;
    padding:28px;
    border-radius:18px;
    border:1px solid #E6E8EC;
    box-shadow:0px 4px 14px rgba(0,0,0,0.08);
    margin-bottom:10px;
}

.source-card{
    background:#F8F9FB;
    padding:16px;
    border-radius:10px;
    border:1px solid #E6E8EC;
    margin-bottom:15px;
}

.footer{
    color:gray;
    text-align:center;
    margin-top:40px;
}
.quick-card{
    background:#EEF6FF;
    border:1px solid #D8EAFE;
    border-radius:12px;
    padding:14px;
    text-align:center;
    font-weight:600;
    color:#16325C;
    margin-bottom:12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.markdown("---")

    st.subheader("Tech Stack")

    st.markdown("""
- 🧠 Gemini 2.5 Flash
- 🔍 ChromaDB
- ⚡ Redis Cache
- 🚀 FastAPI
- 🎨 Streamlit
- 🐳 Docker
""")

    st.markdown("---")

    st.subheader("Knowledge Base")

    st.info("📄 96 Knowledge Chunks")

    st.markdown("---")

    if st.button("🗑 Clear Redis Cache"):

        
        response = requests.post(CLEAR_CACHE_URL)
        

        if response.status_code == 200:
            st.success("Redis Cache Cleared!")

# ---------------- Header ---------------- #

st.markdown("""
<h1 style='margin-bottom:0px;color:#16325C;'>
🤖 Salesforce AI Assistant
</h1>
""", unsafe_allow_html=True)

st.markdown(
"""
<div style="
font-size:18px;
color:#6b7280;
margin-bottom:30px;">
Enterprise RAG powered by Gemini • ChromaDB • Redis • FastAPI
</div>
""",
unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("##### Knowledge Base")
    st.markdown("## 96 Chunks")

with c2:
    st.markdown("##### Model")
    st.markdown("## Gemini 2.5")

with c3:
    st.markdown("##### Cache")
    st.markdown("## Redis")
#st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

# ---------------- Question ---------------- #

question = st.text_input(
    "",
    placeholder="💬 Ask anything about Salesforce...",
    key="question"
)
left, center, right = st.columns([1.5,2,1.5])

with center:
    ask = st.button(
        "🚀 Ask AI",
        use_container_width=True
    )


if ask:
    question = st.session_state.question
    if question.strip():

        try:

            with st.spinner("Searching knowledge base..."):

                response = requests.post(
                API_URL,
                json={"question": question},
                timeout=30)

            if response.status_code == 200:

                data = response.json()

                st.markdown("## 🤖 AI Response")

                st.markdown(
    f"""
<div class="answer-card">

<p style="
font-size:18px;
line-height:1.8;
margin:0;
color:#2F3B52;">
{data["answer"]}
</p>

</div>
""",
    unsafe_allow_html=True
)

                st.write("")

                status_col,time_col=st.columns([5,1])

                with status_col:

                    st.markdown("### ⚙ Status")

                    if data["cached"]:

                        st.success("⚡ Served from Redis Cache")

                    else:

                          st.info("🧠 Generated using Gemini + RAG")

                with time_col:
                    st.write("")
                    st.write("")

                    st.metric(
                            "⏱ Response Time",
                        f'{data["time_taken"]} sec'
                    )

                st.write("")

                with st.expander("📚 Retrieved Sources"):

                    if len(data["sources"]) == 0:

                        st.info(
                            "No sources returned (response came from cache).")

                    else:

                        import re

                        for source in data["sources"]:

                            filename = source["source"]
                            filename = filename.replace(".txt", "")
                            filename = re.sub(r"^\d+_", "", filename)
                            filename = filename.replace("_", " ")

                            with st.container(border=True):
                                st.markdown(f"#### 📄 {filename}")
                                st.write(source["content"])
                        

            else:

                st.error(
                    response.json().get(
                        "detail",
                        "Something went wrong."
                    )
                )
    
        except requests.exceptions.Timeout:

            st.error(
                "The request timed out."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI."
            )

        except Exception as e:

            st.error(str(e))

    else:

        st.warning("Please enter a question.")
st.markdown("## 💡 Popular Questions")

col1, col2, col3 = st.columns(3)

with col1:

    st.info("⚡ Governor Limits")

    st.info("📦 Batch Apex")

with col2:

    st.info("🚀 Queueable Apex")

    st.info("🔍 SOQL vs SOSL")

with col3:

    st.info("⚙ Apex Triggers")

    st.info("🖥 LWC Lifecycle")

