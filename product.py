import mysql.connector
from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename


DBHOST = 'localhost'
#DBNAME = 'assignment'
DBUSER = 'root'
DBPASS = ''
DBDATABASE="onlineshop"


def addProduct():
    if request.method == "GET":
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
        cursor = con.cursor()
        sql = "select * from category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("addProduct.html",cats=cats)
    else:
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
        pname = request.form["pname"]
        price = request.form["price"]
        size=request.form["size"]
        description = request.form["description"]
        f = request.files['image_url'] 
        filename = secure_filename(f.filename)
        filename = "static/Images/"+f.filename
        #This will save the file to the specified location
        f.save(filename)   
        filename = "Images/"+f.filename
        cat_id = request.form["cat"]
        cursor = con.cursor()
        sql = "insert into product (product_name,price,size,description,image_url,cid) values (%s,%s,%s,%s,%s,%s)"
        val = (pname,price,size,description,filename,cat_id)
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllProduct"))


def showAllProduct():
    con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
    cursor = con.cursor()
    sql = '''select product_id,product_name,price,size,description,image_url,cname 
            from product as p inner join category as cat  
            on p.cid = cat.cid;'''
  
    cursor.execute(sql)
    cakes = cursor.fetchall()
    return render_template("showAllProduct.html",cakes=cakes)  
def deleteProduct(id):
    if request.method == "GET":
        return render_template("delete.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
            cursor = con.cursor()
            sql = "delete from product where product_id = %s"
            val = (id,)
            cursor.execute(sql,val)
            con.commit()
        return redirect(url_for("showAllProduct")) 

def editProduct(id):
    if request.method == "GET":
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
        cursor = con.cursor()
        sql = "select * from product where product_id=%s"
        val = (id,)
        cursor.execute(sql,val)
        cat = cursor.fetchone()
        return render_template("editProduct.html",cat=cat)   
    else:
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
        pname = request.form["pname"]
        price = request.form["price"]
        size=request.form["size"]
        description = request.form["description"]
        #f = request.files['image_url'] 
        #filename = secure_filename(f.filename)
        #filename = "static/Images/"+f.filename
        #This will save the file to the specified location
        #f.save(filename)   
        #filename = "Images/"+f.filename
        #cat_id = request.form["cat"]
        #image_url=request.form["image_url"]
        cursor = con.cursor()
        sql = " update product set product_name=%s ,price=%s,size=%s ,description=%s  where product_id=%s"
        val = (pname,price,size,description,id)
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllProduct")) 
               

