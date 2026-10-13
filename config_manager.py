"""
Module name: config_manager.py
Description: Configurations
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.2
"""
import json

CONFIGS = {
    "menubar": False,
    "debug": False
}

def readConfigs(file_dir:str) -> None:
    """
    Reads configs from file directory
    """
    with open(file_dir,'r') as file:
        global CONFIGS
        CONFIGS = json.load(file)
