from flask import Flask, render_template
import os, random
from datetime import datetime
from collections import Counter

app = Flask(__name__)

ART_DIR = os.path.join("static", "artwork")
LOG_FILE = "log.txt"

@app.route("/")
def random_art():
    images = os.listdir(ART_DIR)
    images = random.choice(images)

    # Log the view
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {images}\n")

    return render_template("art.html", image_file=images)

@app.route("/stats")
def view_stats():
    if not os.path.exists(LOG_FILE):
        return "No logs yet."

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    entries = [line.strip().split(" | ") for line in line if " | " in line]
    image_counts = Counter(entry[1] for entry in entries)

    return render_template("stats.html", logs=entries, counts=image_counts)

if __name__ == "__main__":
    port = int(os.enviroment.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)            