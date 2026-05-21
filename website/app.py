import uuid

import streamlit as st

from components.chat import (
    chat_component,
)
from components.ingestion import (
    ingestion_component,
)


class VideoRAGApp:

    def configure_page(self):

        st.set_page_config(
            page_title="Video RAG",
            layout="wide",
        )

    def initialize_session(self):

        if (
            "session_id"
            not in st.session_state
        ):

            st.session_state.session_id = (
                str(uuid.uuid4())
            )

    def render(self):

        self.configure_page()

        self.initialize_session()

        st.title(
            "Multimodal Video RAG"
        )

        tab1, tab2 = st.tabs(
            [
                "Ingestion",
                "Chat",
            ]
        )

        with tab1:

            ingestion_component.render()

        with tab2:

            chat_component.render()


app = VideoRAGApp()

app.render()