import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "lib"))
from lib.query import QueryEngine
print("Importing QueryEngine...")
try:
    engine = QueryEngine()
    print("QueryEngine initialized successfully!")
except Exception as e:
    print(f"Error: {e}")
