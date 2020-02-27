import pandas as pd


def get_unique_products(data, atc, zone1, zone2, zone3):
    products = data.loc[(data.ATC == atc) &
                        (data.사업부 == zone1) &
                        (data.사무소 == zone2) &
                        (data.지역 == zone3), '제품']
    return products.unique().tolist()


def get_sales(data, products, date):
    """:arg
    date: has to be entered in format YYYY-MM
    example --> 2019-11

    return pandas DataFrame
    """
    date = '처방조제액-' + date
    # get the total ammount sold on this date for every product
    sales_values = []
    for product in products:
        sales_values.append(data.loc[data.제품 == product, date].sum())
    sales = pd.DataFrame(products, columns=['Product'])
    sales['Sales'] = sales_values
    sales['Percentage'] = sales.Sales.apply(lambda x: x/sales_2019_01.Sales.sum()*100)
    
    sales.sort_values(by='Sales', ascending=False, inplace=True)

    return sales


raw_data = pd.read_csv('static/data/new_ubist_data.csv')
unique_products = get_unique_products(raw_data,
                                      '[A2B2] 프로톤 펌프 억제제',
                                      '서울1',
                                      '병원강원',
                                      '강원도강릉시')

sales_2019_01 = get_sales(raw_data, unique_products, '2019-11')
