from pathlib import Path


def get_frame_output_dir(
    video_id: str,
) -> Path:

    frame_dir = (
        Path("storage/frames")
        / video_id
    )

    frame_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return frame_dir


def frames_already_exist(
    frame_dir: Path,
) -> bool:

    return any(
        frame_dir.glob("*.jpg")
    )


def build_frame_metadata(
    frame_paths: list[Path],
    interval_seconds: int,
) -> list[dict]:

    metadata = []

    for index, frame_path in enumerate(
        sorted(frame_paths)
    ):

        metadata.append(
            {
                "timestamp": (
                    index
                    * interval_seconds
                ),
                "frame_path": str(
                    frame_path
                ),
            }
        )

    return metadata