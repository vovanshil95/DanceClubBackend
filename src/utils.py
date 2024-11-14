from pydantic import BaseModel

import os
import subprocess
import platform


class BaseResponse(BaseModel):
    message: str='status success'


def kill_port(port):
    try:
        if platform.system() == 'Windows':
            netstat_args = '-ano'
        else:
            netstat_args = '-tulpn'

        result = subprocess.run(
            ["netstat", netstat_args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        lines = result.stdout.splitlines()
        pid_to_kill = None
        for line in lines:
            if f":{port}" in line:
                pid_to_kill = int(line.split()[-1].split('/')[0])
                break
        
        if pid_to_kill:
            os.kill(pid_to_kill, 9)
        else:
            print(f"No process found running on port {port}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

