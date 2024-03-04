import environ
import os
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


HOST = env('HOST')
PORT = env('PORT')
USERNAME = env('USERNAME')
REMOTE_FILE_PATH = os.path.join(env('REMOTE_FILE_PATH'), env('FILE_NAME'))
LOCAL_FILE_PATH = os.path.join(BASE_DIR, env('FILE_NAME'))


def main():
    os.system(f'scp -O -P {PORT} {USERNAME}@{HOST}:{REMOTE_FILE_PATH} {LOCAL_FILE_PATH}')

if __name__ == '__main__':
    main()