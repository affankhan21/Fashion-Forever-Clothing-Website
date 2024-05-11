from main import app
import category as cat
import product as pt
import adminLogin as ad
import user as us

# Urls for Category
app.add_url_rule("/addCategory",view_func=cat.addCategory,methods=["GET","POST"])
app.add_url_rule("/showAllCategories",view_func=cat.showAllCategories)
app.add_url_rule("/deleteCategory/<id>",view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule("/editCategory/<id>",view_func=cat.editCategory,methods=["GET","POST"])



#-------------urls for Product----------------------------
app.add_url_rule("/addProduct",view_func=pt.addProduct,methods=["GET","POST"])
app.add_url_rule("/showAllProduct",view_func=pt.showAllProduct)
app.add_url_rule("/deleteProduct/<id>",view_func=pt.deleteProduct,methods=["GET","POST"])
app.add_url_rule("/editProduct/<id>",view_func=pt.editProduct,methods=["GET","POST"])
#----------------urls for Admin---------------
app.add_url_rule("/adminLogin",view_func=ad.login,methods=["GET","POST"])
app.add_url_rule("/adminHome",view_func=ad.adminHome)
#--------------urls for user-----------------#
app.add_url_rule("/",view_func=us.homepage)
app.add_url_rule("/showPt/<cid>",view_func=us.showPt)
app.add_url_rule("/Login",view_func=us.Login,methods=["GET","POST"])
app.add_url_rule("/Logout",view_func=us.Logout)
app.add_url_rule("/Register",view_func=us.Register,methods=["GET","POST"])
app.add_url_rule("/ViewDetails/<product_id>",view_func=us.ViewDetails,methods=["GET","POST"])
app.add_url_rule("/Cart",view_func=us.ShowCartItems,methods=["GET","POST"])
app.add_url_rule("/MakePayment",view_func=us.MakePayment,methods=["GET","POST"])
app.add_url_rule("/Contact",view_func=us.Contact)
app.add_url_rule("/wishlist/<product_id>",view_func=us.addToWishlist)
app.add_url_rule("/viewwishlist",view_func=us.viewWishlist)
app.add_url_rule("/Aboutus",view_func=us.Aboutus)
app.add_url_rule("/message",view_func=us.message,methods=["GET","POST"])
app.add_url_rule("/showAllMessages",view_func=us.showAllMessages,methods=["GET","POST"])