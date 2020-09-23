from flask import render_template
import pymongo
from pymongo import MongoClient
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from itertools import groupby


app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://daniela:crispeta@cluster0.t3xek.mongodb.net/')
db = client['profiles']
collection_student = db['student_coll']
collection_course = db['course_coll']
dbfavs = client['favorites']
collection_favs = dbfavs['favoritescoll']


@app.route("/studentProfile/<idStudent>",  methods=['GET', 'POST'])
def form(idStudent=None):
    uname = str(request.args.get('username'))
    userid = str(idStudent)
    fname = str(request.args.get('firstname'))
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
                "index_student.html", idStudent=idStudent, firstname=fname, language=idioma, formats=formatos, sources=fuentes)
    return render_template("index_student.html", idStudent=idStudent, username=uname)


@app.route("/favorites/<idCourse>",  methods=['GET', 'POST'])
def favs(idCourse=None):
    list_sec = ["Generales"]
    ids = ["0"]
    cursename = str(request.args.get('coursename'))
    sections = str(request.args.get('section'))
    if sections != "None":
        if sections[-1] == ",":
            sections = sections[:-1]
        for sec in sections.split(","):
            sec = sec.split("--")
            list_sec.append("Section id " + sec[0] + ": " + sec[1])
            ids.append(str(sec[0]))
    q = collection_favs.find({"courseid": idCourse})
    result = list(q)

    if request.method == "POST":
        ids = (request.args.get('idsSections')).split(",")  # get ids from url
        dict_value_titles = {}  # {numsections : list of titles}
        dict_value_urls = {}
        for i in range(len(ids)):
            x = request.form.getlist("title{}".format(i))
            y = request.form.getlist("url{}".format(i))
            dict_value_titles[ids[i]] = x
            dict_value_urls[ids[i]] = y
        l = []
        for i in dict_value_titles.keys():
            titles = dict_value_titles[i]
            urls = dict_value_urls[i]
            section = []
            for t in range(len(titles)):
                if (titles[t] != "" and urls[t] != ""):
                    section.append(
                        {"courseid": idCourse, "sectionid": i, "title": titles[t], "url": urls[t]})
            l.append(section)
        flat_list = [item for sublist in l for item in sublist]
        # Insert in mongo DB
        print(flat_list)
        if result:  # If no hay nada de ese curso en la db
            collection_favs.delete_many({"courseid": idCourse})
        if flat_list:
            collection_favs.insert_many(flat_list)
        return render_template("favorites_ok.html")

    if request.method == "GET":
        result.sort(key=lambda x: x['sectionid'])
        grouped_dict = {}
        for k, v in groupby(result, key=lambda x: x['sectionid'][:7]):
            grouped_dict[k] = list(v)
        list_list_titles = []
        list_list_urls = []
        for i in ids:
            if grouped_dict.get(i):
                list_list_titles.append([doc['title']
                                         for doc in grouped_dict.get(i)])
                list_list_urls.append([doc['url']
                                       for doc in grouped_dict.get(i)])
            else:
                list_list_titles.append([])
                list_list_urls.append([])
        list_rows = [len(i) for i in list_list_titles]
        list_rows = [1 if x == 0 else x for x in list_rows]
        return render_template("favorites.html", idCourse=idCourse, cursename=cursename,
                               number=len(list_sec), sections=list_sec, nrows=list_rows, titles=list_list_titles, urls=list_list_urls, ids=",".join(ids))
    return render_template("favorites.html", idCourse=idCourse, cursename=cursename, number=len(list_sec), sections=list_sec, ids=",".join(ids))


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
