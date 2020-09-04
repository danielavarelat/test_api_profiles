from flask import render_template
import pymongo
from pymongo import MongoClient
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
# Para forms
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired

app = Flask(__name__)
print(app)
# app.config["MONGO_URI"] = 'mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/profiles'
# mongo = PyMongo(app)
client = MongoClient(
    'mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/')
db = client['profiles']
collection = db['student_coll']

# Atlas: daniela, crispeta
# mongo = pymongo.MongoClient('mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/studentDB', maxPoolSize=50, connect=False)


@app.route("/studentProfile/<idStudent>",  methods=['GET', 'POST'])
def form(idStudent=None):
    userid = str(idStudent)
    q = collection.find_one({"userid": userid})

    if request.method == "POST":
        idioma = request.form.getlist("idioma")[0]
        formatos = request.form.getlist("formato")
        fuentes = request.form.getlist("fuente")
        dict_user = {"userid": userid, "lang": idioma,
                     "sources": fuentes, "formats": formatos}
        print(dict_user)
        print(q)
        if q:
            print("Updated")
            collection.update_one({'_id': q['_id']}, {
                                  '$set': dict_user}, upsert=False)
        else:
            print("Created")
            collection.insert_one(dict_user)
        return "PROFILE OK"
    if request.method == "GET":
        if q:
            idioma = q['lang']
            formatos = q['formats']
            fuentes = q['sources']
            print(fuentes)

            return render_template(
                "index.html", idStudent=idStudent, language=idioma, formats=formatos, sources=fuentes)
    return render_template("index.html", idStudent=idStudent)


@app.route('/created')
def studentLink():
    return "OK"


if __name__ == '__main__':
    app.run()

# @app.route("/studentProfile/<idStudent>", methods=['GET', 'POST'])
# def readForm():
#     if request.method == "POST":
#         print(request.form.get("lang"))
#         return "DONE"
#     return render_template("index.html")
    # Pregunta 1
    # idioma = request.values.get("idioma")
    # if request.method == 'POST':
    #     print("OK")
    #     print(request.form.get('hello'))
    # print(request.form.getlist("idioma"))

    # Pregunta 2
    # for i in (range(6)+1):
    #     ii = str("formato"+i)
    #     formatos.append(request.values.get("ii"))

    # Pregunta 3
    # for i in (range(5)+1):
    #     ii = str("fuente"+i)
    #     fuentes.append(request.values.get("ii"))

    # todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
    # return redirect("/home")
