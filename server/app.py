from app import app

def main():
    return app

if __name__ == "__main__":
    # run uvicorn so it's truly executable
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
