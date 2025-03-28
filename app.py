from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia

app = Flask(__name__)
flag = 1

api = os.getenv("makersuite")
#api = "AIzaSyB_CM06ZBjzAYgX_P6Hw3ezHRAXKdTVCYY"
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

@app.route("/",methods = ["POST","GET"])
def index():
    return (render_template("index.html"))

@app.route("/main",methods = ["POST","GET"])
def main():
    global flag
    if flag ==1:
        user_name = request.form.get("q")
        t= datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?,?)", (user_name, t))
        conn.commit()
        c.close()
        conn.close
        flag = 0

    return (render_template("main.html"))

@app.route("/foodexp",methods = ["POST","GET"])
def foodexp():
    return (render_template("foodexp.html"))

@app.route("/foodexp1",methods = ["POST","GET"])
def foodexp1():
    return (render_template("foodexp1.html"))

@app.route("/foodexp2",methods = ["POST","GET"])
def foodexp2():
    return (render_template("foodexp2.html"))

@app.route("/foodexp_pred",methods = ["POST","GET"])
def foodexp_pred():
    q = float(request.form.get("q")) #float 很重要
    return (render_template("foodexp_pred.html",r=q*0.4851+147.4))

@app.route("/ethical_test",methods = ["POST","GET"])
def ethical_test():
    return (render_template("ethical_test.html"))

@app.route("/test_result",methods = ["POST","GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return (render_template("pass.html"))
    elif answer == "true":
        return (render_template("fail.html"))

@app.route("/FAQ",methods = ["POST","GET"])
def FAQ():
    return (render_template("FAQ.html"))

@app.route("/faq1",methods = ["POST","GET"])
def faq1():
    r = model.generate_content("query: Factors for Profit")

    return (render_template("faq1.html",r=r.candidates[0].content.parts[0]))


@app.route("/FAQ_input",methods = ["POST","GET"])
def FAQ_input():
    q = request.form.get("q") #这里的q如果内容有空格就会internal error
    r = wikipedia.summary(q)
    return (render_template("faq_input.html",r=r))


@app.route("/userlog",methods = ["POST","GET"])
def userlog():

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    r= ""
    for row in c:
        r += str(row) + "\n"
    print(r)
    c.close()
    conn.close

    return (render_template("userlog.html",r=r))

@app.route("/deletelog",methods = ["POST","GET"])
def deletelog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close

    return (render_template("deletelog.html"))



if __name__=="__main__":
    app.run()