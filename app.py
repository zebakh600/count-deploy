import os, sys
from flask import Flask
import redis

app = Flask(__name__)

# Intentional crash switch (not used by default)
if os.environ.get("CRASH_MODE") == "true":
    sys.exit(1)

redis_host = os.environ.get("REDIS_HOST", "localhost")
try:
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    r.ping()  # quick check
except Exception as e:
    print(f"Redis connection failed: {e}", flush=True)
    sys.exit(1)

@app.route("/")
def hello():
    count = r.incr("hits")
    return f"Hello from DevOps Challenge! Visitor count: {count}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)