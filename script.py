import json
import csv
import pandas as pd
import requests

def get_json(url,limit,page):
    try:
        r = requests.get(url+f"/products.json?limit={limit}&page={page}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as errh:
        print(f'Erreur http : {errh}')
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Connexion impossible : {errc}")
        return None
    except requests.exceptions.ReadTimeout as errt:
        print(f'Délai dépassé {errt}')
        return None
    except requests.exceptions.RequestException as errx:
        print(f'Erreur : {errx}')
        return None
    
    
def json_to_df(jsonFile):
    df = pd.DataFrame(jsonFile)
    return df

def get_products(url, limit=10):
    page = 1
    all_products = []
    
    while True:
        data = get_json(url,limit,page)
        if not data or 'products' not in data:
            break
        
        for product in data['products']:
            images_src = product['images'][0]['src'] if product['images'] else None
            
            product_price = product['variants'][0]['price'] if product['variants'] else None
            
            product_weight = product['variants'][0]['grams'] if product['variants'] else None
            
            product_regular_price = product['variants'][0]['compare_at_price'] if product['variants'] else None
            
            product_variable_position = product['variants'][0]['position'] if product['variants'] else None
            
            product_attribute_name = product['options'][0]['name'] if product['options'] else None
            
            product_attribute_values = product['options'][0]['values'] if product['options'] else None
            
            if product['variants'][0]['featured_image'] == None:
                product_featured = 0
            else :
                product_featured = 1
                
            if product['variants'][0]['taxable'] == True:
                product_taxable = 'shipping'
            else :
                product_taxable = ''
                
            product_dict = {
                'ID' : product['id'],
                'Name' : product['title'],
                'SKU' : product['handle'],
                'Is featured?' : product_featured,
                'Tax status' : product_taxable,
                'Tax class' : 'standard',
                'Published' : 1,
                'Visibility in catalog' : 'visible',
                'Weight (kg)' : product_weight/2.205,
                'Sale price' : product_price,
                'Regular price' : product_regular_price,
                'Short description' : 'This is a simple product.',
                'description' : product['body_html'],
                'Categories' : product['product_type'],
                'Tags' : product['tags'],
                'Images' : images_src,
                'Position' : product_variable_position,
                'Attribute 1 name' : product_attribute_name,
                'Attribute 1 value(s)' : product_attribute_values
            }
            all_products.append(product_dict)
        
        if page > 10:
            break
        page += 1
        
    df_product = json_to_df(all_products)
    df_product.reset_index(drop=True, inplace=True)
    return df_product

def get_csv(df_final):
    df_final.to_csv("products.csv", sep=",")
    
    
    
url = input("Entrez l'URL du site web qui possède Shopify : ")
df_product = get_products(url)
get_csv(df_product)