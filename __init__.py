from flask import Flask, render_template, request, url_for, redirect, abort
from dbaccess import *

app = Flask(__name__)

session={}

@app.route("/")
def home():
    if "userid" in session:
        return render_template("home.html", signedin=True, id=session['userid'], name=session['name'], type=session['type'])
    return render_template("home.html", signedin=False)

@app.route("/signup/", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        data = request.form
        ok = add_user(data)
        if ok:
            return render_template("success_signup.html")
        return render_template("signup_customer.html", ok=ok)
    return render_template("signup.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        userdat = auth_user(data)
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

@app.route("/viewprofile/<id>/")
def view_profile(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    userid = session["userid"]
    type = session["type"]
    my = True if userid==id else False
    if not my: profile_type = "Customer" if type=="Seller" else "Seller"
    else: profile_type = type

    det, categories = fetch_details(id, profile_type)   #details
    if len(det)==0:
        abort(404)
    det = det[0]
    return render_template("view_profile.html",
                            type=profile_type,
                            name=det[1],
                            email=det[2],
                            phone=det[3],
                            area=det[4],
                            locality=det[5],
                            city=det[6],
                            state=det[7],
                            country=det[8],
                            zip=det[9],
                            category=(None if profile_type=="Customer" else categories),
                            my=my)

@app.route("/viewprofile/", methods=["POST", "GET"])
def profile():
    if 'userid' not in session:
        return redirect(url_for('home'))
    type = "Seller" if session['type']=="Customer" else "Customer"
    if request.method=="POST":
        search = request.form['search']
        results = search_users(search, type)
        found = len(results)
        return render_template('profiles.html', id=session['userid'], type=type, after_srch=True, found=found, results=results)

    return render_template('profiles.html', id=session['userid'], type=type, after_srch=False)

@app.route("/editprofile/", methods=["POST", "GET"])
def edit_profile():
    if 'userid' not in session:
        return redirect(url_for('home'))

    if request.method=="POST":
        data = request.form
        update_details(data, session['userid'], session['type'])
        return redirect(url_for('view_profile', id=session['userid']))

    if request.method=="GET":
        userid = session["userid"]
        type = session["type"]
        det, _ = fetch_details(userid, type)
        det = det[0]
        return render_template("edit_profile.html",
                                name=det[1],
                                email=det[2],
                                phone=det[3],
                                area=det[4],
                                locality=det[5],
                                city=det[6],
                                state=det[7],
                                country=det[8],
                                zip=det[9])

@app.route("/changepassword/", methods=["POST", "GET"])
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

@app.route("/sell/", methods=["POST", "GET"])
def my_products():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session["type"]=="Customer":
        abort(403)
    categories = get_categories(session["userid"])
    if request.method=="POST":
        data = request.form
        srchBy = data["search method"]
        category = None if srchBy=='by keyword' else data["category"]
        keyword = data["keyword"]
        results = search_myproduct(session['userid'], srchBy, category, keyword)
        return render_template('my_products.html', categories=categories, after_srch=True, results=results)
    return render_template("my_products.html", categories=categories, after_srch=False)

@app.route("/sell/addproducts/", methods=["POST", "GET"])
def add_products():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session["type"]=="Customer":
        abort(403)
    if request.method=="POST":
        data = request.form
        add_prod(session['userid'],data)
        return redirect(url_for('my_products'))
    return render_template("add_products.html")

@app.route("/viewproduct/")
def view_prod():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Seller":
        return redirect(url_for('my_products'))
    if session['type']=="Customer":
        return redirect(url_for('buy'))

@app.route("/viewproduct/<id>/")
def view_product(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    type = session["type"]
    ispresent, tup = get_product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if type=="Seller" and sellID!=session['userid']:
        abort(403)
    return render_template('view_product.html', type=type, name=name, quantity=quantity, category=category, cost_price=cost_price, sell_price=sell_price, sell_id=sellID, sell_name=sell_name, desp=desp, prod_id=id)

@app.route("/viewproduct/<id>/edit/", methods=["POST", "GET"])
def edit_product(id):
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Customer":
        abort(403)
    ispresent, tup = get_product_info(id)
    if not ispresent:
        abort(404)
    (name, quantity, category, cost_price, sell_price, sellID, desp, sell_name) = tup
    if sellID!=session['userid']:
        abort(403)
    if request.method=="POST":
        data = request.form
        update_product(data, id)
        return redirect(url_for('view_product', id=id))
    return render_template('edit_product.html', prodID=id, name=name, qty=quantity, category=category, price=cost_price, desp=desp)

@app.route("/buy/", methods=["POST", "GET"])
def buy():
    if 'userid' not in session:
        return redirect(url_for('home'))
    if session['type']=="Seller":
        abort(403)
    if request.method=="POST":
        data = request.form
        srchBy = data["search method"]
        category = None if srchBy=='by keyword' else data["category"]
        keyword = data["keyword"]
        results = search_products(srchBy, category, keyword)
        return render_template('search_products.html', after_srch=True, results=results)
    return render_template('search_products.html', after_srch=False)

#@app.route("/buy/<id>/")

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True)
