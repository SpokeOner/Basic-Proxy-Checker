import requests
import threading
import queue
import time
from datetime import datetime

thread_count = int(input("Enter thread amount: "))


INPUT_FILE = 'proxies.txt'
INVALID_OUTPUT_FILE = 'invalid_proxies.txt'
WATERMARK = 'For UHQ proxies | 1$/gb 4$/hr resi | visit strikeproxy.net'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

proxy_queue = queue.Queue()
valid_proxies = []
invalid_proxies = []

with open(INPUT_FILE, 'r') as f:
    for line in f:
        proxy_queue.put(line.strip())

def check_proxy():
    while not proxy_queue.empty():
        proxy = proxy_queue.get()
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }
        start = time.time()
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
            latency = int((time.time() - start) * 1000)
            if response.status_code == 200:
                print(f'{GREEN}{proxy} | valid | {latency}ms{RESET}')
                valid_proxies.append(proxy)
            else:
                print(f'{RED}{proxy} | invalid{RESET}')
                invalid_proxies.append(proxy)
        except:
            print(f'{RED}{proxy} | invalid{RESET}')
            invalid_proxies.append(proxy)
        proxy_queue.task_done()

threads = []
for _ in range(thread_count):
    t = threading.Thread(target=check_proxy)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

valid_count = len(valid_proxies)
date_str = datetime.now().strftime("%Y-%m-%d")
VALID_OUTPUT_FILE = f'{valid_count:03}_proxies_{date_str}.txt'

with open(VALID_OUTPUT_FILE, 'w') as f:
    f.write(WATERMARK + '\n')
    for proxy in valid_proxies:
        f.write(proxy + '\n')
    f.write(WATERMARK + '\n')

with open(INVALID_OUTPUT_FILE, 'w') as f:
    for proxy in invalid_proxies:
        f.write(proxy + '\n')

print(f'\n✅ Completed! Valid proxies saved in: {VALID_OUTPUT_FILE}')
print(f'❌ Invalid proxies saved in: {INVALID_OUTPUT_FILE}')

