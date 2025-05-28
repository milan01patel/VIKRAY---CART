from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.conf import settings
import os


# Create your views here.
# ***************************************************************************************************user side
def simpleheader(request):
    return render(request, "user/simpleheader.html")


# ********************* index.html
def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("em")
        mobile = request.POST.get("mob")
        password = request.POST.get("pass")
        confirm_password = request.POST.get("cpass")
        housenumber = request.POST.get("hn")
        street = request.POST.get("str")
        city = request.POST.get("ct")
        state = request.POST.get("stt")

        if password != confirm_password:
            messages.error(request, "Password and Confirm Password do not match.")
            return redirect("register")

        with connection.cursor() as cursor:
            query = "INSERT INTO users (firstname, lastname, email, mobile, password, housenumber, street, city, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(
                query,
                [
                    fname,
                    lname,
                    email,
                    mobile,
                    password,
                    housenumber,
                    street,
                    city,
                    state,
                ],
            )
            messages.success(request, "Registration successful. You can now login.")
            return redirect("login")

    return render(request, "user/register.html")


def login(request):
    if "useremail" in request.session:
        messages.success(request, "YOU ARE ALREADY LOGIN")
        return redirect("home")
    if request.method == "POST":
        emailormobile = request.POST.get("eormo")
        password = request.POST.get("password")
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE (email = %s OR mobile = %s)"
            cursor.execute(query, [emailormobile, emailormobile])
            user = cursor.fetchone()
            if user:
                right_password = user[5]
                if right_password == password:
                    request.session["useremail"] = user[3] 
                    messages.success(request, "Login successful! Welcome 😊")
                    return redirect("home")
                else:
                    messages.error(request, "Wrong password. Please try again.")
                    return redirect('login')
            else:
                messages.error(request, "EMAIL OR MOBILE And Password are incorrect.")
                return redirect('login')
    return render(request, "user/login.html")


def logout(request):
    if "useremail" in request.session:
        request.session.flush()
        messages.success(request, "Thank You! Visit Again and Stay Connected 😊")
        return redirect("home")
    else:
        messages.info(request, "You are already logged out.")


def index(request):
    with connection.cursor() as cursor:
        query = "select * from products"
        cursor.execute(query)
        data = cursor.fetchall()
        productlist = [
            {
                "id": row[0],
                "product_type": row[1],
                "product_company": row[2],
                "product_name": row[3],
                "product_description": row[4],
                "product_price": row[5],
                "product_image": row[6],
            }
            for row in data
        ]
        return render(request, "user/index.html", {"products": productlist})


def header(request):
    return render(request, "user/header.html")


def about(request):
    return render(request, "user/about.html")


def products(request):
    with connection.cursor() as cursor:
        query = "select * from products"
        cursor.execute(query)
        data = cursor.fetchall()
        productlist = [
            {
                "id": row[0],
                "product_type": row[1],
                "product_company": row[2],
                "product_name": row[3],
                "product_description": row[4],
                "product_price": row[5],
                "product_image": row[6],
            }
            for row in data
        ]
    return render(request, "user/products.html", {"products": productlist})


def viewproduct(request, id):
    with connection.cursor() as cursor:
        query = "SELECT * FROM products WHERE id=%s"
        cursor.execute(query, [id])
        product = cursor.fetchone()

        productlist = {
            "id": product[0],
            "product_type": product[1],
            "product_company": product[2],
            "product_name": product[3],
            "product_description": product[4],
            "product_price": product[5],
            "product_image": product[6],
        }
    return render(request, "user/viewproduct.html", {"product": productlist})


