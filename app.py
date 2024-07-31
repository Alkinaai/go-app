from flask import Flask, render_template, url_for,request
import sqlite3

app =  Flask(__name__)

@app.route("/")
@app.route("/start")
def start():
    return render_template('start.html')

@app.route("/Innenputz")
def Innenputz():
    return render_template('Innenputz.html')
@app.route("/aussenputz")
def aussenputz():
    return render_template('aussenputz.html')

@app.route("/Klinkerriemchen")
def Klinkerriemchen():
    return render_template("Klinkerriemchen.html")

@app.route("/Kontact")
def Kontact():
    return render_template('Kontact.html')


# Home Page route
@app.route("/home")
def home():
    return render_template("home.html")

# Route to form used to add a new student to the database
@app.route("/enternew")
def enternew():
    return render_template("Customers.html")

# Route to add a new record (INSERT) student data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            telefon = request.form['telefon']
            note = request.form['note']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Customers (name, email, telefon, note) VALUES (?,?,?,?)",(name, email, telefon, note))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route to SELECT all data from the database and display in a table      
@app.route('/list')
def list():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the Customers table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM Customers")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("list.html",rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM Customers WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            name = request.form['name']
            email = request.form['email']
            telefon = request.form['telefon']
            note = request.form['note']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE Customers SET name='"+name+"', email='"+email+"', telefon='"+telefon+"', note='"+note+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE Customers SET name="+name+", email="+email+", telefon="+telefon+", note="+note+" WHERE rowid="+rowid

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM Customers WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)


if __name__ == "__main__":
    app.run(debug=True)