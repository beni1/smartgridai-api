from fastapi import FastAPI, Depends
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# Internal modules (IMPORTANT: must use api. prefix)
from api.model import generate_demand
from api.auth import verify_api_key
from api.usage import check_limit

# Create FastAPI app (must be defined before routes)
app = FastAPI(title="SmartGridAI API")


# -------------------------
# Root endpoint (health check)
# -------------------------
@app.get("/")
def root():
    return {
        "message": "SmartGridAI API is running"
    }


# -------------------------
# Demand endpoint (secured + usage tracking + plans)
# -------------------------
@app.get("/demand")
def get_demand(days: int = 1, auth=Depends(verify_api_key)):
    api_key, plan = auth

    # Check usage limits
    allowed, used, limit = check_limit(api_key, plan)

    if not allowed:
        return {
            "error": "Usage limit exceeded",
            "plan": plan,
            "used": used,
            "limit": limit
        }

    # Generate demand data
    data = generate_demand(days)

    return {
        "plan": plan,
        "used": used,
        "limit": limit,
        "data": data
    }
