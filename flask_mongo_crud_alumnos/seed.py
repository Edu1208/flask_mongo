from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/escuela")
client = MongoClient(MONGO_URI)
db = client.get_default_database()

db.alumnos.delete_many({})

alumnos = [
    {"nombre": "Edgar López", "edad": 16, "grupo": "3A", "promedio": 8.7, "correo":"edgarlopezelnegrito@gmail.com"},
    {"nombre": "Angel Polito", "edad": 17, "grupo": "3B", "promedio": 7.9,"correo":"angelpolitoaliaselnose@gmail.com"},
    {"nombre": " Eduardo López ", "edad": 15, "grupo": "2A", "promedio": 9.2,"correo":"caneduardoviciadoalclash@gmail.com"},

]

db.alumnos.insert_many(alumnos)
print("Seed completado. Registros insertados:", db.alumnos.count_documents({}))
