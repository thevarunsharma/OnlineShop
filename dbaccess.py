import sqlite3
from pickle import load, dump
import os

with open("metadata.bin","rb") as fh:
    metadata = load(fh)

def edit_metadata(metadata):
    with open("newfile.bin", "wb") as fh:
        dump(metadata, fh)
    os.remove("metadata.bin")
    os.rename("newfile.bin", "metadata.bin")

def gen_custID(metadata):
    metadata["custnum"] += 1
    edit_metadata(metadata)
    custnum = str(metadata["custnum"])
    id = "CID"+"0"*(7-len(custnum))+custnum
    return id

def gen_sellID(metadata):
    metadata["sellnum"] += 1
    edit_metadata(metadata)
    sellnum = str(metadata["sellnum"])
    id = "SID"+"0"*(7-len(sellnum))+sellnum
    return id

def add_customer(data):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    email = data["email"]
    a = cur.execute("SELECT * FROM customer WHERE email=?", (email,))
    if len(list(a))!=0:
        return False
    tup = (gen_custID(metadata),
            data["name"],
            data["email"],
            data["phone"],
            data["area"],
            data["locality"],
            data["city"],
            data["state"],
            data["country"],
            data["zip"],
            data["password"])
    cur.execute("INSERT INTO customer VALUES (?,?,?,?,?,?,?,?,?,?,?)", tup)
    conn.commit()
    conn.close()
    return True

def add_seller(data):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    email = data["email"]
    a = cur.execute("SELECT * FROM seller WHERE email=?", (email,))
    if len(list(a))!=0:
        return False
    tup = (gen_sellID(metadata),
            data["name"],
            data["email"],
            data["phone"],
            data["area"],
            data["locality"],
            data["city"],
            data["state"],
            data["country"],
            data["zip"],
            data["password"],
            data["category"])
    cur.execute("INSERT INTO seller VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", tup)
    conn.commit()
    conn.close()
    return True

def auth_customer(data):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    type = data["type"]
    email = data["email"]
    password = data["password"]
    print(email, password)
    if type=="Customer":
        a = cur.execute("SELECT custID, name FROM customer WHERE email=? AND password=?", (email, password))
    elif type=="Seller":
        a = cur.execute("SELECT sellID, name FROM seller WHERE email=? AND password=?", (email, password))
    a = list(a)
    conn.close()
    if len(a)==0:
        return False
    return a[0]

def fetch_details(userid, type):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        a = cur.execute("SELECT * FROM customer WHERE custID=?", (userid,))
    elif type=="Seller":
        a = cur.execute("SELECT * FROM seller WHERE sellID=?", (userid,))
    a = list(a)[0]
    conn.close()
    return a

def update_details(data, userid, type):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        cur.execute("UPDATE customer SET phone=?, area=?, locality=?, city=?, state=?, country=?, zipcode=? where custID=?", (data["phone"],
                    data["area"],
                    data["locality"],
                    data["city"],
                    data["state"],
                    data["country"],
                    data["zip"],
                    userid))
    elif type=="Seller":
        cur.execute("UPDATE seller SET phone=?, area=?, locality=?, city=?, state=?, country=?, zipcode=? where sellID=?", (data["phone"],
                    data["area"],
                    data["locality"],
                    data["city"],
                    data["state"],
                    data["country"],
                    data["zip"],
                    userid))
    conn.commit()
    conn.close()

def check_psswd(psswd, userid, type):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        a = cur.execute("SELECT password FROM customer WHERE custID=?", (userid,))
    elif type=="Seller":
        a = cur.execute("SELECT password FROM seller WHERE sellID=?", (userid,))
    real_psswd = list(a)[0][0]
    conn.close()
    return psswd==real_psswd

def set_psswd(psswd, userid, type):
    conn = sqlite3.connect("onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        a = cur.execute("UPDATE customer SET password=? WHERE custID=?", (psswd, userid))
    elif type=="Seller":
        a = cur.execute("UPDATE seller SET password=? WHERE sellID=?", (psswd, userid))
    conn.commit()
    conn.close()
