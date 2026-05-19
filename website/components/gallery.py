import streamlit as st


class GalleryComponent:

    def render(
        self,
        images: list,
    ):

        if not images:

            return

        st.subheader(
            "Retrieved Frames"
        )

        columns = st.columns(3)

        for (
            index,
            image,
        ) in enumerate(images):

            column = columns[
                index % 3
            ]

            with column:

                st.image(
                    image[
                        "image_path"
                    ],
                    use_container_width=True,
                )


gallery_component = (
    GalleryComponent()
)