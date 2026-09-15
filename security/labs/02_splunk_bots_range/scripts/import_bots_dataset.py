import json
import sys
import time
import urllib.request

url = "http://localhost:9200/bots-enterprise-logs/_bulk"
dataset_path = "datasets/bots_sample_events.json"

print("[*] Waiting for OpenSearch to be healthy...")
for _ in range(30):
    try:
        with urllib.request.urlopen("http://localhost:9200") as resp:  # skipcq: BAN-B310
            if resp.status == 200:
                print("[+] OpenSearch is online!")
                break
    except Exception:
        time.sleep(2)
else:
    print("[-] OpenSearch timed out. Please check docker compose logs.")
    sys.exit(1)

print(f"[*] Importing {dataset_path} into OpenSearch...")
with open(dataset_path, "rb") as f:
    data = f.read()

req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-ndjson"}, method="POST")
with urllib.request.urlopen(req) as resp:  # skipcq: BAN-B310
    result = json.loads(resp.read().decode('utf-8'))
    items_count = len(result.get('items', []))
    print(f"[+] Successfully indexed {items_count} BOTS security events!")
