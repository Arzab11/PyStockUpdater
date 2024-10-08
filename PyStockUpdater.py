from bs4 import BeautifulSoup
import requests 
import pandas as pd

top_five_stocks = []
stock_info = []

def get_5_stocks():
    url = "https://www.google.com/finance/markets/gainers?hl=en"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for stock in range(0,5):
        curr_stock1 = soup.find('div', {'class': 'T4LgNb'}).find_all('li')[stock]
        curr_stockfinal = curr_stock1.find('div', {'class': 'COaKTb'}).text 
        curr_stock1_specifier = soup.find('div', {'class': 'T4LgNb'}).find_all('li')[stock]
        a_tag = curr_stock1_specifier.find('a')
        if a_tag:
            href = a_tag['href']
            last_part = href.split(':')[-1]
            stock_info = {
                'Stock': curr_stockfinal,
                'link_identifier': last_part
            }
            top_five_stocks.append(stock_info)
    return top_five_stocks


def get_stock_data():
    for identifier in top_five_stocks:
        name = identifier['Stock']
        link = identifier['link_identifier']
        url = f'https://www.google.com/finance/quote/{name}:{link}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Checking for price
        price_div = soup.find('div', {'class': 'YMlKec fxKbKc'})
        price_div_text = price_div.text if price_div else "Price not found"

        if price_div_text != "Price not found":
            price = float(price_div_text.replace('$', '').strip())
        else:
            price = None

        # Checking for previous close
        previous_close_div = soup.find('div', {'class': 'P6K39c'})
        previous_close_text = previous_close_div.text.strip() if previous_close_div else "Previous close not found" 

        if previous_close_text != "Price not found":
            previous_close = float(previous_close_text.replace('$', '').strip())
        else:
            previous_close = None

        #Calculate Percentage Change
        percentage_change = ((price - previous_close)/(previous_close)) * 100
        percentage_change_format = f"{percentage_change:.2f}%"

        #Total Price Change
        price_change = (price - previous_close)
        if price_change > 0:
            price_change_format = f"+{price_change:.2f}"
        elif price_change == 0:
            price_change_format = price_change
        else:
            price_change_format = f"-{price_change:.2f}"

        stock = {
            'name': name,
            'price': price_div_text,
            'Previous Close': previous_close_text,
            'Percentage Change': percentage_change_format,
            'Price Change': price_change_format
        }
        stock_info.append(stock)
    return stock_info

get_5_stocks()
get_stock_data()
print(stock_info)

df = pd.DataFrame(stock_info)

output_file = 'C:\\Users\\Arzab Bhattarai\\OneDrive - Arzab_B\\Stock_Data\\stock_data.xlsx'
df.to_excel(output_file, index=False)
print(f"Data saved to {output_file}")
