# Importing required packages
from math import pi
import pandas as pd
import database,send_email,datetime,get_dates

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

from flask import Flask,render_template,request,redirect, session, url_for,flash

register_email = send_email.Register()

db = database.Database()
date = get_dates.DateTime() 

app = Flask(__name__)
app.secret_key = "a very secret  key"

@app.route("/")
def index():
    return redirect(url_for('register'))

@app.route("/register",methods = ['GET',"POST"])
def register():
    
    if request.method == 'POST':

        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email_id']
        pwd = request.form['password']
        cpwd = request.form['confirm_pwd']

        if pwd != cpwd:    
            return render_template('register.html',usr_error = "Password does not match!")

        else:
            
            result = db.view(email)
            
            if result:
                return render_template('register.html',usr_error = "Email Id already Exists!")
            
            user_id = db.length_view() + 1
            db.insert(user_id,fname,lname,email,pwd)

            register_email.get_email(email)
            register_email.SendDynamic()

            flash(" Successfully Registerd, Please login")
            return redirect(url_for("login"))
    else:
        return render_template('register.html')

@app.route("/login",methods = ['GET',"POST"])
def login():
    if request.method == 'POST':

        email = request.form['email_id']
        pwd = request.form['password']
        result = db.lg_view(email)
        print(db.lg_view(email))
        if not result:
            return render_template('login.html',usr_error = "Email id does'nt exists!")
            
        if pwd != result[0]:
            return render_template('login.html',usr_error = "Password doesn't match")
        else:
            session['loggedin'] = True
            session['username'] = email
            return redirect(url_for("dashboard"))
    else:
        return render_template('login.html')

@app.route("/dashboard")

def dashboard():

    email = session['username']
    user_id = db.uid_view(email)

    x_axis = date.get_week()
    bar_chart = bar_graph(user_id,x_axis)
    pie_chart = pie_graph(user_id,x_axis)

    expense_table = db.expense_view(user_id)

    return render_template("dashboard.html",
        details = expense_table,
        js_resources=bar_chart[0],
        css_resources=bar_chart[1],
        plot_script=bar_chart[2],
        plot_div=bar_chart[3],
        pie_js_resources=pie_chart[0],
        pie_css_resources=pie_chart[1],
        pie_script=pie_chart[2],
        pie_div=pie_chart[3]
    )

def bar_graph(user_id,x_axis):
    y_axis = db.chart(x_axis,user_id) 

    fig =figure(
        x_range=x_axis,  
        title="Your Weekly Expenses",
        toolbar_location="right", 
        tools="save,hover",
        tooltips="@x: ₹@top",
        width = 700,
        x_axis_label = "Dates of your Past 7 days",
        y_axis_label = "Amount you have spent"
        )
    fig.toolbar.logo = None
    fig.vbar(x=x_axis, top=y_axis, width=0.9)

    fig.xgrid.grid_line_color = None
    fig.y_range.start = 0

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)   
    print(div)
    return [js_resources,css_resources,script,div]

def pie_graph(user_id,x_axis):
    values = db.pie_chart(user_id,x_axis)
    data = pd.Series(values).reset_index(name='Expense_amt').rename(columns={'index': 'Expense_Name'})
    
    data['angle'] = data['Expense_amt']/data['Expense_amt'].sum() * 2*pi
    data['color'] = Category20c[len(values)]

    p = figure(
            height=350, 
            title="Expense Category Pie Chart", 
            toolbar_location='right',
            tools="save,hover", 
            tooltips="@Expense_Name: ₹@Expense_amt", 
            x_range=(-0.5, 1.0)
        )
    p.toolbar.logo = None
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='Expense_Name', source=data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    return [js_resources,css_resources,script,div]

@app.route("/wallet",methods = ['GET',"POST"])
def wallet():
    try:
        email = session['username']
        if request.method == 'POST':
            
            user_id = db.uid_view(email)   
            expense_name = request.form['exp_name']
            amount = request.form['exp_amt']
            date = request.form['exp_date']

            db.wallet_insert(user_id,amount,expense_name,date)
            flash("Expense Added Successfully!!")
            return render_template('Wallet.html')
        else:
            return render_template('Wallet.html')
    except:
        flash('Login before you want to access wallet page')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash("Logged out Successfully,please login again")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

