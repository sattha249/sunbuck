from flask import Flask ,request
from flask_restful import Api
import sqlite3
from datetime import datetime


app = Flask(__name__)
api = Api(app)

@app.route('/',methods=['GET','POST','PUT','DELETE'])
def index():
    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    data = request.get_json()
    if request.method == 'GET':    
        rows = []
        for row in c.execute('SELECT * FROM coffees'):
            rows.append({"ice":row[3],"hot":row[2],"name":row[1]})
        print (rows)
        return {"coffee":rows}
    if request.method == 'POST':
        c.execute('INSERT INTO coffees (name,hot,ice) VALUES (?,?,?)',(data['name'],data['hot'],data['ice']))
        conn.commit()
        return {"added":data}
    if request.method == 'PUT':
        c.execute('UPDATE coffees SET hot = ?, ice = ? WHERE name = ?',(data['hot'],data['ice'],data['name']))
        conn.commit()
        return {"updated":data}
    if request.method == 'DELETE':
        c.execute('DELETE FROM coffees WHERE name = ?',(data['name'],))
        conn.commit()
        return {"deleted":data['name']}
        

@app.route('/buy',methods =['GET','POST'])
def buy():
    total = 0
    menu = []
    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    data = request.get_json()
    if request.method == 'GET':
        rows = []
        for row in c.execute('SELECT * FROM orders'):
            drink_type = 'hot' if row[2] == 0 else "ice"
            rows.append({"drink_id":row[1],"drink_type":drink_type,"price":row[3],"order date = ":row[4]})
        print (rows)
        return {"orders":rows}
    if request.method == 'POST':
        if ',' in data['name']:
            data['name'] = data['name'].split(',')
            menu = data['name']
            print(menu)        
        for bev in menu:
            quantity = 1   
            if '*' in bev:
                quantity = bev.split('*')
                bev = quantity[0]
                print(quantity[1])
                if quantity[1] == '':
                    return {'Message':"Please insert number after *"}
                quantity = int(quantity[1])
            c.execute("SELECT {},id FROM coffees WHERE name = '{}'".format(data['type'],bev))
            drink_type = False if data['type'] == 'hot' else True
            price = c.fetchone()
            print (price)
            if price is None:
                return {'Message':"Sorry We don't have this Menu"}
            for i in range(quantity):
                c.execute("INSERT INTO orders (drink_id,drink_type,price) VALUES ({},{},{} )".format(price[1],drink_type,price[0]))
                total += price[0]
        conn.commit()
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        return {"price":total,'time':now}

@app.route('/total',methods =['GET'])
def total():
    conn = sqlite3.connect('test.sqlite')
    c = conn.cursor()
    if request.method == 'GET':
        rows = []
        for row in c.execute("SELECT drink_id , SUM(price) from orders WHERE order_date = DATE('now') GROUP BY drink_id"):
            rows.append({"drink id":row[0],"total price":row[1]})
        print ()
        return {"total":rows}



if __name__ == "__main__":
    app.run(debug=True)