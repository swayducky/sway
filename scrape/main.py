import requests
from html2text import html2text

def scrape(url):
    response = requests.get(url)
    return html2text(response.text)

if __name__ == "__main__":
    text = scrape('https://www.getcerta.com/')
    print(text)
    with open('page.txt', 'w') as f:
        f.write(text)
