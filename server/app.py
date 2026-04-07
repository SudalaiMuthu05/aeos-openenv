from app import app

def main():
    return app

if __name__ == "__main__":
    instance = main()
    print("Server entrypoint loaded:", instance)
