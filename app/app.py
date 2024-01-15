from flask import Flask, render_template
import docker
import subprocess

def generate_wireguard_keys():
    privkey = subprocess.check_output("wg genkey", shell=True).decode("utf-8").strip()
    pubkey = subprocess.check_output(f"echo '{privkey}' | wg pubkey", shell=True).decode("utf-8").strip()
    return privkey, pubkey

app = Flask(__name__)

client = docker.DockerClient(base_url="unix://var/run/docker.sock")

@app.route('/')
def index():
    privkey, pubkey = generate_wireguard_keys()
    # return "private: " + privkey + ", public: " + pubkey + "<br />"
    containers = client.containers.list()
    ids = []
    for c in containers:
        ids.append(c.id)
    return { "id": ids }

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
