import sqlite3

def gen_custID():
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET custnum = custnum + 1")
    conn.commit()
    custnum = str([i for i in cur.execute("SELECT custnum FROM metadata")][0][0])
    conn.close()
    id = "CID"+"0"*(7-len(custnum))+custnum
    return id

def gen_sellID():
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET sellnum = sellnum + 1")
    conn.commit()
    sellnum = str([i for i in cur.execute("SELECT sellnum FROM metadata")][0][0])
    conn.close()
    id = "SID"+"0"*(7-len(sellnum))+sellnum
    return id

def gen_prodID():
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET prodnum = prodnum + 1")
    conn.commit()
    prodnum = str([i for i in cur.execute("SELECT prodnum FROM metadata")][0][0])
    conn.close()
    id = "PID"+"0"*(7-len(prodnum))+prodnum
    return id

def gen_orderID():
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    cur.execute("UPDATE metadata SET ordernum = ordernum + 1")
    conn.commit()
    ordernum = str([i for i in cur.execute("SELECT ordernum FROM metadata")][0][0])
    conn.close()
    id = "OID"+"0"*(7-len(ordernum))+ ordernum
    return id

def add_user(data):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    email = data["email"]
    if data['type']=="Customer":
        a = cur.execute("SELECT * FROM customer WHERE email=?", (email,))
    elif data['type']=="Seller":
        a = cur.execute("SELECT * FROM seller WHERE email=?", (email,))
    if len(list(a))!=0:
        return False
    tup = ( data["name"],
            data["email"],
            data["phone"],
            data["area"],
            data["locality"],
            data["city"],
            data["state"],
            data["country"],
            data["zip"],
            data["password"])
    if data['type']=="Customer":
        cur.execute("INSERT INTO customer VALUES (?,?,?,?,?,?,?,?,?,?,?)",(gen_custID(), *tup))
    elif data['type']=="Seller":
        cur.execute("INSERT INTO seller VALUES (?,?,?,?,?,?,?,?,?,?,?)", (gen_sellID(), *tup))
    conn.commit()
    conn.close()
    return True

def auth_user(data):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    type = data["type"]
    email = data["email"]
    password = data["password"]
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
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        a = cur.execute("SELECT * FROM customer WHERE custID=?", (userid,))
        a = list(a)
        b = []
    elif type=="Seller":
        a = cur.execute("SELECT * FROM seller WHERE sellID=?", (userid,))
        a = list(a)
        b = cur.execute("SELECT DISTINCT(category) from product WHERE sellID=?", (userid,))
        b = [i[0] for i in b ]
    conn.close()
    return a, b

def search_users(search, srch_type):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    search = "%"+search+"%"
    if srch_type=="Customer":
        res = cur.execute("SELECT custID, name, email, phone, area, locality, city, state, country, zipcode FROM customer WHERE LOWER(name) like ?", (search,))
    elif srch_type=="Seller":
        res = cur.execute("SELECT sellID, name, email, phone, area, locality, city, state, country, zipcode FROM seller WHERE LOWER(name) like ?", (search,))
    res = [i for i in res ]
    conn.close()
    return res

def update_details(data, userid, type):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
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
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        a = cur.execute("SELECT password FROM customer WHERE custID=?", (userid,))
    elif type=="Seller":
        a = cur.execute("SELECT password FROM seller WHERE sellID=?", (userid,))
    real_psswd = list(a)[0][0]
    conn.close()
    return psswd==real_psswd

def set_psswd(psswd, userid, type):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    if type=="Customer":
        a = cur.execute("UPDATE customer SET password=? WHERE custID=?", (psswd, userid))
    elif type=="Seller":
        a = cur.execute("UPDATE seller SET password=? WHERE sellID=?", (psswd, userid))
    conn.commit()
    conn.close()

def add_prod(sellID, data):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    prodID = gen_prodID()
    tup = (prodID,
           data["name"],
           data["qty"],
           data["category"],
           data["price"],
           data["price"],
           data["desp"],
           sellID)
    cur.execute("INSERT INTO product VALUES (?,?,?,?,?,(SELECT profit_rate from metadata)*?,?,?)", tup)
    conn.commit()
    conn.close()