def addtocart(request, id):
    if "useremail" not in request.session:
        messages.success(request, "Access Starts with a Login.!😊")
        return redirect("login")

    with connection.cursor() as cursor:
        query = "select * from products where id=%s"
        cursor.execute(query, [id])
        productdata = cursor.fetchone()
        if productdata is None:
            return redirect("home")

        useremail = request.session.get("useremail")
        prdid = productdata[0]
        prdname = productdata[3]
        prdprice = productdata[5]
        prdimage = productdata[6]

        insert_query = "insert into cart (product_id,product_name,product_price,product_image,user_email) values (%s,%s,%s,%s,%s)"
        cursor.execute(insert_query, [prdid, prdname, prdprice, prdimage, useremail])
        messages.success(request, "PRODUCT ADDED! IN YOUR CART")
        return redirect("products")
    return render(request, "user/products.html")


def mycart(request):
    if "useremail" not in request.session:
        messages.success(request, "Access Starts with a Login.!😊")
        return redirect("login")
    useremail = request.session.get("useremail")

    with connection.cursor() as cursor:
        query = "select * from cart where user_email=%s"
        cursor.execute(query, [useremail])
        data = cursor.fetchall()
        productlist = [
            {
                "id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "product_price": row[3],
                "product_image": row[4],
            }
            for row in data
        ]
        total_price = 0
        for item in productlist:
            total_price = total_price + int(item["product_price"])
    return render(
        request,
        "user/mycart.html",
        {"cart_items": productlist, "total_price": total_price},
    )


def deletecart(request, id):
    with connection.cursor() as cr:
        query = "delete from cart where id=%s"
        cr.execute(query, [id])
        messages.success(request, "PRODUCT REMOVED ✔")
        return redirect("mycart")


def myorders(request):
    if "useremail" not in request.session:
        messages.success(request, "Access Starts with a Login.!😊")
        return redirect("login")

    useremail = request.session.get("useremail")
    with connection.cursor() as cursor:
        
        query = "select * from orders where user_email=%s"
        cursor.execute(query, [useremail])
        data = cursor.fetchall()
        orderlist = [
            {
                "id": row[0],
                "product_name": row[3],
                "product_price": row[4],
                "product_image" : row[9],
            }
            for row in data
        ]
    return render(request, "user/myorders.html", {"orders": orderlist})


def deletemyorder(request, id):
    with connection.cursor() as cr:
        query = "delete from orders where id=%s"
        cr.execute(query, [id])
        messages.success(request, "ORDER REMOVED ✔")
        return redirect("myorders")


def tocheckout(request):
    if "useremail" not in request.session:
        messages.success(request, "Access Starts with a Login.!😊")
        return redirect("login")

    useremail = request.session.get("useremail")
    with connection.cursor() as cursor:
        query = "select * from users where email=%s"
        cursor.execute(query, [useremail])
        d = cursor.fetchone()
        address = {
            "id": d[0],
            "firstname": d[1],
            "lastname": d[2],
            "email": d[3],
            "mobile": d[4],
            "password": d[5],
            "housenumber": d[6],
            "street": d[7],
            "city": d[8],
            "state": d[9],
        }
    return render(request, "user/tocheckout.html", {"address": address})


