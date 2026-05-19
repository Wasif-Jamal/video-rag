from uuid import uuid4

from llama_index.core.schema import (
    ImageNode,
    TextNode,
)

from app.config.log_config import LogConfig
from app.schema.node_schema import MultimodalNodeResponse
from app.utils.node_utils import (
    group_frames_by_time_window,
)

logger = LogConfig.get_logger(__name__)


class NodeBuilderService:

    def build_nodes(
        self,
        transcript_segments: list,
        frames: list,
        video_id: str,
        window_size: int = 15,
    ):

        logger.info(
            f"Building multimodal nodes "
            f"for {video_id}"
        )

        text_nodes = []
        image_nodes = []

        grouped_frames = (
            group_frames_by_time_window(
                frames=frames,
                window_size=window_size,
            )
        )

        transcript_windows = {}

        # Group transcript text
        for segment in transcript_segments:

            start_time = int(
                segment.start
            )

            window_start = (
                start_time
                // window_size
            ) * window_size

            if (
                window_start
                not in transcript_windows
            ):
                transcript_windows[
                    window_start
                ] = []

            transcript_windows[
                window_start
            ].append(
                segment.text
            )

        # Build nodes
        for (
            window_start,
            texts,
        ) in transcript_windows.items():

            combined_text = " ".join(
                texts
            )

            related_frames = (
                grouped_frames.get(
                    window_start,
                    [],
                )
            )

            frame_paths = [
                frame[
                    "frame_path"
                ]
                for frame in related_frames
            ]

            node_id = str(uuid4())

            text_node = TextNode(
                id_=node_id,
                text=combined_text,
                metadata={
                    "video_id": video_id,
                    "start_time": (
                        window_start
                    ),
                    "end_time": (
                        window_start
                        + window_size
                    ),
                    "frame_paths": (
                        frame_paths
                    ),
                },
            )

            text_nodes.append(
                text_node
            )

            # Create image nodes
            for frame_path in (
                frame_paths
            ):

                image_node = ImageNode(
                    id_=str(uuid4()),
                    image_path=frame_path,
                    metadata={
                        "video_id": (
                            video_id
                        ),
                        "related_text_node": (
                            node_id
                        ),
                        "window_start": (
                            window_start
                        ),
                    },
                )

                image_nodes.append(
                    image_node
                )

        logger.info(
            f"Created "
            f"{len(text_nodes)} "
            f"text nodes and "
            f"{len(image_nodes)} "
            f"image nodes"
        )

        return {
            "text_nodes": text_nodes,
            "image_nodes": image_nodes,
            "response": MultimodalNodeResponse(
                text_node_count=len("text_nodes"),
                image_node_count=len("image_nodes"),
            )
        }


node_builder_service = (
    NodeBuilderService()
)