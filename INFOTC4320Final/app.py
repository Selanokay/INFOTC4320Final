from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

reservations = []

admin_credentials = {}


def update_reservations_file():
    with open('reservations.txt', 'w') as file:
        for line in reservations:
            first_name = line['first_name']
            row = line['row']
            column = line['column']
            tickcode = "INFOTC4320"
            e_ticket = ""
            i = 0
            while (i < len(first_name)) or (i < len(tickcode)):
                if(i < len(first_name)):
                    e_ticket += first_name[i]
                if(i < len(tickcode)):
                    e_ticket += tickcode[i]
                i= i+1
            file.write(f"{first_name}, {row}, {column}, {e_ticket}\n")


@app.route('/save_reservation', methods=['POST'])
def save_reservation():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    row = data.get('row')
    column = data.get('column')

    reservations.append({
        'first_name': first_name,
        'last_name': last_name,
        'row': int(row),
        'column': int(column)
    })

    update_reservations_file()

    return jsonify({'message': 'Reservation saved successfully'})


def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    total_cost = 0
    for line in reservations:
        cost_pos_one = line['row']
        cost_pos_two = line['column']
        cost_for_reservation = cost_matrix[cost_pos_one][cost_pos_two]
        total_cost += cost_for_reservation
        line['cost'] = cost_for_reservation  
    return cost_matrix


def get_seating_matrix():
    seating_matrix = [["O", "O", "O", "O"] for row in range(12)]
    for line in reservations:
        pos_one = line['row']
        pos_two = line['column']
        rep_val = "X"
        seating_matrix[pos_one][pos_two] = rep_val
    print(seating_matrix)
    return seating_matrix

def update_restxt(first_name, row, column):
    with open('reservations.txt', 'a+') as file:
        tickcode = "INFOTC4320"
        e_ticket = ""
        i = 0
        while (i < len(first_name)) or (i < len(tickcode)):
            if(i < len(first_name)):
                e_ticket += first_name[i]
            if(i < len(tickcode)):
                e_ticket += tickcode[i]
            i= i+1
        file.write(f"{first_name}, {row-1}, {column-1}, {e_ticket}\n")
        file.close

def load_admin_credentials():
    with open('passcodes.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(', ')
            admin_credentials[username] = password

def load_initial_reservations():
    with open('reservations.txt', 'r') as file:
        for line in file:
            first_name, row, column, e_ticket = line.strip().split(', ')
            reservations.append({
                'first_name': first_name,
                'row': int(row),
                'column': int(column),
                'e_ticket': e_ticket
            })

#@app.route('/')
#def main_menu():
  #  return render_template('Main.html')

@app.route('/admin_info')
def admin_info():
    cost_matrix = get_cost_matrix()
    seating_matrix = get_seating_matrix()
    total_sales = sum(line['cost'] for line in reservations)
    return render_template("AdminInfo.html", cost_matrix=cost_matrix, seating_matrix=seating_matrix, total_sales=total_sales)

@app.route('/Admin', methods=('GET', 'POST'))
def check_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Username is required!', 'error')
        elif not password:
            flash('Password is required', 'error')
        else:
            if username in admin_credentials and admin_credentials[username] == password:
                flash("Successful Login", 'success')
                return redirect(url_for('admin_info'))
            else:
                flash("Invalid Username or Password.", 'error')
                return render_template("Admin.html")

    return render_template("Admin.html")

load_admin_credentials()
load_initial_reservations()
#update_restxt("test", 1, 1)
#get_seating_matrix()
#get_cost_matrix()

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/Reservation')
def contact():
    cost_matrix = get_cost_matrix()
    seating_matrix = get_seating_matrix()
    return render_template('Reservation.html', cost_matrix=cost_matrix, seating_matrix=seating_matrix)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
