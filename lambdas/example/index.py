import random


def submit_status(event, context):
    return {
        "seconds": random.randrange(4),
        "data": random.randrange(100),
    }


def get_status(event, context):
    return {
        "status": random.choice(["FAILED", "PROCESSING", "SUCCEEDED"]),
        "data": event["data"],
    }


def final_status(event, context):
    print("success")
    return {"status": event["status"], "and data": event["data"]}
