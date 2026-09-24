from fastapi import FastAPI

app = FastAPI(
    title="Triahome API",
    description="AI-powered home repair triage",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "triahome-api",
    }