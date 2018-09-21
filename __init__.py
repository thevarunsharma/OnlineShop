from flask import Flask, render_template, request, url_for, redirect
from dbaccess import *

app = Flask(__name__)

session={}

@app.route("/")
def home():
    if "userid" in session:
        return render_template("home.html", signedin=True, name=session['name'], type=session['type'])
    return render_template("home.html", signedin=False)

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/signup/customer/", methods = ["POST", "GET"])
def signup_customer():
    if request.method == "POST":
        data = request.form
        ok = add_customer(data)
        if ok:
            return render_template("success_signup.html")
        return render_template("signup_customer.html", ok=ok)
    return render_template("signup_customer.html", ok=True)

@app.route("/signup/seller/", methods = ["POST", "GET"])
def signup_seller():
    if request.method == "POST":
        data = request.form
        ok = add_seller(data)
        if ok:
            return render_template("success_signup.html")
        return render_template("signup_seller.html", ok=ok)
    return render_template("signup_seller.html", ok=True)

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        userdat = auth_customer(data)
        if userdat:
            session["userid"] = userdat[0]
            session["name"] = userdat[1]
            session["type"] = data["type"]
            return redirect(url_for('home'))
        return render_template("login.html", err=True)
    return render_template("login.html", err=False)

@app.route("/logout/")
def logout():
    global session
    session = {}
    return redirect(url_for('home'))

@app.route("/view/")
def view_profile():
    if 'userid' not in session:
        return redirect(url_for('home'))
    userid = session["userid"]
    type = session["type"]
    det = fetch_details(userid, type)
    return render_template("view_profile.html",
                            name=det[1],
                            email=det[2],
                            phone=det[3],
                            area=det[4],
                            locality=det[5],
                            city=det[6],
                            state=det[7],
                            country=det[8],
                            zip=det[9],
                            category=(None if type=="Customer" else det[11]))

@app.route("/edit/", methods=["POST", "GET"])
def edit_profile():
    if 'userid' not in session:
        return redirect(url_for('home'))

    if request.method=="POST":
        data = request.form
        update_details(data, session['userid'], session['type'])
        return redirect(url_for('view_profile'))

    if request.method=="GET":
        userid = session["userid"]
        type = session["type"]
        det = fetch_details(userid, type)
        return render_template("edit_profile.html",
                                name=det[1],
                                email=det[2],
                                phone=det[3],
                                area=det[4],
                                locality=det[5],
                                city=det[6],
                                state=det[7],
                                country=det[8],
                                zip=det[9],
                                category=(None if type=="Customer" else det[11]))

@app.route("/changepassword", methods=["POST", "GET"])
def change_password():
    if 'userid' not in session:
        return redirect(url_for('home'))
    check = True
    equal = True
    if request.method=="POST":
        userid = session["userid"]
        type = session["type"]
        old_psswd = request.form["old_psswd"]
        new_psswd = request.form["new_psswd"]
        cnfrm_psswd = request.form["cnfrm_psswd"]
        check = check_psswd(old_psswd, userid, type)
        if check:
            equal = (new_psswd == cnfrm_psswd)
            if equal:
                set_psswd(new_psswd, userid, type)
                return redirect(url_for('home'))
    return render_template("change_password.html", check=check, equal=equal)


app.run(debug=True)
