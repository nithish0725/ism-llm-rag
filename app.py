
import streamlit as st
import requests

st.set_page_config(
    page_title="ISM AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

API_URL = "https://nerve-costume-offshore-site.trycloudflare.com/generate"
API_KEY = "change-this-demo-key"

st.title("📚 ISM AI Study Assistant")
st.write("Ask questions about Information Storage Management.")

marks = st.selectbox(
    "Select Answer Length",
    [2, 5, 10, 12, 15, 20],
    index=2,
    format_func=lambda x: f"{x} Marks"
)

question = st.text_area(
    "Enter your question",
    placeholder="Example: Explain Business Continuity Planning."
)

context = st.text_area(
    "Study material (optional)",
    placeholder="Paste relevant content from your ISM PDFs here."
)

if st.button("Generate Answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating your answer..."):
                full_question = (
                    f"{question}\n"
                    f"Write the answer suitable for {marks} marks. "
                    "Use an appropriate level of detail."
                )

                response = requests.post(
                    API_URL,
                    headers={"x-api-key": API_KEY},
                    json={
                        "question": full_question,
                        "context": context
                    },
                    timeout=180
                )

                if response.ok:
                    st.subheader(f"Answer — {marks} Marks")
                    st.markdown(response.json()["answer"])
                else:
                    st.error(
                        f"API error ({response.status_code}): "
                        f"{response.text}"
                    )

        except requests.RequestException as e:
            st.error(f"Could not connect to Colab: {e}")
