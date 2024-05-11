import mysql.connector
from flask import render_template,request,redirect,url_for,session,make_response
from werkzeug.utils import secure_filename
from datetime import datetime


DBHOST = 'localhost'
#DBNAME = 'assignment'
DBUSER = 'root'
DBPASS = ''
DBDATABASE="onlineshop"

def homepage():
     con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
     cursor = con.cursor()
     sql = '''select product_id,product_name,price,size,description,image_url,cname 
            from product as p inner join category as cat  
            on p.cid = cat.cid;'''
  
     cursor.execute(sql)
     cakes = cursor.fetchall()
     sql1="select * from category"
     cursor.execute(sql1)
     cats=cursor.fetchall()
     return render_template("Homepage3.html",cakes=cakes,cats=cats)

def showPt(cid):
     con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
     cursor = con.cursor()
     sql = "select * from product_vw where cat_id=%s;"
     val=(cid,)
     cursor.execute(sql,val)
     cakes = cursor.fetchall()
     sql1="select * from category"
     cursor.execute(sql1)
     cats=cursor.fetchall()
     return render_template("Homepage3.html",cakes=cakes,cats=cats)
def Login():
     if request.method=="GET":
          if"message" in request.cookies:
               message=request.cookies.get("message")
          else:
               message=None    
          return render_template("Login.html",message=message)
     else:
          uname=request.form["uname"]
          pwd=request.form["pwd"]
          sql=''' select count(*) from userinfo where username=%s and password=%s and role=%s'''
          con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
          cursor=con.cursor()
          val=(uname,pwd,"user")
          cursor.execute(sql,val)
          count=cursor.fetchone()
          print(count)
          if(int(count[0]==1)):
               session["uname"]=uname
               return redirect("/")
          else:
               return redirect(url_for("Login"))     

def Register():
     if request.method=="GET":
          return render_template("Register.html")
     else:
          uname=request.form["uname"]
          pwd=request.form["pwd"] 
          email=request.form["email"]
          con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
          cursor=con.cursor()
          sql=''' insert into userinfo (username,password,email_id,role) values(%s,%s,%s,%s)'''
          val=(uname,pwd,email,"user")
          try:
               
               cursor.execute(sql,val)
          except:
               message="User Already Exsists"
               return render_template("Register.html",message=message)
          else:          
               con.commit()
          return redirect(url_for("Login"))  

def Logout():
    session.clear()
    return redirect("/")

def ViewDetails(product_id):
    if request.method == "GET":
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, database=DBDATABASE)
        cursor = con.cursor()
        sql = 'select * from product_vw where product_id=%s;'
        val = (product_id,)
        cursor.execute(sql, val)
        cake = cursor.fetchone()
        return render_template("ViewDetails.html", cake=cake)
    else:
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, database=DBDATABASE)
        cursor = con.cursor()
        uname = session["uname"]
        qty = request.form["qty"]
        if "uname" in session:
               sql = "select count(*) from MyCart where username=%s and product_id=%s;"
               val = (session["uname"], product_id)
               cursor.execute(sql, val)
               count = cursor.fetchone()
               if int(count[0]) == 1:
                    message = "Item Already in Cart"
               else:   
                    sql = "insert into MyCart (username,product_id,qty) values (%s,%s,%s)"
                    val = (uname,product_id,qty)
                    cursor.execute(sql,val)
                    con.commit()
                    message = "Item added to cart successfully"
               return redirect(url_for("ShowCartItems",message=message))
        else:
          #message = "You need to login to perform Add to cart"
          #resp = make_response(redirect("/Login"))
          #resp.set_cookie("message",message)
          #return resp
          return redirect("/Login")    

       


def ShowCartItems():
     if request.method=="GET":
          if "uname" in session: 
               if "message" in request.args:           
                    message = request.args["message"]
               else:
                    message=""
               uname=session["uname"]
               con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
               cursor = con.cursor()
               sql="select * from cart_vw where username=%s ;"
               val=(uname,)
               cursor.execute(sql,val)
               items=cursor.fetchall()
               sql = "select sum(subtotal) from cart_vw where username=%s"
               val = (session["uname"],)
               cursor.execute(sql,val)
               total = cursor.fetchone()[0]
               session["total"] = total
               return render_template("Cart.html",items=items,message=message)
          else:
             return redirect("/Login")
     else:
          action=request.form["action"]
          con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
          cursor = con.cursor()
          if action=="update":
               qty = request.form["qty"]
               sql = "update MyCart set qty = %s where username=%s and product_id=%s"
               val =  ( qty,session["uname"],request.form["product_id"])            
               cursor.execute(sql,val)
               con.commit() 
          else:
            sql = "delete from MyCart where username=%s and product_id=%s"
            val = ( session["uname"],request.form["product_id"])            
            cursor.execute(sql,val)
            con.commit()
          return redirect("/Cart")

