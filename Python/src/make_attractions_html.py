import json
from config import SEO_CITY_DESCRIPTIONS_DIR, SEO_HTMLS_DIR, SEO_CITY_ATTRACTIONS_DIR
from pathlib import Path


def make_html():
    
    SEO_HTMLS_DIR.mkdir(parents=True, exist_ok=True)

    # Loop over the JSON files and extract the text
    text = ""
    files = sorted(list(Path(SEO_CITY_ATTRACTIONS_DIR).glob('*.json')))
    for i, file in enumerate(files, start=1):
        city = file.name.partition('.')[0]
        with open(file, 'r') as json_file:
            content = json.load(json_file)
        header = f'Most popular free and low-cost attractions in {city}'
        text += f'<h2>{header}</h2>'
        for key, value in content.items():
            attraction_name = key
            attraction_description = value['text']
            text += f'<h3>{attraction_name}</h3><p>{attraction_description}</p>'
          
    # Generate the HTML content
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>City attractions</title>
        <meta name="description" content="Budget Travel Tips, budget-friendly accommodations, cheap eats, free and low-cost attractions, walking tours, and public transportation options to explore the city without breaking the bank. Tips to budget travellers. Start planning your exciting journey with CheapTrip.Guru at a cost-effective advantage for your budget.">
        <meta name="keywords" content="budget travel, cheapest way, low-cost accommodations, cheap eats, free attractions, walking tours, public transportation, affordable trip, CheapTrip.Guru">
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: sans-serif;
                font-size: 16px;
                line-height: 1.5;
                color: #333333;
            }}
            h2 {{
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 0.5em;
            }}
            h3 {{
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 0.5em;
            }}
            p {{
                margin-bottom: 1.2em;
            }}
        </style>
    </head>
    <body>
        <p>{text}</p>
    </body>
    </html>
    """

    # Save the HTML content to a file
    with open(f'{SEO_HTMLS_DIR}/city_attractions.html', "w") as f:
        f.write(html)


if __name__ == '__main__':
    make_html()