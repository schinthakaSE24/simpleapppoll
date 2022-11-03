from flask import Flask, render_template, request, jsonify, flash, redirect
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
 
app = Flask(__name__)
         
app.secret_key = "caircocoders-ednalan"
         
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root'
app.config['MYSQL_DB'] = 'poolappdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) 
     
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM tblprogramming ORDER BY id ASC")
    webframework = cur.fetchall()  
    return render_template('index.html', webframework = webframework)
 
@app.route("/polldata",methods=["POST","GET"])
def polldata():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    query = "SELECT * from tbl_poll"
    cur.execute(query)
    total_poll_row = int(cur.rowcount) 
    cur.execute("SELECT * FROM tblprogramming ORDER BY id ASC")
    framework = cur.fetchall()  
    frameworkArray = []
    for row in framework:
        get_title = row['title']
        cur.execute("SELECT * FROM tbl_poll WHERE web_framework = %s", [get_title])
        row_poll = cur.fetchone()  
        total_row = cur.rowcount
        #print(total_row)
        percentage_vote = round((total_row/total_poll_row)*100)
        print(percentage_vote)
        if percentage_vote >= 40:
            progress_bar_class = 'progress-bar-success'
        elif percentage_vote >= 25 and percentage_vote < 40:   
            progress_bar_class = 'progress-bar-info'  
        elif percentage_vote >= 10 and percentage_vote < 25:
            progress_bar_class = 'progress-bar-warning'
        else:
            progress_bar_class = 'progress-bar-danger'
  
        frameworkObj = {
                'id': row['id'],
                'name': row['title'],
                'percentage_vote': percentage_vote,
                'progress_bar_class': progress_bar_class}
        frameworkArray.append(frameworkObj)
    return jsonify({'htmlresponse': render_template('response.html', frameworklist=frameworkArray)})
 
@app.route("/insert",methods=["POST","GET"])
def insert():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        poll_option = request.form['poll_option']
        print(poll_option)      
        cur.execute("INSERT INTO tbl_poll (web_framework) VALUES (%s)",[poll_option])
        mysql.connection.commit()       
        cur.close()
        msg = 'success' 
    return jsonify(msg)
 
if __name__ == "__main__":
    app.run(debug=True)
