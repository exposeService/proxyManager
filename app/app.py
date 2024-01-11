from flask import Flask, render_template
import subprocess

def generate_wireguard_keys():
    privkey = subprocess.check_output("wg genkey", shell=True).decode("utf-8").strip()
    pubkey = subprocess.check_output(f"echo '{privkey}' | wg pubkey", shell=True).decode("utf-8").strip()
    return privkey, pubkey

app = Flask(__name__)

@app.route('/')
def index():
    privkey, pubkey = generate_wireguard_keys()
    return "private: " + privkey + ", public: " + pubkey

if __name__ == '__main__':
    app.run()
