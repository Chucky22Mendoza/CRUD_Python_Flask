from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'

mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts(fullname, phone, email) VALUES(%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact added successfully')
        return redirect(url_for('home'))

@app.route('/edit/<string:id>')
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<string:id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
    """, (fullname, email, phone, id))
    mysql.connection.commit()
    flash('Contact updated successfully')
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed successfully')
    return redirect(url_for('home'))

@app.route('/cancel_message')
def cancel_message():
    flash('Operation canceled')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)