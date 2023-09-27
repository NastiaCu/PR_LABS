from crawling import crawling
from scraper import scraper

if __name__ == "__main__":
    rent_car = crawling("https://m.999.md/ru/list/transport/rent-a-car?page={}", maxNumPage=2)
    scrap = scraper(rent_car, 10)