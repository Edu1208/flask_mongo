from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://lalo:EduLC@5bpv.kcdyemv.mongodb.net/escuela")
client = MongoClient(MONGO_URI) 
db = client.get_default_database()

def to_str_id(doc):
    if not doc:
        return None
    doc['id'] = str(doc['_id'])      
    return doc

def to_str_list(cursor):
    return [to_str_id(d) for d in cursor]

@app.route("/")
def index():
    alumnos = to_str_list(db.alumnos.find().sort("apellido", 1))
    return render_template("index.html", alumnos=alumnos)

@app.route("/alumnos/new", methods=["GET", "POST"])
def create_alumno():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        edad = request.form.get("edad", "").strip()
        grupo = request.form.get("grupo", "").strip()
        promedio = request.form.get("promedio", "").strip()
        correo = request.form.get("correo", "").strip()
        try:
            promedio = float(promedio) if promedio else None
        except:
            promedio = None

        alumno = {
            "nombre": nombre,
            "edad": int(edad) if edad.isdigit() else None,
            "grupo": grupo,
            "promedio": promedio,
            "correo": correo
        }
        db.alumnos.insert_one(alumno)
        flash("Alumno creado correctamente.", "success")
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/alumnos/<id>")
def view_alumno(id):
    try:
        alumno = db.alumnos.find_one({"_id": ObjectId(id)})
    except:
        alumno = None
    if not alumno:
        flash("Alumno no encontrado.", "danger")
        return redirect(url_for("index"))
    alumno = to_str_id(alumno)
    return render_template("view.html", alumno=alumno)

@app.route("/alumnos/edit/<id>", methods=["GET", "POST"])
def edit_alumno(id):
    try:
        alumno = db.alumnos.find_one({"_id": ObjectId(id)})
    except:
        alumno = None
    if not alumno:
        flash("Alumno no encontrado.", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        edad = request.form.get("edad", "").strip()
        grupo = request.form.get("grupo", "").strip()
        promedio = request.form.get("promedio", "").strip()
        correo = request.form.get("correo", "").strip()
        try:
            promedio = float(promedio) if promedio else None
        except:
            promedio = None
        update = {
            "nombre": nombre,
            "edad": int(edad) if edad.isdigit() else None,
            "grupo": grupo,
            "promedio": promedio,
            "correo": correo
        }
        db.alumnos.update_one({"_id": ObjectId(id)}, {"$set": update})
        flash("Alumno actualizado.", "success")
        return redirect(url_for("index"))
    alumno = to_str_id(alumno)
    return render_template("edit.html", alumno=alumno)

@app.route("/alumnos/delete/<id>", methods=["POST"])
def delete_alumno(id):
    try:
        db.alumnos.delete_one({"_id": ObjectId(id)})
        flash("Alumno eliminado.", "info")
    except Exception as e:
        flash("Error al eliminar: " + str(e), "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
