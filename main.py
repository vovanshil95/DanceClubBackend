import uvicorn

import subprocess
import sys
sys.path.append(f'{sys.path[0]}/src')
from utils import kill_process, find_process_by_port

if __name__ == "__main__":
    process_id = find_process_by_port(8000)
    if process_id is not None:
        kill_process(process_id)

    uvicorn.run("src.app:app", host="0.0.0.0", log_level="info", port=8000)
