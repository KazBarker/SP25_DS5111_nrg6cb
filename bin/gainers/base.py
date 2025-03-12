import os
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from io import StringIO

# DOWNLOADER
class GainerDownload(ABC):
    def __init__(self):
        self.url = url
        self.out_path = out_path
        self.name = data_name

    @abstractmethod
    def download(self):
        pass

# PROCESSOR 
class GainerProcess(ABC):
    def __init__(self):
        self.raw_path = raw_path
        self.out_path = out_path
        self.col_count = col_count
        self.name = name

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def save_with_timestamp(self):
        pass

