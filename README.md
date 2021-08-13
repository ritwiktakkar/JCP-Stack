  <h2 align="center">JCP-Stack</h2>

  <p align="center">
    An efficient way to scrape results from the ACM, Springer, and IEEE Xplore digital libraries
    <br />
    <a href="">View Demo **TO-DO**</a> <!-- TODO: add link to video demo on website (embedded youtube link) -->
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#onomatology">Onomatology</a></li>
        <li><a href="#dependencies">Dependencies</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#steps">Steps</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#status">Status</a></li>
    <li><a href="#issues">Issues</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to help researchers find and sort papers from the ACM, Springer, and IEEE Xplore online databases efficiently. I have compiled a list of 291 journals and conferences with their CCF, Core and Qualis rankings in `SelectedJournalsAndConferences.csv`. This web scraper compares the [similarity (Levenshtein ratio)](https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-ratio) between every single search result's journal/conference title and those listed in `SelectedJournalsAndConferences.csv`. If the similarity between them is greater than or equal to a user-specified percentage, then the result is placed in a CSV file whose path and name is also selected by the user. Once the web scraper has completed traversing each page generated by the user's search term, analyzing the results therein, and storing the ones that fit the given criteria, it alerts the user of its status prior to restarting. 

### Onomatology

"JCP-Stack" is short for "Journal/Conference Paper Stack" given that executing this program (ideally) outputs a CSV file that contains information about a stack of journal/conference papers related to a given keyword. 

### Dependencies

* appdirs==1.4.4
* beautifulsoup4==4.9.3
* black==21.6b0
* certifi==2021.5.30
* charset-normalizer==2.0.3
* click==8.0.1
* colorama==0.4.4
* configparser==5.0.2
* crayons==0.4.0
* idna==3.2
* levenshtein==0.12.0
* mypy-extensions==0.4.3
* pathspec==0.9.0
* regex==2021.4.4
* requests==2.26.0
* selenium==3.141.0
* soupsieve==2.2.1
* toml==0.10.2
* urllib3==1.26.5
* webdriver-manager==3.4.2



<!-- GETTING STARTED -->

## Getting Started

To get this project running on your local machine, follow these simple steps:

### Steps

1. Clone the repo
   ```sh
   git clone https://github.com/ritwiktakkar/rdb-scraper.git
   ```
2. Make sure you're running Python 3 (I wrote and tested this project with Python 3.9.6 64-bit)
   ```sh
   python -V
   ```
3. Install all the packages specified in the configuration file (`requirements.txt`)
   ```sh
   pip install -r requirements.txt
   ```
4. You will need the [latest](https://www.google.com/intl/en_us/chrome/) version of Google Chrome installed on your machine
5. Create a file called `config.py` inside this repo and add the following:
   ```py
   from common_functions import platform

   if platform == "win32":
       path_to_search_results = "C:/<PATH TO SEARCH RESULTS>"
   else:
       path_to_search_results = "/Users/<PATH TO SEARCH RESULTS>"
   ``` 
6. View the "Name" column inside `SelectedJournalsAndConferences.csv`: this is the list of names whose [similarity (Levenshtein ratio)](https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-ratio) will be checked against each search result's journal/conference name. Feel free to modify this column on your local machine to add/remove journal names (not) of interest to you. 
7. Execute `get_all_results.py` using Python
   ```sh
   PATH_TO_PYTHON_INTERPRETER PATH_TO_get_all_results.py
   ``` 



<!-- USAGE EXAMPLES -->
## Usage
<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources. -->

**TO-DO**



<!-- STATUS -->
## Status
Given that the layouts of online research databases are updated occasionally, the scraper may also need to be updated acordingly to successfully retrieve the necessary information therein. The table below provides the current status of the scraper's ability to retrieve information from different online research databases.
|  Database   | Scraper Status |
| :---------: | :------------: |
|     ACM     |       ✅        |
|  Springer   |       ❌        |
| IEEE Xplore |       ❌        |



<!-- ISSUES -->
## Issues
On Windows only: Selenium's quit() method alone fails to kill chromedriver processes thereby leading to a sort of memory leak. To counter this, I added a batch file (`kill_chromedriver.bat`) that kills all `chrome.exe` processes. As a result, ANY Chrome process unrelated to this program will ALSO die at the hands of this rather brute approach.  



<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact
📧 rt398 [at] cornell [dot] edu

🏠 [ritwiktakkar.com](https://ritwiktakkar.com)

Project Link: [https://github.com/ritwiktakkar/JCP-Stack](https://github.com/ritwiktakkar/JCP-Stack)
