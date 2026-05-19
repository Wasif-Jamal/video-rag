import streamlit as st

from api.client import (
    api_client,
)
from components.gallery import (
    gallery_component,
)


class ChatComponent:

    def render(self):

        st.subheader(
            "Video Chat"
        )

        query = st.text_input(
            "Ask a question"
        )

        if st.button(
            "Ask",
            use_container_width=True,
        ):

            if not query:

                st.warning(
                    "Enter a question"
                )

                return

            with st.spinner(
                "Generating answer..."
            ):

                try:

                    result = (
                        api_client
                        .chat(query)
                    )

                    st.markdown(
                        "### Answer"
                    )

                    st.write(
                        result[
                            "answer"
                        ]
                    )

                    gallery_component.render(
                        result[
                            "images"
                        ]
                    )

                except Exception as error:

                    st.error(
                        str(error)
                    )


chat_component = (
    ChatComponent()
)