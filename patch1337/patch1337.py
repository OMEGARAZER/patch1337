#!/usr/bin/env python
"""Patches files based on 1337 patch files."""

import binascii
import shutil
import sys
from pathlib import Path

import click
from loguru import logger

__version__ = "0.5.0"


@click.command()
@click.help_option("-h", "--help")
@click.option(
    "-p",
    "--patch",
    required=True,
    multiple=True,
    default=[
        "nvencodeapi.1337",
        "nvencodeapi64.1337",
    ],
    help="Filename(s) of .1337 patch(es)",
)
@click.option(
    "-t",
    "--target",
    required=True,
    multiple=True,
    default=[
        "nvEncodeAPI.dll",
        "nvEncodeAPI64.dll",
    ],
    help="Filename(s) of target file(s).",
)
@click.option(
    "-o",
    "--offset",
    required=False,
    multiple=True,
    default=[
        True,
        True,
    ],
    help="Apply x64dbg offset (True by default).",
)
@click.option("-v", "--verbose", count=True, default=None, help="Increase verbosity of output.")
@click.pass_context
def main(context: click.Context, **_) -> None:
    """Patches files based on 1337 patch files."""
    set_logging(context)
    patch = context.params["patch"]
    target = context.params["target"]
    offset = context.params["offset"]
    combinations = zip(patch, target, offset)
    for params in combinations:
        patcher(*params)


def set_logging(context: click.core.Context) -> None:
    """Set logging level."""
    level = "INFO"
    if context.params["verbose"]:
        level = "DEBUG"
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", "level": level},
        ],
    )


def check_patch(patch_file: str) -> bool:
    """Check validity of patch file."""
    with Path(patch_file).open() as header:
        if not header.readline().startswith(">"):
            logger.error("{} is not a valid .1337 patch file", Path(patch_file).name)
            return False
        logger.debug("{} is a valid .1337 patch file", Path(patch_file).name)
        return True


def backup_file(target: str) -> bool:
    """Backup original target file."""
    overwrite_backup = True
    backup_file = target + ".BAK"
    if Path(backup_file).exists():
        overwrite_backup = False
        overwrite_check = input("Backup file exists, would you like to overwrite? (y/n/X): ")
        if overwrite_check.lower() == "y":
            overwrite_backup = True
        if not overwrite_backup and overwrite_check.lower() != "n":
            return False
    if overwrite_backup:
        shutil.copy(Path(target), Path(backup_file))
        logger.info("Created backup of {}", Path(target).name)
    return True


def patcher(patch_file: str, target: str, offset: str) -> None:
    """Patch file."""
    errors = False
    if not Path(patch_file).exists() or not Path(target).exists():
        logger.error("{} or {} no longer exist", patch_file, target)
        return
    if not check_patch(patch_file):
        return
    if not backup_file(target):
        return
    with Path(patch_file).open() as patch_file, Path(target).open(mode="r+b", buffering=0) as unpatched_file:
        patch_lines = patch_file.readlines()
        patch_target = str(patch_lines[0])[1:].strip().lower()
        target_filename = Path(target).name
        if patch_target != target_filename.lower():
            logger.error(
                "The .1337 patch is not valid for the selected file ({}) but you selected ({})",
                str(patch_lines[0])[1:].lower(),
                target_filename,
            )
            return
        offset = 0xC00 if offset else 0x0
        for line in patch_lines[1:]:
            if line:
                tmp = line.strip().split(":")
                location = hex(int(tmp[0], base=16) - int(offset))
                patch = tmp[1].split("->")
                logger.debug("Patch line: {}", line.strip())
                logger.debug("Patching {} from {} to {}", "0x" + location[2:].upper(), patch[0], patch[1])
                unpatched_file.seek(int(location, base=16))
                unpatched_read = unpatched_file.read(1)
                if unpatched_read == binascii.unhexlify(patch[0]):
                    unpatched_file.seek(int(location, base=16))
                    unpatched_file.write(binascii.unhexlify(patch[1]))
                    logger.debug("Patched  {} from {} to {}", "0x" + location[2:].upper(), patch[0], patch[1])
                else:
                    logger.error(
                        "Offset {} was expected to be {} but was {} instead",
                        "0x" + location[2:].upper(),
                        patch[0],
                        unpatched_read,
                    )
                    errors = True
                    break
        if not errors:
            for line in patch_lines[1:]:
                if line:
                    tmp = line.strip().split(":")
                    location = hex(int(tmp[0], base=16) - int(offset))
                    patch = tmp[1].split("->")
                    logger.debug("Checking patch at {}", "0x" + location[2:].upper())
                    unpatched_file.seek(int(location, base=16))
                    patched_read = unpatched_file.read(1)
                    if patched_read == binascii.unhexlify(patch[1]):
                        logger.debug("{} has been patched correctly to {}", "0x" + location[2:].upper(), patch[1])
                    else:
                        logger.error(
                            "{} was NOT patched correctly to {} it is currently {}",
                            "0x" + location[2:].upper(),
                            patch[1],
                            patched_read,
                        )
                        break
        logger.info("Patching complete on {}", target_filename)


if __name__ == "__main__":
    main()
