from pydantic import BaseModel
import os
import subprocess


class BaseResponse(BaseModel):
    message: str='status success'


def find_process_by_port(port=8000):
    result = subprocess.run(['lsof', '-i', f':{8000}'], capture_output=True, text=True)
    for line in result.stdout.split('\n')[1:]:
        process_id = line.split()[1]
        return int(process_id)
    return None


def kill_process(process_id):
    os.kill(process_id, 9)
