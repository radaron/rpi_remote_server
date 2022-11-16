import os
import uuid

if __name__ == "__main__":
    secret_path = os.path.join(os.path.dirname(__file__), os.pardir, "secret")
    with open(secret_path, "w", encoding="utf-8") as f:
        f.write(str(uuid.uuid4().hex))