# from bs4 import BeautifulSoup as bs
# import requests
#
#
#
# def get_html(url):
#     response = requests.get(url)
#     return response.text
#
# def get_data(html):
#     soup = bs(html, 'lxml')
#     catalog = soup.find('div', class_='grid-list asdads')
#     items = catalog.find_all('div', class_='ty-column4')
#
#     for item in items:
#         try:
#             title = item.find('a', class_ = 'product-title').text()
#         except:
#             title = ''
#         try:
#             price = item.find('span', class_ = 'ty-price-num')
#         except:
#             price = ''
#         try:
#             image = item.find('img').get('src')
#         except:
#             image = ''
#
#         data = {
#             'title': title,
#             'price': price,
#             'image': image,
#         }
#
#         return data
#
#
# def main():
#     url = 'https://svetofor.info/sotovye-telefony-i-aksessuary/smartfony-xiaomi/'
#     html = get_html(url)
#     # get_data(html)
#     return get_data(html)
#     # print(html)
#     # return html
#
# if __name__ == '__main__':
#     main()
#
#
#
#
#
#
#
