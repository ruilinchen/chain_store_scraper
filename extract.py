import os
import re
import itertools
from datetime import datetime
from lxml import html
from utils.globals import ALL_PRODUCT_TYPES
import pandas as pd

web_name = 'accmarket'

def _extract_date(file_name, web_name):
    file_info = file_name[len(web_name):]
    info_list = file_info.split('_')
    date_str = ''
    for info in info_list:
        if len(info) == 8 and info.isdigit():
            date_str = info
            break
    return datetime.strptime(date_str.strip(), '%m%d%Y')


def get_price(file_name):
    tree = html.fromstring(open(os.path.join(web_name, file_name)).read())
    product_str_list = tree.xpath("//table[@class='table1']/tbody/tr/td/text()")
    product_str_list = [p_str for p_str in product_str_list if len(p_str) > 5]
    price_dict = {'ebay': {'sale': [], 'account': []}, 
                    'card': {'sale': [], 'account': []}, 
                    'paypal': {'sale': [], 'account': []}}
    product_type = None
    for product_str in product_str_list:
        if 'account' in product_str:
            if 'Ebay' in product_str:
                product_type = 'ebay'
            elif 'Bank' in product_str:
                product_type = 'card'
            else:
                product_type = 'paypal'
        else:
            price_list = re.findall("([0-9]+[,.]?[0-9]+)", product_str)
            price_list = list(map(float, price_list))
            price_dict[product_type]['account'].append(price_list[0])
            price_dict[product_type]['sale'].append(price_list[1])


    date = _extract_date(file_name, web_name)
    df = None
    for product_type in price_dict.keys():
        tmp_df = pd.DataFrame(columns=['date', 'product_type', 'web_name', 'account_price', 'sale_price'])
        tmp_df['sale_price'] = price_dict[product_type]['sale']
        tmp_df['account_price'] = price_dict[product_type]['account']
        tmp_df['date'] = date.strftime('%m/%d/%Y')
        tmp_df['web_name'] = web_name
        tmp_df['product_type'] = product_type
        if df is None:
            df = tmp_df
        else:
            df = pd.concat([df, tmp_df])
    return df

