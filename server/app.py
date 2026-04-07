from app import app

def main():
    # simple execution-safe return
    return app

if __name__ == "__main__":
    # explicitly call and print something to ensure execution
    instance = main()
    print("Server initialized:", instance)
