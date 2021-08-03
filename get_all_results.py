from common_functions import *


def is_valid_search() -> []:
    """
    - Input: N.A.
    - Output: 7 -> [1], [2], [3] are drivers for ACM, Springer and IEEE; [4] search query gathered from IO; [5], [6], [7] are the number of pages to traverse when searching for results on ACM, Springer and IEEE
    - Number of essential steps (labeled below as comments): 4
    """
    try:
        # 1 - create drivers for each database
        driver_for_acm = make_chrome_headless(True)  # True hides automated browser
        print("Driver for ACM is ready.")
        driver_for_springer = make_chrome_headless(True)
        print("Driver for Springer is ready.")
        driver_for_ieee = make_chrome_headless(True)
        print("Driver for IEEE Xplore is ready.\n")
        driver_for_ieee.implicitly_wait(10)
        driver_for_springer.implicitly_wait(10)
        query = io_query()
        # 2 - driver visits links with user input term as search query and only check for results between years 2016 - 2021
        driver_for_acm.get(
            "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=Keyword&text1=%s&AfterMonth=1&AfterYear=2016&BeforeMonth=12&BeforeYear=2021"
            % quote(query)
        )
        driver_for_springer.get(
            f"https://link.springer.com/search?date-facet-mode=between&facet-end-year=2021&query=%22{quote(query)}%22&facet-content-type=%22ConferencePaper%22&showAll=true&facet-start-year=2016"
        )
        driver_for_ieee.get(
            f"https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Author%20Keywords%22:{quote(query)})&ranges=2016_2022_Year"
        )
        # 3 - parse max page numbers of results from first page of results
        # 3a - acm driver checks max page results
        source_code_acm = driver_for_acm.page_source
        soup_acm = BeautifulSoup(source_code_acm, "html.parser")
        try:
            temp_hits_acm = soup_acm.find("span", class_="hitsLength").text.strip()
            hits_acm = "".join(filter(str.isalnum, temp_hits_acm))
        except:
            hits_acm = 0
        hits_to_show_acm = int(25)
        max_pages_temp_acm = int(hits_acm) / hits_to_show_acm
        max_pages_acm = ceil(max_pages_temp_acm)
        # 3b - Springer driver parses max pages of results
        try:
            max_pages_springer = driver_for_springer.find_element_by_css_selector(
                "#kb-nav--main > div.functions-bar.functions-bar-top > form > span.page-nr > span.number-of-pages"
            ).text
        except:
            max_pages_springer = 0
        # 3c - ieee driver checks max page results
        try:
            num_hits_ieee = driver_for_ieee.find_element_by_css_selector(
                "#xplMainContent > div.ng-Dashboard > div.col > xpl-search-dashboard > section > div > div.Dashboard-header.col-12 > span:nth-child(1) > span:nth-child(2)"
            ).text
        except:
            num_hits_ieee = 0
        hits_to_show_ieee = int(25)
        max_pages_temp_ieee = int(num_hits_ieee) / hits_to_show_ieee
        max_pages_ieee = ceil(max_pages_temp_ieee)
        # 4 - return data to get_all_results()
        return [
            driver_for_acm,
            driver_for_springer,
            driver_for_ieee,
            query,
            int(max_pages_acm),
            int(max_pages_springer),
            int(max_pages_ieee),
        ]
    except Exception as e:
        fail_message(e)
        driver_for_acm.quit()
        print("Error! Driver for ACM has quit.")
        driver_for_springer.quit()
        print("Error! Driver for Springer has quit.")
        driver_for_ieee.quit()
        print("Error! Driver for IEEE Xplore has quit.")
        return []
    except KeyboardInterrupt as k:
        fail_message(k)
        print("Please wait for the ACM, Springer and IEEE Xplore drivers to quit...")
        driver_for_acm.quit()
        print("Error! Driver for ACM has quit.")
        driver_for_springer.quit()
        print("Error! Driver for Springer has quit.")
        driver_for_ieee.quit()
        print("Error! Driver for IEEE Xplore has quit.")
        return []


