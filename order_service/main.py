from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Order Service")


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# SERVICE STATUS
# ==========================================

service_status = {
    "healthy": True,
    "slow": False
}


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "service": "Order Service",
        "status": "running"
    }


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health():

    if not service_status["healthy"]:
        return {
            "service": "order-service",
            "status": "unhealthy"
        }

    return {
        "service": "order-service",
        "status": "healthy"
    }


# ==========================================
# METRICS
# ==========================================

@app.get("/metrics")
def metrics():

    response_time = random.randint(50, 150)

    if service_status["slow"]:
        response_time = random.randint(800, 2000)

    return {
        "service": "order-service",
        "cpu": random.randint(10, 80),
        "memory": random.randint(20, 75),
        "response_time_ms": response_time,
        "error_rate": random.randint(0, 5)
    }


# ==========================================
# SIMULATE FAILURE
# ==========================================

@app.post("/simulate/failure")
def simulate_failure():

    service_status["healthy"] = False

    return {
        "message": "Order Service failure simulated",
        "status": "failed"
    }


# ==========================================
# RECOVER SERVICE
# ==========================================

@app.post("/simulate/recover")
def recover():

    service_status["healthy"] = True
    service_status["slow"] = False

    return {
        "message": "Order Service recovered",
        "status": "healthy"
    }


# ==========================================
# SIMULATE SLOW SERVICE
# ==========================================

@app.post("/simulate/slow")
def simulate_slow():

    service_status["slow"] = True

    return {
        "message": "Slow response simulated"
    }