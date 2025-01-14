import calendar
from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from custom_filters import format_date

app = Flask(__name__)
app.secret = "mysecret"
app.config["SECRET_KEY"] = "mysecret"
app.jinja_env.filters["format_date"] = format_date


def get_day_data(date):
    day_data = {
        "date": date.strftime("%Y-%m-%d"),
        "day_name": date.strftime("%A"),
    }
    return day_data


@app.route("/save_date/<string:selected_date>", methods=["POST"])
def save_date(selected_date):

    session["selected_date"] = selected_date
    session.modified = True
    current_date = datetime.strptime(session.get("current_date"), "%Y-%m-%d")
    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)
    # current_date = datetime.strptime(selected_date, "%Y-%m-%d")

    print(f"Saved date: {selected_date}")
    context = {
        "days": session.get("days"),
        "prev_date": prev_date.date().isoformat(),
        "current_date": current_date.date().isoformat(),
        "next_date": next_date.date().isoformat(),
        "selected_date": selected_date,
    }
    print(context)
    return render_template("calendar.html", **context)


@app.route("/calendar/<string:date_str>", methods=["GET"])
def get_calendar(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    days = [get_day_data(date + timedelta(days=i)) for i in range(-1, 2)]
    session["days"] = days
    session.modified = True
    session["current_date"] = date.date().isoformat()
    if "selected_date" not in session:
        middle_date = date + timedelta(days=1)
        session["selected_date"] = middle_date.date().isoformat()

    context = {
        "days": days,
        "prev_date": (date - timedelta(days=1)).date().isoformat(),
        "current_date": date.date().isoformat(),
        "next_date": (date + timedelta(days=1)).date().isoformat(),
        "selected_date": session.get("selected_date"),
    }

    return render_template("calendar.html", **context)


@app.route("/", methods=["GET"])
def get_3day_calendar():
    # get the current date from the session
    date_str = session.get("current_date", None)
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()
    days = [get_day_data(date + timedelta(days=i)) for i in range(-1, 2)]
    session["days"] = days
    session.modified = True
    session["current_date"] = date.date().isoformat()

    context = {
        "days": days,
        "prev_date": (date - timedelta(days=1)).date().isoformat(),
        "current_date": date.date().isoformat(),
        "next_date": (date + timedelta(days=1)).date().isoformat(),
        "selected_date": session.get("selected_date"),
    }

    return render_template("index.html", **context)


@app.route("/prev-day", methods=["GET"])
def get_prev_day():
    # get the current date from the session
    date_str = session.get("current_date", datetime.now().date().isoformat())
    if date_str:
        prev_day = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        prev_day = datetime.now()
    prev_day = prev_day - timedelta(days=1)  # change this to 3 days so that we can see the previous 3 days

    days = [get_day_data(prev_day + timedelta(days=i)) for i in range(-1, 2)]
    session["days"] = days
    session.modified = True
    session["current_date"] = prev_day.date().isoformat()

    print(prev_day.date().isoformat())

    context = {
        "days": days,
        "prev_date": (prev_day - timedelta(days=1)).date().isoformat(),  # "prev_date": "2021-09-01
        "current_date": prev_day.date().isoformat(),
        "next_date": (prev_day + timedelta(days=1)).date().isoformat(),
        "selected_date": session.get("selected_date"),
    }
    return render_template("calendar.html", **context)


@app.route("/next-day", methods=["GET"])
def get_next_day():
    # get the current date from the session
    date_str = session.get("current_date", datetime.now().date().isoformat())
    if date_str:
        next_day = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        next_day = datetime.now()
    next_day = next_day + timedelta(
        days=1
    )  # change this to 3 days so that we can see the next 3 days

    days = [get_day_data(next_day + timedelta(days=i)) for i in range(-1, 2)]
    session["days"] = days
    session.modified = True
    session["current_date"] = next_day.date().isoformat()

    print(next_day.date().isoformat())

    context = {
        "days": days,
        "prev_date": (next_day - timedelta(days=1)).date().isoformat(),
        "current_date": next_day.date().isoformat(),
        "next_date": (next_day + timedelta(days=1)).date().isoformat(),
        "selected_date": session.get("selected_date"),
    }
    return render_template("calendar.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
