import json

import requests

from original_metaplex_python.metaplex.errors.sdk_error import (
    DriverNotProvidedError,
    InvalidJsonStringError,
)
from original_metaplex_python.metaplex.storage_module.metaplex_file import (
    get_bytes_from_metaplex_files,
    to_metaplex_file,
    to_metaplex_file_from_json,
)


class StorageClient:
    def __init__(self):
        self._driver = None

    def driver(self):
        if not self._driver:
            raise DriverNotProvidedError("StorageDriver")
        return self._driver

    def set_driver(self, new_driver):
        self._driver = new_driver

    def get_upload_price_for_bytes(self, data):
        return self.driver().get_upload_price(data)

    def get_upload_price_for_file(self, file):
        return self.get_upload_price_for_files([file])

    def get_upload_price_for_files(self, files):
        driver = self.driver()
        if hasattr(driver, "get_upload_price_for_files"):
            return driver.get_upload_price_for_files(files)
        else:
            return self.get_upload_price_for_bytes(
                get_bytes_from_metaplex_files(*files)
            )

    def upload(self, file):
        return self.driver().upload(file)

    def upload_all(self, files):
        driver = self.driver()
        if hasattr(driver, "upload_all"):
            return driver.upload_all(files)
        else:
            return [self.driver().upload(file) for file in files]

    def upload_json(self, json_obj):
        return self.upload(to_metaplex_file_from_json(json_obj))

    def download(self, uri, options=None):
        driver = self.driver()
        if hasattr(driver, "download"):
            return driver.download(uri, options)
        else:
            response = requests.get(uri, **(options or {}))
            return to_metaplex_file(response.content, uri)

    def download_json(self, uri, options=None):
        file = self.download(uri, options)
        try:
            return json.loads(file["buffer"].decode())
        except Exception as error:
            raise InvalidJsonStringError(error)
