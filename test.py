import json
import hashlib
import os

a= json.dumps(("hello", hashlib.sha256("random".encode("utf-8")).hexdigest())).encode("utf-8")

print(json.loads(a.decode("utf-8")))