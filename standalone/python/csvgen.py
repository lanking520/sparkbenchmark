import csv

ROWS = 10000

with open('players.csv', 'w', newline='') as file:
    fieldnames = ['player_name', 'fide_rating']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for idx in range(ROWS - 1):
        writer.writerow({'player_name': 'Test' + str(idx), 'fide_rating': idx})
