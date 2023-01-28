=========
Trimshare
=========
Trimshare *trims* your videos into short clips, made web-friendly for easy *sharing*. No need to remember the correct FFmpeg incantation!

Trimshare is handy if you have long videos like gameplay footage and want to grab specific moments to share with others in chatrooms or forums. A 10-30 second clip at 720p 60 fps will usually take less than 8 MB.

Details
-------
This command-line tool is a frontend to FFmpeg with a simpler, opinionated interface specifically for extracting short clips from long videos and encoding them into VP9 ``.webm`` files. The VP9 encoder is set to use constant quality mode with a CRF of 50 by default.

Building from source
--------------------
Prerequisites
=============
* pip
* `Poetry <https://python-poetry.org/>`_
* FFmpeg
    * Must be available on your PATH
    * Must be built with VP9 encode support (it very likely already is)

Build
=====
Build and install the ``trimshare`` binary to your PATH::

    poetry install

Usage
-----
Run with the command::

    trimshare

Get full help text for arguments with::

    trimshare --help
    
Example typical usage to grab 0:23 to 0:49 on a file called ``example.mkv``::

    trimshare example.mkv -s 0:23 -e 0:49

This generates a file called ``example.webm`` that's a shortened, compressed clip of the original video file.

License
-------
Copyright © 2022-2023 JonLiuFYI.

Trimshare is free software. Its source is released under the GNU GPL v3. See ``LICENSE``.