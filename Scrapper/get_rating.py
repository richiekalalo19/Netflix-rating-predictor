import pandas as pd
from imdb_scraper import get_rating
import threading
import time
import os
from sort_txt import sorted_file

file_name = "netflix_titles copy.csv"
data = pd.read_csv(file_name)

thread_list = []
MAX_THREADS = 10
BATCH_SIZE = 500
save_file = "rating.txt"
sorted_file_name = "sorted.txt"

def rating(title, index):
    with open(save_file, 'a') as file:
        try:
            rating = get_rating(title)
            if rating:
                file.write(f"{index}:{title}:{rating}\n")
            else:
                file.write(f"{index}:{title}:NONE\n")
        except UnicodeEncodeError:
            file.write(f"{index}:[ERROR]\n")

def get_batch():
    if sorted_file_name in os.listdir():
        with open(sorted_file_name, 'r') as file:
            data = file.read().split('\n')
            last_row = data[-2].split(':')
            return int(last_row[0])
    return 0

batch_start = get_batch()
if batch_start + BATCH_SIZE < len(data['title']):
    batch_end = batch_start+BATCH_SIZE
else:
    batch_end = len(data['title'])

def batch_process():
    while batch_start < batch_end:
        if len(thread_list) < MAX_THREADS:
            thread = threading.Thread(target=rating, args=[data["title"][batch_start], batch_start])
            thread.start()
            thread_list.append(thread)
            batch_start += 1
        
        for ind, thread in enumerate(thread_list):
            if thread.is_alive():
                pass
            else:
                thread_list.pop(ind)

def get_missing():
    batch_start = 0
    with open('sorted.txt', 'r') as file:
        rows = file.read().split('\n')
        rows = rows[:-1]
        it_no = [int(i.split(':')[0]) for i in rows]
        print(it_no)

    while batch_start < len(data['title']):
        if batch_start not in it_no:
            if len(thread_list) < MAX_THREADS:
                thread = threading.Thread(target=rating, args=[data["title"][batch_start], batch_start])
                thread.start()
                thread_list.append(thread)
                batch_start += 1
            
            for ind, thread in enumerate(thread_list):
                if thread.is_alive():
                    pass
                else:
                    thread_list.pop(ind)
        else:
            batch_start += 1

def check_threads():
    while thread_list:
        for ind, thread in enumerate(thread_list):
            if thread.is_alive():
                pass
            else:
                thread_list.pop(ind)

def cleanup():
    sorted_file(file_to_sort=save_file, sorted_file_name=sorted_file_name)
    while True:
        try:
            os.remove(save_file)
            break
        except PermissionError:
            pass

def sort_files(file_to_sort, file_to_append):
    sorted_file(file_to_sort=file_to_append, sorted_file_name=file_to_append)
