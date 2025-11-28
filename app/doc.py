import glob
import os
import subprocess
import time
import traceback
from pathlib import Path

import numpy as np
from PIL import Image


class Doc:
    def __init__(self):
        self.supported_documents = set([".pdf"])
        self.supported_images = set([])
        self.supported_files = self.supported_documents | self.supported_images

    def get_name(self, filename: str) -> str:
        name = Path(filename).name
        i = name.rfind(".")
        if name != "":
            return name[:i]
        return None

    def get_suffix(self, filename: str) -> str:
        suffix = Path(filename).suffix
        if len(suffix) != 0:
            return Path(filename).suffix.lstrip(".").lower()
        return None

    def verify(self, filename: str) -> bool:
        return Path(filename).suffix in self.supported_files

    def extract(self, filename: str) -> tuple:
        return (self.get_name(filename), self.get_suffix(filename))

    def convert(self, directory: str, filename: str) -> bool:
        try:
            if Path(filename).suffix in self.supported_files:
                if self.to_jpeg(directory, filename):
                    return True
            return False
        except Exception:
            traceback.print_exc()

    def to_jpeg(self, directory: str, filename: str) -> bool:
        try:
            absolute_path = os.path.join(os.getcwd(), directory)
            absolute_data_path = os.path.join(absolute_path, "data")
            name, extension = self.extract(filename)
            if extension == "pdf":
                commands = " && ".join(
                    [
                        f"cd {absolute_path}",
                        f"pdftoppm -jpeg -r 500 {filename} {absolute_data_path}/{filename}",
                    ]
                )
                output = subprocess.check_output(commands, shell=True)
                return True
            return False
        except Exception:
            traceback.print_exc()
