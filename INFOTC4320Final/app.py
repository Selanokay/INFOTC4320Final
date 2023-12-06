from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/Admin')
def admin():
    return render_template('Admin.html')

@app.route('/Admin', methods=('GET', 'POST'))
def check_admin():
        username = request.form['userUsername']
        password = request.form['userPassword']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required')
        else:
            if (username in admin_credentials and admin_credentials[username] == password):
                return redirect(url_for('admin_info'))
            else:
                flash("Invalid Username or Password.")
        return render_template("Admin.html")


@app.route('/Reservation')
def reservation():
    return render_template('Reservation.html')


if __name__ == '__main__':
    app.run(debug=True)

