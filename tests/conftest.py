import os
import sys

# app/main.py imports `model` as a top-level module (as it runs inside Docker),
# so make the app/ directory importable when running the tests from the repo root.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))
