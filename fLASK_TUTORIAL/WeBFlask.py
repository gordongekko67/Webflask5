from flask import Flask
from flask_restful import Resource, Api

from flask import Flask, render_template, request, jsonify
from flask_restful import fields, marshal_with, Resource, Api, reqparse
import simplejson
import requests
import cgi
import pymongo
import  paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time, json

Connected = False   #global variable for the state of the connection
count = 0
x = 0

# Create the API
app = Flask(__name__)
api = Api(app)

@app.route('/pagina1', methods=['GET', 'POST'])
def test():
    if request.method=='GET':
        print("ricevuto get")
        return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        esito = controllo_database(username,password)
        if (esito == "ok"):
            return render_template('scelta.html')
        else:
            return render_template('home.html')
        return ("ok")
    else:
        return("ok")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inserimento')
def template():
    return render_template('inserimento.html')

@app.route('/person')
def hello():
    return jsonify({'name':'Jimit',
                    'address':'India'})

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method=='POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydb"]
        mycol = mydb["libri"]
        mydict = {"titolo": titolo, "autore": autore}
        x = mycol.insert_one(mydict)
    return render_template('scelta.html')

@app.route('/chiamataREST', methods=['GET', 'POST'])
def chiamataREST():
    return "Chiamata REST"

def sendmsgMqtt():
    # inizialize MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("fkjqkoul", "wK0aUWpQWS35")
    client.connect("tailor.cloudmqtt.com", 16434, 60)
    client.subscribe("Tutorial2/#", 1)
    #client.publish("Tutorial2", "Getting started with MQTT TEST")
    client.publish("Tutorial2", "avanti")

@app.route('/robotAvanti', methods=['GET', 'POST'])
def robotAvanti():
    if request.method == 'GET':
        sendmsgMqtt()
    return render_template('scelta.html')


def controllo_database(username1, password1):
    result  = "no"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydb"]
    mycol = mydb["Utenti"]

    myquery1 = {"username": username1}
    myquery2 = {"password": password1}
    mydoc1 = mycol.find(myquery1)
    mydoc2 = mycol.find(myquery2)
    for x in mydoc1:
        for y in mydoc2:
            result = "ok"
    return result



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Tutorial2/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    if msg.payload.decode() == "prova":
        print("Robot avanti")

def on_publish(client, userdata, msg):
    print("Message published-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

 
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        print("questo e' il post")
        return {'hello': 'post1'}


class Libro(Resource):
    def get(self):
        print("ho ricevuto un get")

        return {'message': 'Success'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('titolo', required=True)
        parser.add_argument('autore', required=True)
        # Parse the arguments into an object
        args = parser.parse_args()
        print(args["titolo"])

api.add_resource(HelloWorld, '/prova')
api.add_resource(Libro, '/libro')

if __name__ == '__main__':
    app.run(debug=True)




