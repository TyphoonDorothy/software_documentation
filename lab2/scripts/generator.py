import uuid
import random
import csv

def generate_bulk_csv(filename="./data/data_source.csv", rows=1000):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'id', 'title', 'pricePerNight', 'ownerId', 'name', 'email'])

        for i in range(0, rows, 2):
            writer.writerow(['user', str(i), '', '', '', f'User_{i}', f'test{i}@mail.com'])

        for i in range(1, rows, 2):
            writer.writerow(['listing', str(i), f'Apartment {i}', 
                             round(random.uniform(50, 500), 2), 
                             str(i - 1), '', ''])
if __name__ == "__main__":
    generate_bulk_csv()
    print("CSV file generated successfully with sample data.")