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

client = MongoClient(
    'mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/')
db = client['profiles']
collection_student = db['student_coll']
collection_course = db['course_coll']

# Atlas: daniela, crispeta
# mongo = pymongo.MongoClient('mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/studentDB', maxPoolSize=50, connect=False)


@app.route("/studentProfile/<idStudent>",  methods=['GET', 'POST'])
def form(idStudent=None):
    userid = str(idStudent)
    q = collection_student.find_one({"userid": userid})

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
            collection_student.update_one({'_id': q['_id']}, {
                                  '$set': dict_user}, upsert=False)
        else:
            print("Created")
            collection_student.insert_one(dict_user)
        return render_template("student_ok.html", idStudent=idStudent)


    if request.method == "GET":
        if q:
            idioma = q['lang']
            formatos = q['formats']
            fuentes = q['sources']
            print(fuentes)

            return render_template(
                "index_student.html", idStudent=idStudent, language=idioma, formats=formatos, sources=fuentes)

    return render_template("index_student.html", idStudent=idStudent)


@app.route("/courseProfile/<idCourse>",  methods=['GET', 'POST'])
def formCourse(idCourse=None):
    courseid = str(idCourse)
    #q = collection_course.find_one({"courseid": courseid})

    return render_template("index_course.html", idCourse=idCourse)


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
