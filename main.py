import sys
import os

# Add src to sys.path if not installed in editable mode
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from random_walk.cli import main

if __name__ == '__main__':
    main()
