import time

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from lgbt import lgbt


def online_split(all_onl):
    all_current = []
    all_max = []
    for text in all_onl:
        parts = text.split('/')
        all_current.append(parts[0])
        all_max.append(parts[1])
    return all_current, all_max


def parse(pages_amount):
    print('Starting webdriver...')

    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    ranks = []
    names = []
    addresses = []
    cur_online = []
    max_online = []
    statuses = []

    print('Starting parsing...')

    pages_bar = lgbt(range(pages_amount), desc="pages", hero='unicorn')

    for page in pages_bar:
        url = f"https://minecraftservers.org/index/{page+1}"
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        all_ranks = soup.find_all(class_="rank")
        all_ranks = all_ranks[1::2]
        all_ranks_text = [(a.text.replace('\n', "")
                           if a.text.replace('\n', "") != ''
                           else 'featured')
                          for a in all_ranks]
        ranks.extend(all_ranks_text)

        all_names = soup.find_all('a', href=lambda
                                  value: value and '/server/' in value)
        all_names = all_names[::4]
        all_names_text = [a.text for a in all_names]
        names.extend(all_names_text)

        all_addresses = soup.find_all(class_="server")
        all_addresses = all_addresses[1::2]
        all_addresses_text = [a.text.replace('\n', "").replace('Copy', "")
                              for a in all_addresses]
        addresses.extend(all_addresses_text)

        all_online = soup.find_all(class_="value")
        all_online = all_online[::4]
        all_online_list = [a.text for a in all_online]
        all_current_online, all_max_online = online_split(all_online_list)

        cur_online.extend(all_current_online)
        max_online.extend(all_max_online)

        all_statuses = soup.find_all(class_="value online")
        all_statuses_text = [a.text for a in all_statuses]
        all_statuses_text = all_statuses_text[::2]
        statuses.extend(all_statuses_text)

    print('Saving data...')
    result = zip(ranks, names, addresses, cur_online, max_online, statuses)

    print('Parsing complete! Quitting driver...')
    driver.quit()
    return result


def data_to_csv(input_data):
    print('Saving to csv...')

    dataframe = pd.DataFrame(input_data, columns=["Ranks", "Name",
                                                  "Address", "Current online",
                                                  "Maximum online", "Status"])
    dataframe.to_csv('servers.csv', index=False, encoding="utf-8")

    print('Saved to servers.csv')


data = parse(20)
data_to_csv(data)
