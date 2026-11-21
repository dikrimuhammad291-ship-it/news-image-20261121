#!/usr/bin/env python3
"""Entrypoint for the 21 November 2026 world-news front page.

This program takes the finished front-page image (``entry.png``, which lives
next to this script) and places a copy of it in the output directory so the
grader can find it.  It does not draw anything itself -- the drawing is done
by ``render.py``; this script only delivers the finished picture.

The output directory is ``/output`` by default.  Outside the grader you can
point it somewhere else with the ``MAKEFUN_OUTPUT_DIR`` environment variable.
"""

import os
import shutil
import sys
from pathlib import Path

# Name of the finished image file, sitting beside this script.
IMAGE_NAME = "entry.png"

# Where the grader expects the picture to end up.
DEFAULT_OUTPUT_DIR = "/output"

# Environment variable that overrides the output directory when set.
OUTPUT_DIR_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def script_folder() -> Path:
    """Return the directory that contains this script."""
    return Path(__file__).resolve().parent


def output_folder() -> Path:
    """Return where the image should be copied to.

    The ``MAKEFUN_OUTPUT_DIR`` environment variable wins when it is set to a
    non-empty value; otherwise we fall back to ``/output``.
    """
    override = os.environ.get(OUTPUT_DIR_ENV_VAR, "").strip()
    if override:
        return Path(override)
    return Path(DEFAULT_OUTPUT_DIR)


def deliver_image() -> Path:
    """Copy ``entry.png`` into the output directory.

    Returns the path of the copy that was written.  Raises
    ``FileNotFoundError`` when the source image is missing and ``OSError``
    when the copy itself fails.
    """
    source = script_folder() / IMAGE_NAME
    if not source.is_file():
        raise FileNotFoundError(f"finished image not found: {source}")

    destination_dir = output_folder()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / IMAGE_NAME

    shutil.copyfile(source, destination)

    # Sanity check: the copy must be exactly as large as the original.
    if destination.stat().st_size != source.stat().st_size:
        raise OSError(
            f"copy size mismatch: {destination} is "
            f"{destination.stat().st_size} bytes, expected "
            f"{source.stat().st_size}"
        )
    return destination


def main() -> int:
    """Copy the front page into place and report what happened."""
    try:
        written = deliver_image()
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: could not write the image: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
