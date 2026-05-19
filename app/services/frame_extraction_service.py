import subprocess
from pathlib import Path

from app.utils.frame_utils import (
    build_frame_metadata,
    frames_already_exist,
    get_frame_output_dir,
)
from app.config.log_config import LogConfig

logger = LogConfig.get_logger(__name__)


class FrameExtractionService:

    def extract_frames(
        self,
        video_id: str,
        video_path: str,
        interval_seconds: int = 2,
    ) -> dict:

        logger.info(
            f"Starting frame extraction "
            f"for {video_id}"
        )

        frame_dir = (
            get_frame_output_dir(
                video_id
            )
        )

        # Reuse existing frames
        if frames_already_exist(
            frame_dir
        ):

            logger.info(
                "Frames already exist. "
                "Skipping extraction."
            )

            existing_frames = sorted(
                frame_dir.glob("*.jpg")
            )

            frame_metadata = (
                build_frame_metadata(
                    frame_paths=(
                        existing_frames
                    ),
                    interval_seconds=(
                        interval_seconds
                    ),
                )
            )

            return {
                "video_id": video_id,
                "frame_count": len(
                    frame_metadata
                ),
                "frames": frame_metadata,
            }

        output_pattern = str(
            frame_dir
            / "frame_%04d.jpg"
        )

        fps_value = (
            f"1/{interval_seconds}"
        )

        command = [
            "ffmpeg",
            "-i",
            video_path,
            "-vf",
            f"fps={fps_value}",
            output_pattern,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
        ]

        try:

            subprocess.run(
                command,
                check=True,
            )

        except subprocess.CalledProcessError as exc:

            logger.exception(
                "Frame extraction failed."
            )

            raise RuntimeError(
                "Failed to extract frames."
            ) from exc

        extracted_frames = sorted(
            frame_dir.glob("*.jpg")
        )

        frame_metadata = (
            build_frame_metadata(
                frame_paths=(
                    extracted_frames
                ),
                interval_seconds=(
                    interval_seconds
                ),
            )
        )

        logger.info(
            f"Extracted "
            f"{len(frame_metadata)} "
            f"frames for {video_id}"
        )

        return {
            "video_id": video_id,
            "frame_count": len(
                frame_metadata
            ),
            "frames": frame_metadata,
        }


frame_extraction_service = (
    FrameExtractionService()
)