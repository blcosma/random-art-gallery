from flask import Flask, render_template, request
import os
import random
import datetime

app = Flask(__name__)

# Path to my art
IMAGE_FOLDER = "static/artwork"
images = os.listdir(IMAGE_FOLDER)
# Keep track of last shown image to avoid repeats
last_image = None
# log file Location
LOG_FILE = "log.txt"

@app.route("/")
def random_art():
    global last_image

    if not images:
        return "No images found", 404

    # Pick a random image, avoid immediate repetition
    if len(images) > 1:
        img = random.choice([i for i in images if i != last_image])
    else:
        img = images[0]

    last_image = img    

    # Log the view
    log_entry = f"{datetime.datetime.now()} | {img} | IP: {request.remote_addr} | Agent: {request.user_agent}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    return render_template("art.html", image_file=img)

# Route to check healt
@app.route("/healt")
def healt_check():
    return "OK", 200

# View stats 
@app.route("/stats")
def view_stats():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readline()
    except FileNotFoundError:
        logs = []
    return "<br>".json(logs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)