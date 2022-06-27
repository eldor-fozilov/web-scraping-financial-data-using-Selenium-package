from selenium import webdriver
from selenium.webdriver.common.by import By
# import chromedriver_autoinstaller  # pip install chromedriver-autoinstaller

import requests


# Get free proxies for rotating
def get_free_proxies(driver):
    driver.get('https://sslproxies.org')

    table = driver.find_element(By.TAG_NAME, 'table')
    thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, 'td')
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)

    return proxies





def select_proxy(proxies_dict):
    url = "http://ipinfo.io"
    failed_indexes = []
    for i in range(len(proxies_dict)):
        try:
            proxy = f"{proxies_dict[i]['IP Address']}:{proxies_dict[i]['Port']}"
            # print(proxy)
            response = requests.get(url, proxies = {"http":proxy, "https":proxy})
            failed_indexes.append(i)
            for idx in failed_indexes:
                proxies_dict.remove(proxies_dict[idx])
            return proxies_dict, proxy
        except:
            # print("Failed ", i)
            failed_indexes.append(i)
            # proxies_dict.remove(proxies_dict[i])



if __name__ == "__main__":
    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()  # To update your chromedriver automatically

    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)

    print("Collecting Proxies ....")
    free_proxies = get_free_proxies(driver)
    print("Proxies Collected....")
    print("Choosing Proxy ....")
    free_proxies, proxy = select_proxy(free_proxies)

    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.unist.ac.kr")

