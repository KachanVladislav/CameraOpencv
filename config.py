import pickle
import cv2
import numpy as np
from pathlib import Path
import configparser


def get_config():
    config = Path("./config/config.conf")
    if not config.is_file():
        print("Config file was not found, creating...")



def main():
    pass

if (__name__ == "__main__"):
    main()