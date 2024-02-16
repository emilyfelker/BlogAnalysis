import os
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Tuple


def list_dirs(folder_path: str) -> List[str]:
    return [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]


def get_blogpost_dataset(directory: str, number_of_files: int = -1) -> List[Tuple[str, datetime, str]]:
    blogpost_dataset = []
    for year in list_dirs(directory):  # loop through years
        for month in list_dirs(directory + "/" + year):  # loop through months
            for filename in os.listdir(directory + "/" + year + "/" + month):
                if not filename.endswith(".htm"):
                    continue
                full_path = os.path.join(directory, year, month, filename)
                blogpost_dataset.append(get_info_for_post(full_path))  # add relevant info to dataset
                if len(blogpost_dataset) == number_of_files:
                    return blogpost_dataset
    return blogpost_dataset


def get_info_for_post(location: str) -> Tuple[str, datetime.date, str]:
    with open(location, 'r') as file:
        post = file.read()
    soup = BeautifulSoup(post, 'html.parser')
    # get post title
    title = soup.find('title').text.split('|')[0].strip()
    # get post date
    date_str = soup.find('h3', class_='groupname date').find('span').text
    date = datetime.strptime(date_str, "%A, %d %B %Y").date()
    # get post body
    biggest = max(soup.find_all('div', class_='details'), key=len)
    content_selection = str(biggest).split('<div class="itemfooter">')[0].split("</h4>")[-1]
    content_formatted = content_selection.replace("<br/>", "\n")
    body = BeautifulSoup(content_formatted, 'html.parser').text
    return title, date, body


def get_database():
    # open the database connection
    connection = sqlite3.connect("data/gpt_data.db")
    cursor = connection.cursor()

    # check if table is present and if not, create it
    cursor.execute(f"PRAGMA table_info({'gpt_table'})")
    result = cursor.fetchall()
    if len(result) == 0:  # would result if database did not contain 'gpt_table' table
        cursor.execute("CREATE TABLE gpt_table (hash_query TEXT, model TEXT, response TEXT)")
    cursor.close()

    connection.commit()
    return connection


def add_to_database(connection, hash_query: str, model: str, response: str):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO gpt_table VALUES (?, ?, ?)", (hash_query, model, response))

    connection.commit()
    cursor.close()
    connection.close()


def get_response_from_database(connection, hash_query: str, model: str):
    cursor = connection.cursor()

    cursor.execute("SELECT response FROM gpt_table WHERE hash_query = ? AND model = ?", (hash_query, model))
    result = cursor.fetchone()  # Eventual test to add: what if there are multiple matches? Shouldn't be...

    if result is not None:
        if not len(result) == 1:
            raise LookupError(f"Expected only 1 result but found {str(len(result))}")
        return result[0]  # If matching row exists, return value from 'response' column
    else:
        print("no match found!")
        return None
