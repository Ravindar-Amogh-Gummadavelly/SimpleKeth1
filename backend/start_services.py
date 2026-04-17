"""
SimpleKeth — Native Backend Launcher
Starts all 4 microservices concurrently for easier local development without Docker.
"""

import subprocess
import sys
import time

SERVICES = [
    ("Prediction Service", "prediction_service.main:app", 8001),
    ("Recommendation Service", "recommendation_service.main:app", 8002),
    ("Notification Service", "notification_service.main:app", 8003),
    ("Profile Service", "profile_service.main:app", 8004),
]

processes = []

def main():
    print("🚀 Starting SimpleKeth Native Backend Services...\n")
    
    for name, module, port in SERVICES:
        cmd = [sys.executable, "-m", "uvicorn", module, "--port", str(port), "--reload"]
        print(f"[{name}] Starting on port {port}...")
        
        import os
        # Start process and don't block
        p = subprocess.Popen(
            cmd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        processes.append((name, p))
        time.sleep(1) # Slight stagger to prevent log jumbling
        
    print("\n✅ All services started. Press Ctrl+C to stop all.\n")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        for name, p in processes:
            p.terminate()
            p.wait()
            print(f"[{name}] Halted.")
        print("Done.")

if __name__ == "__main__":
    main()