def get_all_results() -> bool:
    """
    - Input: N.A.
    - Output: bool (True/False) -> if True, then this function runs again
    - Number of essential steps (labeled below as comments): 5
    """
    try:
        # 1 - assign values from is_valid_search()
        (
            driver_for_acm,
            driver_for_springer,
            driver_for_ieee,
            query,
            max_pages_acm,
            max_pages_springer,
            max_pages_ieee,
        ) = itemgetter(0, 1, 2, 3, 4, 5, 6)(is_valid_search())
        # 2 - do IO to: (1) get similarity_percentage user wants, (2) create file for results, and (3) let user know that drivers are starting to find & place results now
        similarity_percentage, sp = itemgetter(0, 1)(sp_io())
        file_path = create_file(config.path_to_search_results)
        print_checking_all_results(sp)
        # 3 - create a list of titles to append to in order to prevent duplicate additions
        added_titles = []
        result_count = 0  # keep track of how many results are added to the final list
        # 4 - check all databases
        # 4a - check acm first
        print("Checking results in ACM:")
        with open(str(file_path), "w", encoding="UTF8", newline="") as f:
            # create the csv writer
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            k = 0  # counts how many results match selected journals/conferences
            for i in range(int(max_pages_acm)):  # traverse each page
                t = i + 1
                # print(f"Checking results on page {t}...")
                driver_for_acm.get(
                    "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=Keyword&text1=%s&AfterMonth=1&AfterYear=2016&BeforeMonth=12&BeforeYear=2021&startPage=%s&pageSize=%s"
                    % (quote(query), str(i), "25")
                )
                # parse source code
                soup = BeautifulSoup(driver_for_acm.page_source, "html.parser")
                # Get the result containers
                result_containers = soup.findAll("div", class_="issue-item__content")
                j = 0  # set increment representing how many hits the user wants to traverse
                # Loop through every container
                for container in result_containers:
                    # Final results list
                    results = []
                    # check if result journal is in list of selected journals
                    journal = container.find("div", class_="issue-item__detail").a[
                        "title"
                    ]
                    for matched_with in list_of_selected_jc:
                        if ratio(journal, matched_with) >= similarity_percentage:
                            # Result title
                            title_tmp = container.find("h5").text
                            title = title_tmp.strip("'")
                            if (
                                added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                added_titles.append(title)
                                k += 1
                                result_count += 1
                                print(
                                    f"Placed {k} results from ACM and {result_count} in total so far! Still checking..."
                                )
                                # Result url
                                temp_url = container.find("h5").a["href"]
                                lst = ["https:/", temp_url[:4], ".org", temp_url[4:]]
                                url = "".join(lst)
                                # Result authors
                                authors = []
                                ul = container.find("ul")
                                for li in ul.findAll("li"):  # list of authors
                                    authors.append(li.text.rstrip(", \n").strip("'"))
                                t_author_list = str(authors).strip("[]")
                                author_list = t_author_list.replace("'", "")
                                # Result date
                                date = (
                                    container.find("div", class_="issue-item__detail")
                                    .find("span", class_="dot-separator")
                                    .find("span")
                                    .text.rstrip(", ")
                                )
                                numbers = compile(r"\d+(?:\.\d+)?")
                                p_year = numbers.findall(date)[0]
                                # Result num
                                j += 1
                                # Similarity %
                                t_sim_per = ratio(journal, matched_with) * 100
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "ACM",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
        driver_for_acm.quit()
        print("Done! Driver for ACM has quit.")
        # 4b - check springer second
        i_springer = (
            0  # set increment representing how many pages the user wants to traverse
        )
        print("Checking results in Springer:")
        with open(str(file_path), "a+", encoding="UTF8", newline="") as f:
            # create the csv writer
            writer = csv.writer(f)
            # list of journal names to append to to prevent duplicate additions
            added_titles = []
            k = 0  # counts how many results match selected journals/conferences
            for i in range(int(max_pages_springer)):  # traverse each page
                t = i + 1
                # print(f"Checking results on page {t}...")
                driver_for_springer.get(
                    f"https://link.springer.com/search/page/{str(t)}?date-facet-mode=between&facet-end-year=2021&query=%22{quote(query)}%22&facet-content-type=%22ConferencePaper%22&showAll=true&facet-start-year=2016"
                )
                results_per_page = driver_for_springer.find_elements_by_css_selector(
                    "#results-list li"
                )
                j = 0  # set increment representing how many hits the user wants to traverse
                # Loop through every container
                for result in results_per_page:
                    # Final results list
                    results = []
                    # Result journal title
                    journal = result.find_element_by_class_name(
                        "publication-title"
                    ).get_attribute("title")
                    for matched_with in list_of_selected_jc:
                        if ratio(journal, matched_with) >= similarity_percentage:
                            # Result title
                            title = result.find_element_by_tag_name("h2").text
                            added_titles.append(title)
                            if (
                                added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                k += 1
                                result_count += 1
                                print(
                                    f"Placed {k} results from Springer and {result_count} in total so far! Still checking..."
                                )
                                # Result url
                                links = result.find_element_by_tag_name(
                                    "h2"
                                ).find_elements_by_tag_name("a")
                                url = "None"
                                for link in links:
                                    url = link.get_attribute("href")
                                # Result author(s)
                                t_author_list = []
                                a_list = result.find_element_by_class_name(
                                    "authors"
                                ).text
                                b_list = ""
                                try:
                                    b_list = (
                                        result.find_element_by_class_name("authors")
                                        .find_element_by_tag_name("span")
                                        .get_attribute("title")
                                    )
                                except:
                                    pass
                                full = a_list + b_list
                                t_author_list.append(full)
                                t2_author_list = str(t_author_list).strip("[]")
                                t3author_list = t2_author_list.replace("'", "")
                                author_list = t3author_list.replace("…", ", ")
                                # Result publish year
                                p_year = result.find_element_by_class_name(
                                    "year"
                                ).get_attribute("title")
                                # Result num
                                j += 1
                                # Similarity %
                                t_sim_per = ratio(journal, matched_with) * 100
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "Springer",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
        driver_for_springer.quit()
        print("Done! Driver for Springer has quit.")
        # 4c - check ieee third
        print("Checking results in IEEE:")
        with open(str(file_path), "a+", encoding="UTF8", newline="") as f:
            # create the csv writer
            writer = csv.writer(f)
            k = 0  # counts how many results match selected journals/conferences
            for i in range(1, int(max_pages_ieee) + 1):
                # print(f"Checking results on page {i}...")
                driver_for_ieee.get(
                    f"https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Author%20Keywords%22:{quote(query)})&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber={str(i)}&ranges=2016_2022_Year&returnFacets=ALL&rowsPerPage=25"
                )
                results_per_page = driver_for_ieee.find_elements_by_class_name(
                    "List-results-items"
                )
                for result in results_per_page:
                    # Final results list
                    results = []
                    # Result title
                    # check if result journal is in list of selected journals
                    try:
                        journal = (
                            result.find_element_by_class_name("description")
                            .find_element_by_tag_name("a")
                            .text
                        )
                    except:
                        journal = "No journal name found"
                    for matched_with in list_of_selected_jc:
                        if ratio(journal, matched_with) >= similarity_percentage:
                            # Result title
                            title = result.find_element_by_tag_name("h2").text
                            added_titles.append(title)
                            if (
                                added_titles.count(title) == 0
                            ):  # only add to result CSV if title hasn't been added already
                                k += 1
                                result_count += 1
                                print(
                                    f"Placed {k} results from IEEE and {result_count} in total so far! Still checking..."
                                )
                                # Result url
                                links = result.find_element_by_tag_name(
                                    "h2"
                                ).find_elements_by_tag_name("a")
                                url = "None"
                                for link in links:
                                    url = link.get_attribute("href")
                                # Result author_list
                                t1author_list = []
                                t1author_list.append(
                                    result.find_element_by_class_name(
                                        "author"
                                    ).text.replace(";", ", ")
                                )
                                t_author_list = str(t1author_list).strip("[]")
                                author_list = t_author_list.replace("'", "")
                                # Result publish year
                                p_year_t1 = (
                                    result.find_element_by_class_name(
                                        "publisher-info-container"
                                    )
                                    .find_element_by_tag_name("span")
                                    .text.lstrip(ascii_letters)
                                )
                                p_year = p_year_t1.lstrip(": ")
                                # Similarity %
                                t_sim_per = ratio(journal, matched_with) * 100
                                sim_per = format(t_sim_per, ".2f")
                                data = [
                                    url,
                                    title,
                                    author_list,
                                    p_year,
                                    journal,
                                    matched_with,
                                    sim_per,
                                    "IEEE",
                                    query,
                                ]
                                # write the data
                                writer.writerow(data)
        driver_for_ieee.quit()
        print("Done! Driver for IEEE Xplore has quit.")
        # 5 - let user know this round of searching for & placing results is finished
        print(f"Done! Placed {result_count} results in total.\n")
        return True
    except Exception as e:
        fail_message(e)
        driver_for_acm.quit()
        print("Error! Driver for ACM has quit.")
        driver_for_springer.quit()
        print("Error! Driver for Springer has quit.")
        driver_for_ieee.quit()
        print("Error! Driver for IEEE Xplore has quit.")
        return False
    except KeyboardInterrupt as k:
        fail_message(k)
        print("Please wait for the ACM, Springer and IEEE Xplore drivers to quit...")
        driver_for_acm.quit()
        print("Error! Driver for ACM has quit.")
        driver_for_springer.quit()
        print("Error! Driver for Springer has quit.")
        driver_for_ieee.quit()
        print("Error! Driver for IEEE Xplore has quit.")
        return False


def main():
    while True:
        get_all_results()


if __name__ == "__main__":
    main()
