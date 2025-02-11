from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "contacts.json"

# Load contacts from JSON file
def load_contacts():
    if not os.path.exists(DATA_FILE):
        return {"contacts": []}
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"contacts": []}

# Save contacts to JSON file
def save_contacts(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    data = load_contacts()
    return render_template("index.html", contacts=data["contacts"])

@app.route("/show/<int:index>")
def show_contact(index):
    data = load_contacts()
    if index < len(data["contacts"]):
        contact = data["contacts"][index]
        return render_template("show.html", userdetails=contact, indexNo=index)
    return "Contact not found", 404

@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        new_contact = {"name": name, "phone": phone, "email": email, "address": address}
        data = load_contacts()
        data["contacts"].append(new_contact)
        save_contacts(data)

        return redirect(url_for("index"))

    return render_template("add_contact.html")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_contact(index):
    data = load_contacts()
    if request.method == "POST":
        data["contacts"][index]["name"] = request.form["name"]
        data["contacts"][index]["phone"] = request.form["phone"]
        data["contacts"][index]["email"] = request.form["email"]
        data["contacts"][index]["address"] = request.form["address"]
        save_contacts(data)
        return redirect(url_for("index"))

    contact = data["contacts"][index]
    return render_template("edit_contact.html", contact=contact, index=index)

@app.route("/delete/<int:index>")
def delete_contact(index):
    data = load_contacts()
    if index < len(data["contacts"]):
        data["contacts"].pop(index)
        save_contacts(data)
    return redirect(url_for("index"))

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").lower()
    data = load_contacts()
    results = [c for c in data["contacts"] if query in c["name"].lower() or query in c["phone"]]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True )
