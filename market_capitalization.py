import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import squarify

url = "https://www.companiesmarketcap.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# for table in soup.find_all('table'):
#     print(table.get('class'))

table = soup.find("table", class_="default-table table marketcap-table dataTable")
symbols = []
market_caps = []
sizes = []

row = table.tbody

symbols = [code.text.strip() for code in row.find_all("div", class_="company-code")]
market_caps = [market_cap.text.strip() for market_cap in row.find_all("td", class_='td-right') if market_cap.get("class")[0] == "td-right"][::2]

for market_cap in market_caps:
    if market_cap.endswith("T"):
        size = float(market_cap[1:-1]) * 1e12  # Trillion
    elif market_cap.endswith("B"):
        size = float(market_cap[1:-1]) * 1e9  # Billion
    else:
        size = float(market_cap[1:])  # In case no suffix is present
    sizes.append(size)


# plt.figure(figsize=(12, 8))
# squarify.plot(sizes=sizes, label=symbols, alpha=0.8)
# plt.title("Stock Market Capitalization of Top 100 Companies")
# plt.axis("off")
# plt.show()

plt.figure(figsize=(16, 10))
color_palette = plt.cm.PuBuGn
colors = [color_palette(i / len(sizes)) for i in range(len(sizes))]
squarify.plot(
    sizes=sizes,
    label=symbols,
    alpha=0.9,
    color=colors,
    text_kwargs={
        'fontsize': 9,
        'fontfamily': 'Verdana',
        'weight': 'bold',
        'color': 'black',
    },
    edgecolor='white',
    linewidth=1
)
plt.title(
    "Stock Market Capitalization of Top 100 Companies",
    fontsize=20,
    fontweight="bold",
    fontfamily="Verdana",
    color="darkgreen",
    pad=20
)

plt.axis("off")
plt.show()
