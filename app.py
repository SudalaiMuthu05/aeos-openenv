from fastapi import FastAPI
from env.environment import AEOSEnv
from env.models import AEOSAction

app = FastAPI()

# Initialize environment
env = AEOSEnv()


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def home():
    return {"message": "AEOS is running 🚀"}


# -----------------------------
# RESET
# -----------------------------
@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.model_dump()}


# -----------------------------
# STEP
# -----------------------------
@app.post("/step")
def step(action: AEOSAction):
    result = env.step(action)

    return {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }


# -----------------------------
# STATE
# -----------------------------
@app.get("/state")
def state():
    return env.state().model_dump()
