import json

def create_config(path="config.json"):
    """
    สร้างไฟล์ config.json สำหรับ MT5 credentials
    """
    config = {
        "login": int(input("Enter MT5 login: ")),
        "password": input("Enter MT5 password: "),
        "server": input("Enter MT5 server name: ")
    }
    with open(path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Config saved to {path}")

if __name__ == "__main__":
    create_config()
