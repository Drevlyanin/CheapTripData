# Scrappers for [cheaptrip.guru](https://cheaptrip.guru/)

## Overview
<p align="justify">
Theis is my first scrappers. 
They were built for getting the minimal price in EUR(€) to get from one city to another.
The project only supports European cities for now.
The route can have mixed types of transport but the total price includes the cost of all tickets.
There are two different scrappers in the project but for the same purposes: one scrapper uses previously inspected API calls the site makes, and another scrapper was implemented using Selenium framework to imitate the real user behaviour.
I've chosen Selenium because it's also a great way to scrape JS rendered websites.
</p>



## Installation

### Clone the repo
```bash
git clone https://github.com/VoorheesDev/CheapTripGuru_scrapping.git
cd CheapTripGuru_scrapping
```

### Create and activate a virtual environment
+ For <b>Linux</b>:
```bash
python3 -m venv venv
source venv/bin/activate
```

+ For <b>Windows</b>:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Install requirements
```bash
pip install -r requirements.txt
```

## Usage
Run the first scrapper using `python` or `python3` command, provide 2 city names as an arguments: the starting point and the destination:
```bash
python min_price_between_cities.py <fromCity> <toCity>
```
Or you can try another approach using Selenium in Docker:
```bash
docker build -t scrapper .
docker run --rm scrapper <fromCity> <toCity>
```
