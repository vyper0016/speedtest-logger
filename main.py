import speedtest
import time
from datetime import datetime
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

INTERVAL_TESTS = config['DEFAULT'].getint('interval')*60
LOG_FILE = config['DEFAULT'].get('log path')

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

def test_speed():
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    return s.results.dict()


def log_test():
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = {}
    
    timestamp = str(datetime.now())
    
    print('testing at', timestamp)
    logs[timestamp] = test_speed()

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=3)

    print('finished')


def periodic_test(interval=INTERVAL_TESTS):

    while True:
        log_test()
        print('\nstanding by for', interval, 'seconds...')
        time.sleep(interval)


periodic_test()
