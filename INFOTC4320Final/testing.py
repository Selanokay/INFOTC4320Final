reservations = []

admin_credentials = {}

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    total_cost = 0
    for line in reservations:
        cost_pos_one = line['row']
        cost_pos_two = line['column']
        total_cost += cost_matrix[cost_pos_one][cost_pos_two]

    print(cost_matrix)
    print(total_cost)
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


load_admin_credentials()
load_initial_reservations()
update_restxt("test", 1, 1)
get_seating_matrix()
get_cost_matrix()
