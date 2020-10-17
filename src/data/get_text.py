import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


def get_data_from_table(site, site_table):

    driver.get(site)

    head = len(driver.find_elements_by_xpath(f'{site_table}/thead/tr[1]/th'))  # Count number of feature names
    rows = len(driver.find_elements_by_xpath(f'{site_table}/tbody/tr'))  # Count number of rows
    cols = len(driver.find_elements_by_xpath(f'{site_table}/tbody/tr[1]/td'))  # Count number of cols

    table = []
    features = []
    for feature in range(1, head + 1):
        feature_names = driver.find_element_by_xpath(
            f'{site_table}/thead/tr[1]/th[{str(feature)}]').text
        features.append(feature_names)
    table.append(features)
    for row in range(1, rows + 1):
        samples = []
        year = driver.find_element_by_xpath(
            f'{site_table}/tbody/tr[{str(row)}]/th[1]').text
        samples.append(year)
        for col in range(1, cols + 1):
            sample = driver.find_element_by_xpath(
                f'{site_table}/tbody/tr[{str(row)}]/td[{str(col)}]').text
            samples.append(sample)
        table.append(samples)
    return table


sites = ['https://www.f1-fansite.com/f1-results/f1-champions',
         'https://www.f1-fansite.com/f1-results/all-time-f1-driver-rankings',
         'https://www.f1-fansite.com/f1-results/all-time-f1-team-rankings',
         'https://www.f1-fansite.com/f1-results/all-time-f1-engine-brand-ranking',
         'https://www.f1-fansite.com/f1-results/time-f1-list-drivers-country']

site_table = '//*[@id="header"]/div[2]/div[4]/div/div[1]/div[2]/table'


for site in sites:
    with open(f'{site.split("/")[-1]}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        table = get_data_from_table(str(site), str(site_table))
        for line in table:
            writer.writerow(line)