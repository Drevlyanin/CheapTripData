from scraping import scrap
from extraction import extract
from treatment import treat
from fixing import fixing_price


def main():
    
    scrap()
    
    extract()
    
    treat()

    fixing_price()


if __name__ == '__main__':
    main()