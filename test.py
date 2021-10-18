import csv

link = '123'

field_names = ['name', 'address', 'inn']

with open('CSV_/' + link + '.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names, quotechar = ';')
    writer.writeheader()
    writer.writerow({'name': 'B', 'address': 'Jane', 'inn': 'Oscar'})
    writer.writerow({'name': 'B', 'address': 'Jane', 'inn': 'Loive'})
 
print("Writing complete")