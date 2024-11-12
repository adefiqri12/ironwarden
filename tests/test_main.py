import unittest
from unittest.mock import patch, MagicMock, call
import sqlite3
import sys
import os
import ctypes

# Since main.py is in app directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import (
    clear_screen,
    secure_clear,
    exit_program,
    display_menu,
    handle_login,
    handle_password_operations,
    main
)