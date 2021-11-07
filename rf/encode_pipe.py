import os, sys, ctypes

# Fast send 18 ms, long 72ms

LOW = b'\00'
HIGH = b'\01'
NOOP_KEY = b'n'
ITERATIONS_KEY_VALID = 500
KEY_MAP = { 'w': 10, 's': 40, 'a': 58, 'd': 64, 'q': 28, 'e': 34, 'z': 52, 'c': 46 }
KEY_CODES = { k: [HIGH, HIGH, HIGH, LOW] * 4 + [HIGH, LOW] * v for k, v in KEY_MAP.items() }

libc = ctypes.CDLL('libc.so.6')
os.set_blocking(sys.stdin.fileno(), False)

last_key = NOOP_KEY
last_key_valid_times = 0

def update_key():
    global last_key
    global last_key_valid_times

    key = sys.stdin.read(1)
    if key != '' and key != '\n':
        last_key = key
        last_key_valid_times = ITERATIONS_KEY_VALID
        update_key()

while True:
    update_key()
    key = last_key if last_key_valid_times > 0 else NOOP_KEY

    if key in KEY_CODES:
        codes = KEY_CODES[key]
        for code in codes:
            os.write(sys.stdout.fileno(), code)
            libc.usleep(500)
            last_key_valid_times -= 1
    else:
        os.write(sys.stdout.fileno(), LOW)
        libc.usleep(500)
        last_key_valid_times -= 1
