from flask import Flask, render_template, redirect,request, url_for, session
import requests
import ibm_db
import json
import os
import sendmail
app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yzh63070;PWD=VxRllTtylqJ3u6lp",'','')

@app.route('/registration')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    x = [x for x in request.form.values()]
    print(x)
    name=x[0]
    email=x[1]
    phone=x[2]
    city=x[3]
    infect=x[4]
    blood=x[5]
    password=x[6]
    sql = "SELECT * FROM user WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('register.html', pred="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO  user VALUES (?, ?, ?, ?, ?, ?, ?)"
        # insert into user values('yuvan','yuvan@gmail.com','8072660060','chennai','infected','O Positive','yuvan')
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, phone)
        ibm_db.bind_param(prep_stmt, 4, city)
        ibm_db.bind_param(prep_stmt, 5, infect)
        ibm_db.bind_param(prep_stmt, 6, blood)
        ibm_db.bind_param(prep_stmt, 7, password)
        ibm_db.execute(prep_stmt)
        return render_template('register.html', pred="Registration Successful, please login using your details")
       
           
        
# @app.route('/login')
@app.route('/')    
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    sql = "SELECT * FROM user WHERE email=? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.bind_param(stmt,2,passw)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(user,passw)
    if account:
            return redirect(url_for('stats'))
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username / password !") 
      
        
@app.route('/stats')
def stats():
    sql = "select blood,COUNT(*) blood from user group by blood"
    stmt=ibm_db.exec_immediate(conn,sql)
    lst=[]
    donors={}
    while ibm_db.fetch_row(stmt) !=False:
        donors[ibm_db.result(stmt,0)]=ibm_db.result(stmt,1)

    return render_template('stats.html',b=sum(donors.values()),b1=donors.get('A Negative'),b2=donors.get('A Positive'),b3=donors.get('AB Negative'),b4=donors.get('AB Positive'),b5=donors.get('B Negative'),b6=donors.get('B Positive'),b7=donors.get('O Negative'),b8=donors.get('O Positive'))

@app.route('/requester')
def requester():
    return render_template('request.html')


@app.route('/requested',methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    address = request.form['address']
    print(address)
    sql = "SELECT email FROM user WHERE blood=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,bloodgrp)
    ibm_db.execute(stmt)
    lst1=[]

    # sending Email through SendGrid

    msg = "Need Plasma of your blood group for the address:  "+address

    while ibm_db.fetch_row(stmt) !=False:
        lst1.append(ibm_db.result(stmt,0))
    
    if len(lst1)==0:
        return render_template('request.html', pred="No donors for the requested plasma Type.")
    
    else:
        for i in lst1:
            try:
                sendmail.sendMailUsingSendGrid(sendmail.API,sendmail.from_email,i,sendmail.subject,msg)
                return render_template('request.html', pred="Your request is sent to the concerned people.")
            except:
                print("Problem in sending Email")
            
    

if __name__=="__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(port=port,host='0.0.0.0')