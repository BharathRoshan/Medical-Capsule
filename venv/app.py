from flask import Flask, request, render_template

import pyrebase
import json

from blocks import *
import time

config = {

    "apiKey": "AIzaSyDrCSoTsz_iXv7roOlzpKwGBNt1eNCnD9w",
    "authDomain": "test-b69c6.firebaseapp.com",
    "databaseURL": "https://test-b69c6.firebaseio.com",
    "projectId": "test-b69c6",
    "storageBucket": "test-b69c6.appspot.com",
    "messagingSenderId": "664654215644",
    "appId": "1:664654215644:web:40e8a062336771fb1cb719",

}
firebase = pyrebase.initialize_app(config)
fbUserName = None

auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)

firebaseUser = None


@app.route('/', methods=['GET', 'POST'])
def home():
    global firebaseUser, fbUserName

    if request.method == 'POST' and "age" not in request.form:
        email = request.form['email']
        password = request.form['pass']

        try:
            result = auth.sign_in_with_email_and_password(email, password)
            firebaseUser = result
            print("Firebase Result", firebaseUser)

            return render_template('home.html', userName=firebaseUser["email"])
        except Exception as e:
            strError = str(e)
            errorMessage = strError[strError.find("message") + 10:strError.find("errors")].split(',')[0]
            print("Exception", e, errorMessage)
            return render_template('home.html', error=errorMessage)

    elif request.method == 'POST' and "age" in request.form:
        email = request.form['email']
        password = request.form['pass']
        name = request.form['name']
        age = request.form['age']
        dob = request.form['dob']
        aadhar = request.form['aadhar']
        city = request.form['city']
        state = request.form['state']
        pin = request.form['pin']

        try:
            result = auth.create_user_with_email_and_password(email, password)
            firebaseUser = result
            print("Firebase Result", firebaseUser)

            data = {"name": name,
                    "email": email,
                    "age": age,
                    "dob": dob,
                    "aadhar": aadhar,
                    "city": city,
                    "state": state,
                    "pin": pin
                    }
            db.child("users").child(firebaseUser['localId']).set(data)

            fbUserName = db.child("users").child(firebaseUser['localId']).get().val()["name"]
            print("fbUserName", fbUserName)

            data = ""
            for val in db.child("users").child(firebaseUser['localId']).get().val().values():
                data += val

            prevHash = db.child("prevHash").get().val()

            block = MainBlock(str(datetime.datetime.utcnow()), data, prevHash)
            blockData = {"timestamp": str(block.getTimestamp()),
                         "data": block.getData(),
                         "prevHash": block.getPreviousHash(),
                         "hash": block.getHash(),
                         "innerBlocks": block.getInnerBlocks(),
                         "innerPrevHash": block.getInnerPrevHash(),
                         }
            print("93")
            db.child("blocks").child(firebaseUser['localId']).set(block.__dict__)
            print("95")
            db.update({"prevHash": block.getHash()})
            print("97")
            return render_template('home.html', userName=fbUserName)
        except Exception as e:
            strError = str(e)
            errorMessage = strError[strError.find("message") + 10:strError.find("errors")].split(',')[0]
            print("Exception", e, errorMessage)
            return render_template('home.html', error=errorMessage)

    return render_template('home.html')


@app.route('/contactus')
def contactus():
    fbUserName = db.child("users").child(firebaseUser['localId']).get().val()["name"]


    return render_template('contactus.html', userName=fbUserName)


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    time.sleep(2)

    fbUserName = db.child("users").child(firebaseUser['localId']).get().val()["name"]

    if request.method == 'POST':
        treatment = request.form['treatment']
        date = request.form['date']
        hname = request.form['hname']
        symptoms = request.form['symptoms']
        bp = request.form['bp']
        sugar = request.form['sugar']
        weight = request.form['weight']
        docName = request.form['doc']

        record = Record(treatment, str(date), hname, symptoms, bp, sugar, weight, docName)

        try:

            result = db.child("users").child(firebaseUser['localId']).child("history").push(record.__dict__)

            print(result)

            print(db.child("users").child(firebaseUser['localId']).child("history").child(result['name']).get().val())

            recordDataDict = dict(db.child("users").child(firebaseUser['localId']).child("history").child(result['name']).get().val())



            data = ""
            for val in recordDataDict.values():
                data += val #inner_previous_hash
            prevHash = db.child("blocks").child(firebaseUser['localId']).child("innerPrevHash").get().val()

            innerBlock = InnerBlock(str(datetime.datetime.utcnow()), data, prevHash)

            db.child("historyBlocks").child(firebaseUser['localId']).push(innerBlock.__dict__)

            db.child("blocks").child(firebaseUser['localId']).update({"innerPrevHash": innerBlock.getHash()})

            return render_template('home.html', userName=fbUserName)
        except Exception as e:
            strError = str(e)
            errorMessage = strError[strError.find("message") + 10:strError.find("errors")].split(',')[0]
            print("Exception", e, errorMessage)
            return render_template('home.html', error=errorMessage)


    return render_template('upload.html', userName=fbUserName)


@app.route('/history')
def history():
    time.sleep(2)
    fbUserName = db.child("users").child(firebaseUser['localId']).get().val()["name"]

    # user=>id=>history=>get

    history = db.child("users").child(firebaseUser['localId']).child("history").get()

    #print(dict(history.val()))
    historyData = [fbUserName]

    if history is not None:

        for val in dict(history.val()).values():
            historyData.append(val)
        print(historyData)

        return render_template('history.html', data=historyData)
    else:
        return render_template('history.html', data=historyData)




app.run(debug=True)
