import streamlit as st
from dotenv import load_dotenv

from app.utils.pdf_utils import get_pdf_text
from app.utils.text_utils import get_text_chunks
from app.utils.embeddings_utils import get_vector_store
from app.utils.conversation_utils import get_conversation_chain, handle_user_input
from app.html.htmlTemplates import css


def submit():
    st.session_state.ask = st.session_state.widget
    st.session_state.widget = ''


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with your documents", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header(":page_facing_up: Chat with your CONTENT")

    if 'ask' not in st.session_state:
        st.session_state.ask = ''

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

    st.text_input("Ask", key='widget', on_change=submit, placeholder="Ask..", label_visibility="hidden")
    user_input = st.session_state.ask

    if user_input:
        handle_user_input(user_input)
        st.session_state.ask = user_input

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'process'", accept_multiple_files=True)

        process_button = st.button("Process")

        if process_button and pdf_docs:
            # Check if the uploaded files are PDFs
            pdf_files = [f.name for f in pdf_docs]
            non_pdf_files = [filename for filename in pdf_files if not filename.endswith(".pdf")]

            if non_pdf_files:
                st.error(f"The following files are not PDFs: {', '.join(non_pdf_files)}")

            else:
                with st.spinner("Processing"):
                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create a vector store
                    vectorstore = get_vector_store(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
