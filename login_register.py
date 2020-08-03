from flask import Flask,render_template
from flask import request,redirect,url_for, make_response
import pymysql
import traceback
#import mysql.connector

app = Flask(__name__)

class Database:
    def __init__(self):
        host='localhost'
        user='root'
        password='jayden'
        db='register'

        self.con = pymysql.connect(host=host,user=user,
                                   password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur =self.con.cursor()

    def insert_data(self,username,password):
        self.cur.execute("INSERT into user(username,password) VALUES (%s,%s)",(username,password))
        self.con.commit()
        return "Successful"

    def get_data(self,username,password):
        self.cur.execute("SELECT * from user WHERE username= %s and password= %s",(username,password))
        result = self.cur.fetchall()
        return result


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    db = Database()
    msg =""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            result= db.get_data(username,password)
            print(result)

            if len(result)== 1 :
                response = redirect(url_for('transfer'))
                response.set_cookie('username',username)
                return response
                #return render_template('transfer.html')
            else:
                msg = 'username/password is incorrect'

        except:
            traceback.print_exc()

    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    db = Database()
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        confirmed_password = data['confirmed_password']

        if password == confirmed_password:
            try:
                msg = db.insert_data(username,password)
                return redirect(url_for('login'))

            except:
                msg = "exist same username"
        else:
            msg = "two password are not same"

    return render_template('register.html',msg=msg)


@app.route('/transfer',methods=['GET','POST'])
def transfer():
    username = request.cookies.get('username',None)

    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        to_account = request.form.get('to_account')
        money = request.form.get('money')
        return 'transfer {} dollars to {} successfully'.format(money,to_account)

    response = make_response(render_template('transfer.html'))
    return response

if __name__ == '__main__':
    app.run(debug=True, port=2020)