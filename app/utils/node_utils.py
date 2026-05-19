from collections import defaultdict


def group_frames_by_time_window(
    frames: list[dict],
    window_size: int = 15,
) -> dict:

    grouped = defaultdict(list)

    for frame in frames:

        timestamp = frame[
            "timestamp"
        ]

        window_start = (
            int(timestamp)
            // window_size
        ) * window_size

        grouped[
            window_start
        ].append(frame)

    return grouped