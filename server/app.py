def main():
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from app import app
    return app
