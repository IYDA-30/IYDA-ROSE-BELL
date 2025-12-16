from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from models import db, Event, Resource, EventResourceAllocation

app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db.init_app(app)

# ---------------- HOME ----------------
@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html", show_navbar=False)

# ---------------- HELPERS ----------------
def is_conflict(resource_id, start, end):
    allocations = EventResourceAllocation.query.filter_by(resource_id=resource_id).all()
    for alloc in allocations:
        event = Event.query.get(alloc.event_id)
        if start < event.end_time and end > event.start_time:
            return True
    return False

# ---------------- EVENTS ----------------
@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        e = Event(
            name=request.form["name"],
            start_time=datetime.fromisoformat(request.form["start"]),
            end_time=datetime.fromisoformat(request.form["end"])
        )
        db.session.add(e)
        db.session.commit()
        flash("✅ Event Added")

    return render_template(
        "events.html",
        events=Event.query.all(),
        show_navbar=True
    )

@app.route("/delete_event/<int:event_id>")
def delete_event(event_id):
    EventResourceAllocation.query.filter_by(event_id=event_id).delete()
    Event.query.filter_by(id=event_id).delete()
    db.session.commit()
    flash("🗑️ Event Deleted")
    return redirect("/events")

# ---------------- RESOURCES ----------------
@app.route("/resources", methods=["GET", "POST"])
def resources():
    if request.method == "POST":
        r = Resource(
            name=request.form["name"],
            type=request.form["type"]
        )
        db.session.add(r)
        db.session.commit()
        flash("✅ Resource Added")

    return render_template(
        "resources.html",
        resources=Resource.query.all(),
        show_navbar=True
    )

@app.route("/delete_resource/<int:resource_id>")
def delete_resource(resource_id):
    EventResourceAllocation.query.filter_by(resource_id=resource_id).delete()
    Resource.query.filter_by(id=resource_id).delete()
    db.session.commit()
    flash("🗑️ Resource Deleted")
    return redirect("/resources")

# ---------------- ALLOCATE ----------------
@app.route("/allocate", methods=["GET", "POST"])
def allocate():
    if request.method == "POST":
        event_id = int(request.form["event"])
        resource_id = int(request.form["resource"])
        event = Event.query.get(event_id)

        if is_conflict(resource_id, event.start_time, event.end_time):
            flash("❌ Resource conflict detected!")
        else:
            alloc = EventResourceAllocation(
                event_id=event_id,
                resource_id=resource_id
            )
            db.session.add(alloc)
            db.session.commit()
            flash("✅ Resource allocated")

    return render_template(
        "allocate.html",
        events=Event.query.all(),
        resources=Resource.query.all(),
        show_navbar=True
    )

# ---------------- REPORT ----------------
@app.route("/report")
def report():
    WEEK_HOURS = 168
    data = []

    for r in Resource.query.all():
        used_hours = 0
        allocations = EventResourceAllocation.query.filter_by(resource_id=r.id).all()

        for a in allocations:
            event = Event.query.get(a.event_id)
            if event:
                used_hours += (event.end_time - event.start_time).total_seconds() / 3600

        free_hours = max(WEEK_HOURS - used_hours, 0)
        utilization = round((used_hours / WEEK_HOURS) * 100, 2)

        data.append({
            "resource": r.name,
            "used": round(used_hours, 2),
            "free": round(free_hours, 2),
            "utilization": utilization
        })

    return render_template("report.html", data=data, show_navbar=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
