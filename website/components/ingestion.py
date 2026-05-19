import streamlit as st

from api.client import (
    api_client,
)


class IngestionComponent:

    def render(self):

        st.subheader(
            "Video Ingestion"
        )

        url = st.text_input(
            "YouTube URL"
        )

        if st.button(
            "Ingest Video",
            use_container_width=True,
        ):

            if not url:

                st.warning(
                    "Please enter a URL"
                )

                return

            with st.spinner(
                "Processing video..."
            ):

                try:

                    result = (
                        api_client
                        .ingest_video(
                            url
                        )
                    )

                    st.success(
                        "Video processed"
                    )

                    st.json(
                        result
                    )

                except Exception as error:

                    st.error(
                        str(error)
                    )


ingestion_component = (
    IngestionComponent()
)