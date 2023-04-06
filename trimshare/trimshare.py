#!/usr/bin/env python3
"""trimshare.py: Trim a video and convert to webm for easy sharing.

trimshare makes short clips out of long video files. It then converts
them to webm with the vp9 codec. By default, the quality is CRF 50.
At 720p and 60 fps, a clip of 10-30 seconds is usually less than 8 MB.

Source code of trimshare is Copyright © 2022-2023 JonLiuFYI,
licensed under GNU GPL v3. See LICENSE.

Example to grab 0:23-0:49 of `example.mkv`:
    trimshare example.mkv -s 0:23 -e 0:49

Usage:
    trimshare.py <in_video> [options]
    trimshare.py -h | --help
    trimshare.py --version

Arguments:
    <in_video>              Path to the video to trim.

Options:
    -o <out_video>          Export trimmed clip to this path as webm. If unspecified, automatically choose a name similar to <in_video> and save the clip in the same directory.
    -s --starttime <t>      Start the clip at this point in time. If unspecified, start at 0:00 on the source video.
    -e --endtime <t>        End the clip at this point in time. If unspecified, stop at the end of the source video.
    -q --quality <qual>     Set output vp9 quality (CRF mode), 0-63. Lower is better. [default: 50]
    -v --vresolution <px>   Change the resolution of the outputted video. Give the new vertical resolution in pixels and the horizontal resolution will scale automatically.
    --debug                 Show debugging info while this runs.
    -h --help               Show this help info.
    --version               Show the version number of trimshare.
"""
import logging
from pathlib import Path
import subprocess as sp

from docopt import docopt

VERSION = "trimshare 0.2.0"


def infer_out_video_name(outname: str | None, inname: str) -> str:
    """Determine what the output file's name should be, if needed.

    If ``outname`` is None, return the input video's file name with the
    extension changed to ``.webm``, adding ``-trimshare-{datetime}`` to
    avoid conflicts if needed.

    Args:
        outname (str | None): Output file name or None. If None, make up a name.
        inname (str): Input file name

    Raises:
        FileExistsError: ``outname`` and ``inname`` are the same

    Returns:
        str: File name to output to
    """
    if outname is not None:
        if outname == inname:
            raise FileExistsError("Output video must be different from the input video")
        return outname

    # strip file extension if there is one
    if "." in inname:
        inname = ".".join(inname.split(".")[:-1])

    conv_name = f"{inname}.webm"
    if Path(conv_name).exists():
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        safer_name = f"{inname}-trimshare-{now}.webm"
        if Path(safer_name).exists():
            raise NameError(
                f"Could not automatically generate a safe file name for {inname}"
            )
        return safer_name
    else:
        return conv_name


def main():
    args = docopt(__doc__, version=VERSION, more_magic=False)  # type: ignore
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.ERROR)

    in_video = args.in_video
    if not Path(in_video).exists():
        raise SystemExit(f"No file called {in_video}")

    start_time = args.starttime
    end_time = args.endtime
    out_video = infer_out_video_name(args.o, in_video)
    qual = args.quality
    vresolution = args.vresolution
    logging.debug(
        "Given args:\n"
        f"\t{in_video = }\n"
        f"\t{start_time = }\n"
        f"\t{end_time = }\n"
        f"\t{out_video = }\n"
        f"\t{qual = }\n"
        f"\t{vresolution = }"
    )

    start_time_arg = ["-ss", start_time] if start_time is not None else []
    end_time_arg = ["-to", end_time] if end_time is not None else []
    vresolution_arg = (
        ["-vf", f"scale=-1:{vresolution}"] if vresolution is not None else []
    )

    # fmt: off
    pass1 = [
        "ffmpeg",
        "-i", in_video,
        *start_time_arg,
        *end_time_arg,
        "-c:v", "libvpx-vp9",
        "-b:v", "0",
        "-crf", qual,
        *vresolution_arg,
        "-row-mt", "1",
        "-pass", "1",
        "-an",
        "-f", "null",
        "/dev/null",
    ]
    pass2 = [
        "ffmpeg",
        "-i", in_video,
        *start_time_arg,
        *end_time_arg,
        "-c:v", "libvpx-vp9",
        "-b:v", "0",
        "-crf", qual,
        *vresolution_arg,
        "-row-mt", "1",
        "-pass", "2",
        out_video,
    ]
    # fmt: on
    logging.debug(f"Pass 1: {' '.join(pass1)}")
    logging.debug(f"Pass 2: {' '.join(pass2)}")

    firstpass = sp.run(pass1)
    if firstpass.returncode != 0:
        raise SystemExit(
            "The first encoding pass failed! Check ffmpeg's output for the reason why."
        )
    sp.run(pass2)


if __name__ == "__main__":
    main()
