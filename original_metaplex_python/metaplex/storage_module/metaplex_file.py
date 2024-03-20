import json
import os

from original_metaplex_python.metaplex.utils.common import (
    get_content_type,
    get_extension,
    random_str,
)


def to_metaplex_file(content, file_name, options=None):
    if options is None:
        options = {}

    file_content = parse_metaplex_file_content(content)
    display_name = options.get("displayName", file_name)
    unique_name = options.get("uniqueName", random_str())
    content_type = options.get("contentType", get_content_type(file_name))
    extension = options.get("extension", get_extension(file_name))
    tags = options.get("tags", [])

    return {
        "buffer": file_content,
        "fileName": file_name,
        "displayName": display_name,
        "uniqueName": unique_name,
        "contentType": content_type,
        "extension": extension,
        "tags": tags,
    }


def to_metaplex_file_from_browser(file_path, options=None):
    with open(file_path, "rb") as file:
        content = file.read()
    return to_metaplex_file(content, os.path.basename(file_path), options)


def to_metaplex_file_from_json(json_obj, file_name="inline.json", options=None):
    try:
        json_string = json.dumps(json_obj)
    except Exception as error:
        raise ValueError(f"Invalid JSON variable: {error}")

    return to_metaplex_file(json_string, file_name, options)


def parse_metaplex_file_content(content):
    # If the content is a byte-like object (similar to ArrayBuffer in JS)
    if isinstance(content, (bytes, bytearray, memoryview)):
        return bytes(content)

    # Assuming the content is a string if not a byte-like object
    return content.encode()


def get_bytes_from_metaplex_files(*files):
    return sum(len(file["buffer"]) for file in files)


def write_metaplex_file_to_disk(metaplex_file):
    with open(metaplex_file["fileName"], "wb") as f:
        f.write(metaplex_file["buffer"])


def is_metaplex_file(metaplex_file):
    required_keys = {
        "buffer",
        "fileName",
        "displayName",
        "uniqueName",
        "contentType",
        "extension",
        "tags",
    }
    return (
        all(key in metaplex_file for key in required_keys)
        if isinstance(metaplex_file, dict)
        else False
    )
