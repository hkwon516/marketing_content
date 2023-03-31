import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

all_paths = []

driver = webdriver.Chrome()
driver.get("https://marketingexamples.com/")

for i in range(20):
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all("a", {"class": "card bingo"})
    contents = os.path.join(os.getcwd() + "/venv/contents.md")
    print(results)

    for result in results:
        page = "https://marketingexamples.com" + result.get('href')
        request_to_page = requests.get(page)
        soup_per_page = BeautifulSoup(request_to_page.content, "html.parser")

        #get the modal_for_each_page
        modal_for_each_page = soup_per_page.find("article", {"class" : "post"})

        with open("contents.md", 'w+') as f:
            for child in modal_for_each_page.findChildren():
                if child.name == "h1":
                    # print(child.get_text())
                    f.write("# " + child.get_text() + "\n" * 2)
                elif child.name == "h2" :
                    f.write("## " + child.get_text()  + "\n" * 2)
                elif child.name == "h3" :
                    f.write("### " + child.get_text() + "\n" * 2)
                elif child.name == "img" :
                    print(child["src"] + "\n" * 2)
                    f.write("![Image](" + child["src"] +")" + "\n" * 2)
                elif child.name == "p":
                    f.write(child.get_text() + "\n" * 2)
driver.quit()