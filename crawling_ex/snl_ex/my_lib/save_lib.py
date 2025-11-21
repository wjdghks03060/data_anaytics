from datetime import datetime
import os
import csv

def save_datas(data_keyword, head, movie_list):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    folder = f"{data_keyword}_{timestamp}"
    filename = f"kobis_movie_{timestamp}.csv"
    filepath = os.path.join(folder, filename)
    
    os.makedirs(folder, exist_ok=True)
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(movie_list)
    print(f"Data saved to {filepath}")