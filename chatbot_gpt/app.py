# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:27:15 2023

@author: aksha
"""
# https://www.scaler.com/topics/login-page-in-html/
# https://vegibit.com/how-to-use-forms-in-python-flask/#:~:text=Data%20associated%20with%20an%20HTML,args.&text=The%20code%20just%20above%20uses,%3E%2C%20which%20exists%20in%20home.

from flask import request, Flask, render_template, url_for, flash, redirect, session
import pymongo
import datetime
from bson import ObjectId
import chatbot

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
print(myclient.list_database_names())

if 'chats_gpt' not in myclient.list_database_names():
    mydb = myclient["chats_gpt"]
    mycol = mydb["chats"]

app = Flask(__name__)
app.secret_key = "gpt"
app.permanent_session_lifetime = datetime.timedelta(minutes=30)

@app.route("/",  methods=["POST", "GET"])
def home():
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
            user = request.form.get("username")
            if user == None:
                return render_template("login.html")
            else:
                session.permanent = True
                session["user"] = user
                return redirect(url_for("chat"))
	else:
		if "user" in session:
			return redirect(url_for("chat"))

		return render_template("login.html")
    
@app.route("/chat", methods=["POST", "GET"])
def chat():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            message = request.form.get("msger-input")
            datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mydb = myclient["chats_gpt"]
            mycol = mydb["chats"]
            myquery = { "user": user} # common query to be used later
            
            chat_log = ''
            # preparing chat log before sending current user input to mongo
            mydoc = mycol.find(myquery)
            for x in mydoc:
                if x["person"] == user:
                    question = x["message"]
                    chat_log = f'{chat_log}Human: {question}\n'
                elif x["person"] == 'GPT':
                    answer = x["message"]
                    chat_log = f'{chat_log}AI: {answer}\n'
            
            # inserting user input
            mydict = { "user": user, "person": user, "timestamp": datetime_now, "message": message}
            x = mycol.insert_one(mydict)
            # inserting gpt chatbot answer
            answer = chatbot.ask(message, chat_log)
            datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mydict = { "user": user, "person": "GPT", "timestamp": datetime_now, "message": answer}
            x = mycol.insert_one(mydict)
            
            # fetching interaction record for rendering
            mydoc = mycol.find(myquery)
            chats = []
            for x in mydoc:
                chats.append([x["person"], x["message"], x["timestamp"]])
            chats.reverse() # reverse is done to be compatible with reverse flex direction in msger-chat css, so that scroll is at bottom showing latest message. 
            return render_template("chat.html", user = user, chats = chats)
        else:
            starting_message = "Hi, welcome to GPT ChatBot! Go ahead and send me a message. 😄"
            datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chats = []
            chats.append(['GPT', starting_message, datetime_now]) 
            return render_template("chat.html", user = user, chats = chats)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    user = session["user"]
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/delete")
def delete():
    user = session["user"]
    mydb = myclient["chats_gpt"]
    mycol = mydb["chats"]
    myquery = { "user": user}
    mycol.delete_many(myquery)
    return redirect(url_for("chat"))



if __name__ == "__main__":
    app.run(debug=True)