def MakePayment():
     if request.method=="GET":
          return render_template("MakePayment.html")
     else:
          cardno = request.form["cardno"]
          cvv = request.form["cvv"]
          expiry = request.form["expiry"]   
          con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
          cursor = con.cursor()
          sql = "select count(*) from payment where cardno=%s and cvv=%s and expiry=%s"
          val=(cardno,cvv,expiry)
          cursor.execute(sql,val)
          count = int(cursor.fetchone()[0])
          if (count==1):
              total=session["total"]
              sql1="update payment set balance=balance-%s where cardno=%s and cvv=%s and expiry=%s;"
              val1=(total,cardno,cvv,expiry)
              sql2="update payment set balance=balance+%s where cardno=%s and cvv=%s and expiry=%s;"
              val2=(total,"22222","5678","06/2040")
              cursor.execute(sql1,val1)
              cursor.execute(sql2,val2)
              con.commit()
              dd = datetime.today().strftime('%Y-%m-%d')
              sql3="insert into order_master(username,date_of_order,amount)values(%s,%s,%s);"
              val3=(session["uname"],dd,total)
              cursor.execute(sql3,val3)
              con.commit()
              print("Done till ordermaster")
              dd = datetime.today().strftime('%Y-%m-%d')
              sql4="select id from order_master where username=%s and date_of_order=%s and amount=%s limit 1 ;"
              val4=(session["uname"],dd,total)
              print(val4)
              cursor.execute(sql4,val4)
              oid=int(cursor.fetchone()[0])
              sql5="update mycart set order_id=%s where username=%s and order_id is null;"
              val5=(oid,session["uname"])  
              cursor.execute(sql5,val5)
              con.commit()
              sql6="delete from mycart  where username=%s ;"
              val6=(session["uname"],)  
              cursor.execute(sql6,val6)
              con.commit()
              return redirect("/")    
          else:
                return redirect(url_for("MakePayment"))   


def Contact():
     return render_template("Contact.html")

def addToWishlist(product_id):
    if request.method == "GET":
        if "uname" in session:
            uname = session["uname"]
            con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
            cursor = con.cursor()
            sql = "INSERT INTO wishlist (username, product_id) VALUES (%s, %s)"
            val = (uname, product_id)
            cursor.execute(sql, val)
            con.commit()
            return "Item added to wishlist"
        else:
            return redirect("/Login")

def viewWishlist():
    if request.method == "GET":
        if "uname" in session:
            uname = session["uname"]
            con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
            cursor = con.cursor()
            sql = "SELECT p.product_id, p.product_name, p.price, p.description, p.image_url, c.cname FROM product p INNER JOIN category c ON p.cid = c.cid WHERE p.product_id IN (SELECT product_id FROM wishlist WHERE username = %s)"
            val = (uname,)
            cursor.execute(sql, val)
            wishlist_items = cursor.fetchall()
            print("Wishlist Items:", wishlist_items)  # Debugging statement
            return render_template("wishlist.html", wishlist=wishlist_items)
        else:
            return redirect("/Login")

def Aboutus():
     return render_template("aboutus.html")
def message():
     if request.method == "GET":
               return render_template("message.html")
     else:
               uname = session["uname"]
               message = request.form["message"]
               category = request.form["category"]
               con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS,database=DBDATABASE)
               cursor = con.cursor()
               sql = "INSERT INTO message (category,messages,username) VALUES (%s, %s,%s)"
               val = (category,message ,uname)
               cursor.execute(sql, val)
               con.commit()
               
     return redirect("/") 
   
    
def showAllMessages():
    if 'uname' not in session:
        return redirect('/adminLogin')

    if request.method == "GET":
        uname = session["uname"]
        con = mysql.connector.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, database=DBDATABASE)
        cursor = con.cursor()
        sql = "SELECT * FROM message;"
        cursor.execute(sql)
        showm = cursor.fetchall()
        print(showm)
        con.close()  # Close the connection
        return render_template("showmessages.html", showm=showm)
    else:
        return redirect("/adminLogin")
