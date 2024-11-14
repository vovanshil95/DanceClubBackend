import uvicorn

import sys
sys.path.append(f'{sys.path[0]}/src')
from utils import kill_port

if __name__ == "__main__":
    kill_port(8000)

    uvicorn.run("src.app:app", host="0.0.0.0", log_level="info", port=8000)