def makeorder(request):
    useremail = request.session.get("useremail")
    if request.method == "POST":
        houseno = request.POST.get("hn")
        street = request.POST.get("str")
        city = request.POST.get("ct")
        state = request.POST.get("sta")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cart WHERE user_email=%s", [useremail])
            cart_items = cursor.fetchall()

            for item in cart_items:
                prdid = item[1]
                prdname = item[2]
                prdprice = item[3]
                prdimage = item[4]


                query = """
                    INSERT INTO orders (user_email, product_id, product_name, product_price, housenumber, street, city, state, product_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
                """
                cursor.execute(
                    query,
                    [useremail, prdid, prdname, prdprice, houseno, street, city, state, prdimage],
                )

            cursor.execute("DELETE FROM cart WHERE user_email=%s", [useremail])

        messages.success(request, "Your order has been placed successfully! 🎉")
        return redirect("myorders")

    return render(request, "user/makeorder.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("nm")
        email = request.POST.get("em")
        subject = request.POST.get("sub")
        message = request.POST.get("msg")
        with connection.cursor() as cursor:
            query = "INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, [name, email, subject, message])
            messages.success(request, "Thank you for contacting us!🙏")
            return redirect("home")
    return render(request, "user/index.html")


def customersupport(request):
    return render(request, "user/customersupport.html")


def footer(request):
    return render(request, "user/footer.html")


# *************************************************************************************************** ADMIN SIDE
def admin(request):
    if "adminemail" in request.session:
        return redirect("admindashboard")
    if request.method == "POST":
        email = request.POST.get("em")
        password = request.POST.get("pas")
        with connection.cursor() as cursor:
            query = "SELECT * FROM admin WHERE email = %s AND password = %s"
            cursor.execute(query, [email, password])
            admin = cursor.fetchone()
            if admin:
                request.session["adminemail"] = admin[2]
                messages.success(request, "Login successful! Welcome 😊")
                return redirect("admindashboard")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect("admin")
    return render(request, "admin/admin.html")


def a_logout(request):
    if "adminemail" in request.session:
        request.session.flush()
        messages.success(request, "LOGOUT SUCCESSFULL")
        return redirect("admin")


def adminheader(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    return render(request, "admin/adminheader.html")


def dashboard(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    return render(request, "admin/dashboard.html")


def manageproduct(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    with connection.cursor() as cursor:
        query = "select * from products"
        cursor.execute(query)
        data = cursor.fetchall()
        productlist = [
            {
                "id": row[0],
                "product_type": row[1],
                "product_company": row[2],
                "product_name": row[3],
                "product_description": row[4],
                "product_price": row[5],
                "product_image": row[6],
            }
            for row in data
        ]
    return render(request, "admin/manageproduct.html", {"products": productlist})


def addproduct(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    if request.method == "POST":
        with connection.cursor() as cursor:
            prddtype = request.POST.get("prdtyp")
            prdcompany = request.POST.get("prdcomp")
            prdname = request.POST.get("mnm")
            prddescription = request.POST.get("des")
            prdprice = request.POST.get("p")
            prdimage = request.FILES.get("img")
            image_r_p = ""
            if prdimage:
                image_path = os.path.join(
                    settings.MEDIA_ROOT, "products", prdimage.name
                )
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, "wb") as f:
                    for chunk in prdimage.chunks():
                        f.write(chunk)
                image_r_p = "/vikrayapp/static/image/products/" + prdimage.name
                query = "insert into products (product_type,product_company,product_name,product_description,product_price,product_image) values (%s,%s,%s,%s,%s,%s)"
                cursor.execute(
                    query,
                    [
                        prddtype,
                        prdcompany,
                        prdname,
                        prddescription,
                        prdprice,
                        image_r_p,
                    ],
                )
                messages.success(request, "PRODUCT ADDED SUCCESSFULL ✔️")
                return redirect("manageproduct")
    return render(request, "admin/manageproduct.html")


def updateproduct(request, id):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")

    if request.method == "POST":
        prdname = request.POST.get("mnm")
        prddescription = request.POST.get("des")
        prdprice = request.POST.get("p")
        prdimage = request.FILES.get("img")
        image_r_p = ""
        if prdimage:
            image_path = os.path.join(settings.MEDIA_ROOT, "products", prdimage.name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, "wb") as f:
                for chunk in prdimage.chunks():
                    f.write(chunk)
            image_r_p = "/vikrayapp/static/image/products/" + prdimage.name
        with connection.cursor() as cursor:
            query = "update products set product_name=%s,product_description=%s,product_price=%s,product_image=%s where id=%s"
            cursor.execute(query, [prdname, prddescription, prdprice, image_r_p, id])
            messages.success(request, "PRODUCT UPDATED SUCCESS !")
            return redirect("manageproduct")

    with connection.cursor() as cursor:
        query = "SELECT * FROM products WHERE id=%s"
        cursor.execute(query, [id])
        product = cursor.fetchone()

        productlist = {
            "id": product[0],
            "product_type": product[1],
            "product_company": product[2],
            "product_name": product[3],
            "product_description": product[4],
            "product_price": product[5],
            "product_image": product[6],
        }
    return render(request, "admin/updateproduct.html", {"product": productlist})


def deleteproduct(request):
    with connection.cursor() as cr:
        query = "delete from products where id=%s"
        cr.execute(query, [id])
        messages.success(request, "PRODUCT DELETED ✔")
        return redirect("manageproduct")


def allcart(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    with connection.cursor() as cursor:
        query = "select * from cart"
        cursor.execute(query)
        data = cursor.fetchall()
        cartlist = [
            {
                "id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "product_price": row[3],
                "product_image": row[4],
                "user_email": row[5],
            }
            for row in data
        ]
        return render(request, "admin/allcart.html", {"carts": cartlist})


def daletefromallcart(request, id):
    with connection.cursor() as cr:
        query = "delete from cart where id=%s"
        cr.execute(query, [id])
        messages.success(request, "CART DELETED ✔")
        return redirect("allcart")


def manageusers(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    with connection.cursor() as cursor:
        query = "select * from users"
        cursor.execute(query)
        datas = cursor.fetchall()
        userslist = [
            {
                "id": d[0],
                "firstname": d[1],
                "lastname": d[2],
                "email": d[3],
                "mobile": d[4],
                "password": d[5],
                "housenumber": d[6],
                "street": d[7],
                "city": d[8],
                "state": d[9],
            }
            for d in datas
        ]
        return render(request, "admin/manageusers.html", {"users": userslist})


def deleteuser(request, id):
    with connection.cursor() as cr:
        query = "delete from users where id=%s"
        cr.execute(query, [id])
        messages.success(request, "USER DELETED ✔")
        return redirect("manageusers")


def manageaddress(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    with connection.cursor() as cursor:
        query = "select * from orders"
        cursor.execute(query)
        datas = cursor.fetchall()
        userslist = [
            {
                "user_email": d[1],
                "housenumber": d[5],
                "street": d[6],
                "city": d[7],
                "state": d[8],
            }
            for d in datas
        ]
    return render(request, "admin/manageaddress.html", {"addresses": userslist})


def manageorders(request):
    if "adminemail" not in request.session:
        messages.success(request, "Access Starts with a Login.!😊")
        return redirect("admin")

    with connection.cursor() as cursor:
        query = "select * from orders"
        cursor.execute(query)
        data = cursor.fetchall()
        orderlist = [
            {
                "id": row[0],
                "user_email": row[1],
                "product_id": row[2],
                "product_name": row[3],
                "product_price": row[4],
                "product_image" :row[9],
            }
            for row in data
        ]
    return render(request, "admin/manageorders.html", {"orders": orderlist})


def deleteorder(request, id):
    with connection.cursor() as cr:
        query = "delete from orders where id=%s"
        cr.execute(query, [id])
        messages.success(request, "ORDER REMOVED ✔")
        return redirect("manageorders")


def managecontacts(request):
    if "adminemail" not in request.session:
        messages.success(request, "Not Logged In? Access Starts with a Login.!!")
        return redirect("admin")
    with connection.cursor() as cursor:
        query = "select * from contacts"
        cursor.execute(query)
        datas = cursor.fetchall()
        contacts = [
            {
                "id": d[0],
                "name": d[1],
                "email": d[2],
                "subject": d[3],
                "message": d[4],
            }
            for d in datas
        ]
    return render(request, "admin/managecontacts.html", {"contacts": contacts})


def deletecontact(request, id):
    with connection.cursor() as cr:
        query = "delete from contacts where id=%s"
        cr.execute(query, [id])
        messages.success(request, "CONTACT DELETED ✔")
    return redirect("managecontacts")
