import json
import os
from dotenv import set_key

# Paths to your config and .env files
CONFIG_PATH = "config.json"
ENV_PATH = ".env"

def update_config():
    if not os.path.exists(CONFIG_PATH):
import os
import json

CONFIG_PATH = "config.json"
ENV_PATH = ".env"

def set_key(file_path, key, value):
    """
    Updates or adds a key=value pair in a .env file.
    """
    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
    updated = False
    with open(file_path, "w") as f:
        for line in lines:
            if line.startswith(f"{key}="):
                f.write(f"{key}={value}\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f"{key}={value}\n")

def update_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:  # Create config.json if it doesn't exist
            f.write("{}")

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    api_id = input("API ID: ")
    api_hash = input("API Hash: ")
    phone = input("Phone Number: ")

    if api_id:
        config["api_id"] = api_id
    if api_hash:
        config["api_hash"] = api_hash
    if phone:
        config["phone"] = phone

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print("config.json updated successfully!")

def update_env():
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, "w").close()  # Create .env if it doesn't exist

    email = input("Quotex Email: ")
    password = input("Quotex Password: ")

    if email:
        set_key(ENV_PATH, "QUOTEX_EMAIL", email)
    if password:
        set_key(ENV_PATH, "QUOTEX_PASSWORD", password)

    print(".env updated successfully!")

if __name__ == "__main__":
    update_config()
    update_env()
    print("All credentials updated. You can now run: python main.py")
import os
import json

CONFIG_PATH = "config.json"
ENV_PATH = ".env"

def set_key(file_path, key, value):
    """
    Updates or adds a key=value pair in a .env file.
    """
    lines = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
    updated = False
    with open(file_path, "w") as f:
        for line in lines:
            if line.startswith(f"{key}="):
                f.write(f"{key}={value}\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f"{key}={value}\n")

def update_config():
    if not os.path.exists(CONFIG_PATH):
        open(CONFIG_PATH, "w").write("{}")  # Create config.json if it doesn't exist

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    api_id = input("API ID: ")
    api_hash = input("API Hash: ")
    phone = input("Phone Number: ")

    if api_id:
        config["api_id"] = api_id
    if api_hash:
        config["api_hash"] = api_hash
    if phone:
        config["phone"] = phone

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print("config.json updated successfully!")

def update_env():
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, "w").close()  # Create .env if it doesn't exist

    email = input("Quotex Email: ")
    password = input("Quotex Password: ")

    if email:
        set_key(ENV_PATH, "QUOTEX_EMAIL", email)
    if password:
        set_key(ENV_PATH, "QUOTEX_PASSWORD", password)

    print(".env updated successfully!")

if __name__ == "__main__":
    update_config()
    update_env()
    print("All credentials updated. You can now run: python main.py")
        print(f"{CONFIG_PATH} not found!")
        return

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    print("Leave a field blank to keep the current value.\n")

    api_id = input(f"API ID [{config.get('api_id')}]: ") or config.get("api_id")
    api_hash = input(f"API Hash [{config.get('api_hash')}]: ") or config.get("api_hash")
    phone = input(f"Phone [{config.get('phone')}]: ") or config.get("phone")
    trade_amount = input(f"Trade Amount [{config.get('trade_amount', 20)}]: ") or config.get("trade_amount")
    use_real_broker = input(f"Use Real Broker (true/false) [{config.get('use_real_broker', False)}]: ") or config.get("use_real_broker")

    config.update({
        "api_id": api_id,
        "api_hash": api_hash,
        "phone": phone,
        "trade_amount": int(trade_amount),
        "use_real_broker": use_real_broker if isinstance(use_real_broker, bool) else use_real_broker.lower() == "true"
    })

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print("config.json updated successfully!")

def update_env():
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, "w").close()  # Create .env if it doesn't exist

    email = input("nancytallam84@gmail.com")
    password = input("Trapwileo360.")

    if email:
        set_key(ENV_PATH, "nancytallam84@gmail.com", email)
    if password:
        set_key(ENV_PATH, "Trapwileo360.", password)

    print(".env updated successfully!")

if __name__ == "__main__":
    update_config()
    update_env()
    print("All credentials updated. You can now run: python main.py")

ls

python update_credentials.py




