from selenium import webdriver
from typing import List
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from Levenshtein import ratio
from urllib.parse import quote
from bs4 import BeautifulSoup
from os import path, makedirs
from math import ceil
from operator import itemgetter
from string import ascii_letters
from sys import platform
import re
import subprocess
import csv
import config


def make_chrome_headless(o=True):
    """
    Return a headless driver of Chrome
    """
    options = Options()
    if o:
        options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    headless_driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options,
    )
    return headless_driver


def create_list_of_selected_jc() -> List:
    """
    Return the "SelectedJournalsAndConferences.csv" as a list
    """
    selected_jc = []
    with open("SelectedJournalsAndConferences.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            selected_jc.append(row["Name"])
    selected_jc.pop(0)
    return selected_jc


def io_query() -> str:
    """
    IO: returns search term
    """
    return input("Enter your search term here: ")


def io_hits_to_show(database) -> int:
    """
    IO: returns how many hits to search for per page
    """
    if database == "ACM":
        return input(
            "How many hits would you like to search for per page? (max = 50): "
        )
    return input(
        "How many hits would you like to search for per page? (10, 25, 50, or 75): "
    )


def create_file(path_to_search_results) -> str:
    """
    Return file path
    """
    file_name = input(
        "Enter a file name where you would like to store the search results: "
    )
    if not path.exists(path_to_search_results):
        makedirs(path_to_search_results)
    file_path = path.join(path_to_search_results, str(file_name + ".csv"))
    return file_path


def fail_message(e):
    """
    Print failure message
    """
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(e).__name__, e.args)
    print(message)


def print_checking_results(num_results, sp):
    """
    IO: print status to show results are getting checked
    *unused
    """
    print(
        "Checking "
        + str(num_results)
        + " results where journal/conference name matches selected ones by "
        + str(sp)
        + chr(37)
    )


def print_checking_all_results(sp):
    """
    IO: print status to show results are getting checked
    """
    print(
        "Checking all results where journal/conference name matches selected ones by "
        + str(sp)
        + chr(37)
    )


def sp_io() -> List:
    """
    Return (1) similarity percentage [0, 1] and (2) sp [0, 100]
    - The similarity corresponds to the minimum percentage likeness between the journal/conference name of each result and those listed in "SelectedJournalsAndConferences.csv"
    """
    similarity_percentage = float(
        input(
            "What is the minimum percentage likeness you like to check against the selected journals/conferences (choose between 0.0 and 1.0): "
        )
    )
    sp = similarity_percentage * 100
    return [similarity_percentage, sp]


def io_pages_to_show(
    database,
    max_pages,
    num_results_per_page=0,
) -> int:
    """
    IO: returns how many pages to search
    """
    if database == "Springer":
        return input(
            "How many pages would you like to see the results for? (max = %s and results per page = %s): "
            % (str(max_pages), str(num_results_per_page))
        )
    return input(
        "How many pages would you like to see the results for? (max = "
        + str(max_pages)
        + "): "
    )


# result CSV file's header
header = [
    "URL",
    "Title",
    "Author(s)",
    "Year",
    "Journal",
    "Matched with Selected Journal/Conference",
    "Similarity %",
    "Database",
    "Query",
]

# create list of selected journals and conferences using below function
list_of_selected_jc = create_list_of_selected_jc()
