import pytest
from freezegun import freeze_time
from trimshare import __version__
from trimshare.trimshare import infer_out_video_name


def test_version():
    assert __version__ == "0.1.0"


@freeze_time("2001-01-01 01:01:01")
def test_infer_out_video_name(tmp_path):
    # don't infer name: valid, explicit out name
    assert infer_out_video_name("pwn3d.webm", "myvideo.mp4") == "pwn3d.webm"
    # deep input path
    assert (
        infer_out_video_name("pwn3d.webm", "deep/as/heck/path/myvideo.mp4")
        == "pwn3d.webm"
    )
    # same, but infer name
    assert (
        infer_out_video_name(None, "deep/as/heck/path/myvideo.mp4")
        == "deep/as/heck/path/myvideo.webm"
    )

    # infer name, no name conflict
    assert infer_out_video_name(None, "myvideo.mp4") == "myvideo.webm"
    # infer name, lots of dots
    assert infer_out_video_name(None, "my.special.video.mp4") == "my.special.video.webm"
    # infer name, name conflict: webm exists already
    (tmp_path / "myvideo.webm").touch()
    assert infer_out_video_name(None, str(tmp_path / "myvideo.webm")) == str(
        tmp_path / "myvideo-trimshare-2001-01-01-010101.webm"
    )


def test_same_out_and_in_name_error():
    with pytest.raises(FileExistsError):
        infer_out_video_name("myvideo.webm", "myvideo.webm")


@freeze_time("2001-01-01 01:01:01")
def test_rare_name_conflict(tmp_path):
    (tmp_path / "stuff.mkv").touch()
    (tmp_path / "stuff.webm").touch()
    (tmp_path / "stuff-trimshare-2001-01-01-010101.webm").touch()
    with pytest.raises(NameError):
        infer_out_video_name(None, str(tmp_path / "stuff.mkv"))
