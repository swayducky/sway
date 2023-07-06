import requests
from html2text import html2text
import tiktoken


def scrape(url):
    response = requests.get(url)
    return html2text(response.text)

def dump():
    text = scrape('https://www.getcerta.com/contract')
    with open('page.txt', 'w') as f:
        f.write(text)
    print("Saved!", len(text), "chars")


def measure():
    with open('page.txt', 'r') as f:
        text = f.read()
    enc = tiktoken.encoding_for_model("gpt-4")
    encoding = enc.encode(text)
    print(len(encoding), 'tokens!')

if __name__ == "__main__":
    dump()
    measure()
