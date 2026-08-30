from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Payment Service")


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================
# SERVICE STATUS
# =========================

service_status = {
    "healthy": True,
    "slow": False
}


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "service": "Payment Service",
        "status": "running"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():

    if not service_status["healthy"]:
        return {
            "service": "payment-service",
            "status": "unhealthy"
        }

    return {
        "service": "payment-service",
        "status": "healthy"
    }


# =========================
# METRICS
# =========================

@app.get("/metrics")
def metrics():

    # Generate response time
    response_time = random.randint(50, 150)

    # If service is slow
    if service_status["slow"]:
        response_time = random.randint(800, 2000)

    # Generate metrics
    return {
        "service": "payment-service",
        "cpu": random.randint(10, 80),
        "memory": random.randint(20, 75),
        "response_time_ms": response_time,
        "error_rate": random.randint(0, 5),
        "healthy": service_status["healthy"],
        "slow": service_status["slow"]
    }


# =========================
# SIMULATE FAILURE
# =========================

@app.post("/simulate/failure")
def simulate_failure():

    service_status["healthy"] = False

    return {
        "message": "Payment Service failure simulated",
        "status": "failed"
    }


# =========================
# RECOVER SERVICE
# =========================

@app.post("/simulate/recover")
def recover():

    service_status["healthy"] = True
    service_status["slow"] = False

    return {
        "message": "Payment Service recovered",
        "status": "healthy"
    }


# =========================
# SIMULATE SLOW SERVICE
# =========================

@app.post("/simulate/slow")
def simulate_slow():

    service_status["slow"] = True

    return {
        "message": "Slow response simulated",
        "status": "slow"
    }