#!/usr/bin/env python3
import subprocess
import sys
import webbrowser
import time
import os
from dotenv import load_dotenv

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    compose_file = os.path.join(os.path.dirname(project_root), "docker-compose.yml")

    if os.path.exists(compose_file):
        os.chdir(os.path.dirname(project_root))
        subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)
        time.sleep(15)
        webbrowser.open("http://localhost:8000/docs")
    else:
        os.chdir(project_root)
        load_dotenv()
        proc = subprocess.Popen(
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            cwd=project_root
        )
        time.sleep(3)
        webbrowser.open("http://localhost:8000/docs")
        proc.wait()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)