def get_categories(sellID):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    a = cur.execute("SELECT DISTINCT(category) from product where sellID=?", (sellID,))
    categories = [i[0] for i in a]
    conn.close()
    return categories

def search_myproduct(sellID, srchBy, category, keyword):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    keyword = ['%'+i+'%' for i in keyword.split()]
    if len(keyword)==0: keyword.append('%%')
    if srchBy=="by category":
        a = cur.execute("""SELECT prodID, name, quantity, category, cost_price
                        FROM product WHERE category=? AND sellID=? """,(category, sellID))
        res = [i for i in a]
    elif srchBy=="by keyword":
        res = []
        for word in keyword:
            a = cur.execute("""SELECT prodID, name, quantity, category, cost_price
                            FROM product
                            WHERE (name LIKE ? OR description LIKE ? OR category LIKE ?) AND sellID=? """,
                            (word, word, word, sellID))
            res += list(a)
        res = list(set(res))
    elif srchBy=="both":
        res = []
        for word in keyword:
            a = cur.execute("""SELECT prodID, name, quantity, category, cost_price
                            FROM product
                            WHERE (name LIKE ? OR description LIKE ?) AND sellID=? AND category=? """,
                            (word, word, sellID, category))
            res += list(a)
        res = list(set(res))
    conn.close()
    return res

def get_product_info(id):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute("""SELECT p.name, p.quantity, p.category, p.cost_price, p.sell_price,
                    p.sellID, p.description, s.name FROM product p JOIN seller s
                    WHERE p.sellID=s.sellID AND p.prodID=? """, (id,))
    res = [i for i in a]
    conn.close()
    if len(res)==0:
        return False, res
    return True, res[0]

def update_product(data, id):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    cur.execute("""UPDATE product
    SET name=?, quantity=?, category=?, cost_price=?,
    sell_price=(SELECT profit_rate from metadata)*?, description=?
    where prodID=?""",( data['name'],
                        data['qty'],
                        data['category'],
                        data['price'],
                        data['price'],
                        data['desp'],
                        id))
    conn.commit()
    conn.close()

def search_products(srchBy, category, keyword):
    conn = sqlite3.connect("OnlineShop/onlineshop.db")
    cur = conn.cursor()
    keyword = ['%'+i+'%' for i in keyword.split()]
    if len(keyword)==0: keyword.append('%%')
    if srchBy=="by category":
        a = cur.execute("""SELECT prodID, name, category, sell_price
                        FROM product WHERE category=? AND quantity!=0 """,(category,))
        res = [i for i in a]
    elif srchBy=="by keyword":
        res = []
        for word in keyword:
            a = cur.execute("""SELECT prodID, name, category, sell_price
                            FROM product
                            WHERE (name LIKE ? OR description LIKE ? OR category LIKE ?) AND quantity!=0 """,
                            (word, word, word))
            res += list(a)
        res = list(set(res))
    elif srchBy=="both":
        res = []
        for word in keyword:
            a = cur.execute("""SELECT prodID, name, category, sell_price
                            FROM product
                            WHERE (name LIKE ? OR description LIKE ?) AND quantity!=0 AND category=? """,
                            (word, word, category))
            res += list(a)
        res = list(set(res))
    conn.close()
    return res

