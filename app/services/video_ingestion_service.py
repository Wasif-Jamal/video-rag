from app.schema.node_schema import MultimodalNodeResponse
from app.services.youtube_service import (
    youtube_service,
)
from app.services.video_download_service import (
    video_download_service,
)
from app.services.transcription_service import (
    transcription_service,
)

from app.services.frame_extraction_service import (
    frame_extraction_service,
)

from app.services.node_builder_service import (
    node_builder_service,
)


class VideoIngestionService:

    async def ingest_youtube_video(
        self,
        url: str,
    ) -> dict:

        # 1. Fetch metadata
        metadata = youtube_service.get_metadata(url)

        duration = metadata.get("duration")

        if not duration:
            raise ValueError(
                "Could not retrieve video duration."
            )

        # 2. Enforce duration limit
        if duration > 420:

            raise ValueError(
                f"Video is too long ({duration}s). "
                "Maximum allowed length is 7 minutes."
            )

        # 3. Download video
        video_id = metadata["id"]

        video_path = (
            video_download_service.download_video(
                url=url,
                video_id=video_id,
            )
        )

        # 4. Generate transcript
        transcript_result = (
            transcription_service
            .process_transcript(
                video_id=video_id,
                local_video_path=video_path,
            )
        )

        # 5. Extract frames
        frame_result = (
            frame_extraction_service
            .extract_frames(
                video_id=video_id,
                video_path=video_path,
            )
        )

        # 6. Create text and image nodes
        node_result = (
            node_builder_service
            .build_nodes(
                transcript_segments=(
                    transcript_result
                    .segments
                ),
                frames=(
                    frame_result["frames"]
                ),
                video_id=video_id,
            )
        )

        # 7. Return ingestion result
        return {
            "video": {
                "url": url,
                "video_id": video_id,
                "title": metadata["title"],
                "duration": duration,
                "channel": metadata.get(
                    "channel",
                    "Unknown",
                ),
                "local_path": video_path,
            },
            "transcript": transcript_result,
            "frames": frame_result,
            "nodes": node_result["response"]
        }


video_ingestion_service = (
    VideoIngestionService()
)