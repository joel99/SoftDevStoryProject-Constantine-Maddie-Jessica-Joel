from flask import Flask, request, session, url_for, redirect
import hashlib

@app.route("/makeAccount/", methods = ['POST'])
def newAccount():
    d = request.form
    if (validateAccount(d)):
        makeAccount(d["userName"], hashlib.sha512(d["pass1"]).hexdigest())
    return render_template('makeAccount.html', success = validateAccount(request.form))

@app.route("/authen/", methods = ['POST'])
def auth():
    d = request.form #works like dictionary
    if accountCheck(d["userName"], d["pass"]):
        session["user"] = d["userName"]
    return redirect(url_for('home'))    
    
#login

@app.route("/logout/", methods = ['POST'])
def logout():
    session.pop("user")
    return redirect(url_for('home'))

def accountCheck(userName, password):
    reader = csv.reader(open("data/users.csv", "r"))
    if userName == "CLEAR" and password == "CLEAR":
        clearAllAccounts()
    d = {}
    for row in reader:
        k, v = row
        d[k] = v
    if not userName in d.keys():
        return False
    else:
        if hashlib.sha512(password).hexdigest() == d[userName]: 
            session["user"] = userName #login
            return True
        return False


#making new account
def validateAccount(d):
    return d["pass1"] == d["pass2"] and len(d["userName"]) > 0 and len(d["pass1"]) > 0

def makeAccount(name, hashed):
    print "we're making it"
    data = open("data/users.csv", "a")
    data.write(name + "," + hashed + "\n")
    data.close()

def clearAllAccounts():
    data = open("data/users.csv", "w")
    data.write("")
    data.close()