def get_seller_products(sellID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute("SELECT prodID, name, category, sell_price FROM product WHERE sellID=? AND quantity!=0", (sellID,))
    res = [i for i in a]
    conn.close()
    return res

def place_order(prodID, custID, qty):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    orderID = gen_orderID()
    cur.execute("""INSERT INTO orders
                    SELECT ?,?,?,?,datetime('now'), cost_price*?, sell_price*?, 'PLACED'
                    FROM product WHERE prodID=? """, (orderID, custID, prodID, qty, qty, qty, prodID))
    conn.commit()
    conn.close()

def cust_orders(custID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute("""SELECT o.orderID, o.prodID, p.name, o.quantity, o.sell_price, o.date, o.status
                       FROM orders o JOIN product p
                       WHERE o.prodID=p.prodID AND o.custID=? AND o.status!='RECIEVED'
                       ORDER BY o.date DESC """, (custID,))
    res = [i for i in a]
    conn.close()
    return res

def sell_orders(sellID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute(""" SELECT o.orderID, o.prodID, p.name, o.quantity, p.quantity, o.cost_price, o.date, o.status
                        FROM orders o JOIN product p
                        WHERE o.prodID=p.prodID AND p.sellID=? AND o.status!='RECIEVED'
                        ORDER BY o.date DESC """, (sellID,))
    res = [i for i in a]
    conn.close()
    return res

def get_order_details(orderID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute(""" SELECT o.custID, p.sellID, o.status FROM orders o JOIN product p
                        WHERE o.orderID=? AND o.prodID=p.prodID """, (orderID,))
    res = [i for i in a]
    conn.close()
    return res

def change_order_status(orderID, new_status):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE orderID=? ", (new_status, orderID))
    if new_status=='DISPACHED':
        cur.execute("""UPDATE product SET
                     quantity=quantity-(SELECT quantity FROM orders WHERE orderID=? )
                     WHERE prodID=(SELECT prodID FROM orders WHERE orderID=? )""", (orderID, orderID))
    conn.commit()
    conn.close()

def cust_purchases(custID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute("""SELECT o.prodID, p.name, o.quantity, o.sell_price, o.date
                       FROM orders o JOIN product p
                       WHERE o.prodID=p.prodID AND o.custID=? AND o.status='RECIEVED'
                       ORDER BY o.date DESC """, (custID,))
    res = [i for i in a]
    conn.close()
    return res

def sell_sales(sellID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute("""SELECT o.prodID, p.name, o.quantity, o.sell_price, o.date, o.custID, c.name
                       FROM orders o JOIN product p JOIN customer c
                       WHERE o.prodID=p.prodID AND o.custID=c.custID AND p.sellID=? AND o.status='RECIEVED'
                       ORDER BY o.date DESC """, (sellID,))
    res = [i for i in a]
    conn.close()
    return res

def add_product_to_cart(prodID, custID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    cur.execute("""INSERT INTO cart VALUES (?,?,1) """, (custID, prodID))
    conn.commit()
    conn.close()

def get_cart(custID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    a = cur.execute("""SELECT p.prodID, p.name, p.sell_price, c.sum_qty, p.quantity
                       FROM (SELECT custID, prodID, SUM(quantity) AS sum_qty FROM cart
                       GROUP BY custID, prodID) c JOIN product p
                       WHERE p.prodID=c.prodID AND c.custID=?""", (custID,))
    res = [i for i in a]
    conn.close()
    return res

def update_cart(custID, qty):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    for prodID in qty:
        cur.execute("DELETE FROM cart WHERE prodID=? AND custID=?", (prodID, custID))
        cur.execute("INSERT INTO cart VALUES (?,?,?)", (custID, prodID, qty[prodID]))
    conn.commit()
    conn.close()

def cart_purchase(custID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    cart = get_cart(custID)
    for item in cart:
        orderID = gen_orderID()
        prodID = item[0]
        qty = item[3]
        cur.execute("""INSERT INTO orders
                        SELECT ?,?,?,?,datetime('now'), cost_price*?, sell_price*?, 'PLACED'
                        FROM product WHERE prodID=? """, (orderID, custID, prodID, qty, qty, qty, prodID))
        cur.execute("DELETE FROM cart WHERE custID=? AND prodID=?", (custID, prodID))
        conn.commit()
    conn.close()

def empty_cart(custID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE custID=?", (custID,))
    conn.commit()

def remove_from_cart(custID, prodID):
    conn = sqlite3.connect('OnlineShop/onlineshop.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE custID=? AND prodID=?", (custID, prodID))
    conn.commit()
    
