from flask import Flask, render_template, request
from fetch_data import fetch_air_quality
from database_operations import save_to_database

import os

app = Flask(__name__,
            template_folder=os.path.abspath("frontend/templates"),
            static_folder=os.path.abspath("frontend/static"))


@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city").strip()

        if not city:
            error = "⚠️ Please enter a city name."
        else:
            data, error = fetch_air_quality(city)

            if data:
                save_to_database(data)

    return render_template("index.html", data=data, error=error)


if __name__ == "__main__":
    app.run(debug=True)
