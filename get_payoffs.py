import csv


def get_payoff(user,context):
    with open('user_context.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        user_payoffs =[]
        for row in csv_reader:
            if row[0] == user:
                user_payoffs.append(row)
