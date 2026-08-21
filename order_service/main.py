from fastapi import FastAPI
import random

app = FastAPI(title="Order Service")

service_status = {
    "healthy": True,
    "slow": False
}


@app.get("/")
def home():
    return {
        "service": "Order Service",
        "status": "running"
    }


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


@app.post("/simulate/failure")
def simulate_failure():
    service_status["healthy"] = False

    return {
        "message": "Order Service failure simulated",
        "status": "failed"
    }


@app.post("/simulate/recover")
def recover():
    service_status["healthy"] = True
    service_status["slow"] = False

    return {
        "message": "Order Service recovered",
        "status": "healthy"
    }


@app.post("/simulate/slow")
def simulate_slow():
    service_status["slow"] = True

    return {
        "message": "Slow response simulated"
    }