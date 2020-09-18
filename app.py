from flask import render_template
import pymongo
from pymongo import MongoClient
from flask import Flask, request, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/')
db = client['profiles']
collection_student = db['student_coll']
collection_course = db['course_coll']

# Atlas: daniela, crispeta
@app.route("/studentProfile/<idStudent>",  methods=['GET', 'POST'])
def form(idStudent=None):
    uname = str(request.args.get('username'))
    userid = str(idStudent)
    q = collection_student.find_one({"userid": userid})
    if request.method == "POST":
        idioma = request.form.get("idioma")
        formatos = request.form.getlist("formato")
        fuentes = request.form.getlist("fuente")
        dict_user = {"userid": userid, "username": uname, "lang": idioma,
                     "sources": fuentes, "formats": formatos}
        print(dict_user)
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
            return render_template(
                "index_student.html", idStudent=idStudent, username=uname, language=idioma, formats=formatos, sources=fuentes)
    # si hace get y no encuentra nada - renderizar asi>
    return render_template("index_student.html", idStudent=idStudent, username=uname)


@app.route("/favorites/<idCourse>",  methods=['GET', 'POST'])
def favs(idCourse=None):
    cursename = str(request.args.get('coursename'))
    sections = str(request.args.get('section'))
    print(sections)

    # list_rows = [0 for i in list_rows if i == 1]
    list_list_titles = [["hola", "hola2", "hola3"], [
        "second", "secondsito"], ["jijij"], ["lol"]]
    list_list_titles = [[], [], [], []]
    list_rows = [len(i) for i in list_list_titles]
    list_rows = [1 for i in list_rows if i == 0]
    print(list_rows)
    list_sec = ["Generales"]
    if sections != "None":
        if sections[-1] == ",":
            sections = sections[:-1]
        for sec in sections.split(","):
            sec = sec.split("--")
            list_sec.append("Section id " + sec[0] + ": " + sec[1])
    if request.method == "POST":
        counter = str(request.form.getlist("test"))
        print("Counter " + counter)

        if counter != "[]":
            rows = []
            for i in counter.replace("[", "").replace("]", "").split(","):
                rows.append(int(i.replace("/", "").replace("'", '')))
            max_rows = max(rows) + 2
        else:
            max_rows = 1
        print("max rows " + str(max_rows))
        res = []
        for i in range(max_rows):
            if i == 0:
                x = request.form.getlist("title")
            else:
                x = request.form.getlist("title{}".format(i-1))
            res.append(x)
        print("res " + str(res))
        return render_template("favorites_ok.html")

    if request.method == "GET":
        return render_template("favorites.html", idCourse=idCourse, cursename=cursename,
                               number=len(list_sec), sections=list_sec, nrows=list_rows, titles=list_list_titles)
    return render_template("favorites.html", idCourse=idCourse, cursename=cursename, number=len(list_sec), sections=list_sec)


@app.route("/courseProfile/<idCourse>",  methods=['GET', 'POST'])
def formCourse(idCourse=None):
    courseid = str(idCourse)
    uname = str(request.args.get('username'))
    q = collection_course.find_one({"courseid": courseid})
    if request.method == "POST":
        idioma = request.form.get("idioma")
        fuentes = request.form.getlist("fuente")
        dict_course = {"courseid": courseid, "username": uname, "lang": idioma,
                       "sources": fuentes}
        print(dict_course)
        print(q)
        if q:
            print("Updated")
            collection_student.update_one({'_id': q['_id']}, {
                '$set': dict_course}, upsert=False)
        else:
            print("Created")
            collection_course.insert_one(dict_course)
        return render_template("course_ok.html", idCourse=idCourse)

    if request.method == "GET":
        if q:
            idioma = q['lang']
            fuentes = q['sources']
            print(fuentes)

            return render_template(
                "index_course.html", idCourse=idCourse, username=uname, language=idioma, sources=fuentes)
    return render_template("index_course.html", idCourse=idCourse, username=uname)


if __name__ == '__main__':
    app.run()
