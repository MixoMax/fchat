import csv
import os

def filter_csv(chat_id):
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    input_file_path = "./data/" + chat_id + "/chat.csv"
    output_file_path = "./data/" + chat_id + "/filtered_chat.csv"
    with open(input_file_path, "r") as input_file, open(output_file_path, "w", newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        for row in reader:
            if any(row):
                writer.writerow(row)
    os.remove(input_file_path)
    os.rename(output_file_path, input_file_path)
    