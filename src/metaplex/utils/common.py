import mimetypes
import random
import re


def remove_empty_chars(value: str) -> str:
    return re.sub(r"\x00", "", value)


def zip_map(left, right, fn):
    return [fn(t, u) for i, (t, u) in enumerate(zip(left, right))]


def random_str(
    length=20, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
):
    return "".join(random.choice(alphabet) for _ in range(length))


def get_content_type(file_name):
    return mimetypes.guess_type(file_name)[0]


def get_extension(file_name):
    last_dot_index = file_name.rfind(".")
    return None if last_dot_index < 0 else file_name[last_dot_index + 1 :]
