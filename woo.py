import base64
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

import requests
from woocommerce import API

from config import woo_key, woo_secret

domain = 'cool3dthings.com'

def wp_upload_image(domain, imgPath):
    # imgPath can be local image path or can be url
    url = 'https://'+ domain + '/wp-json/wp/v2/media'
    filename = imgPath.split('/')[-1] if len(imgPath.split('/')[-1])>1 else imgPath.split('\\')[-1]
    extension = imgPath[imgPath.rfind('.')+1 : len(imgPath)]
    if imgPath.find('http') == -1:
        try: data = open(imgPath, 'rb').read()
        except:
            print('image local path not exits')
            return None
    else:
        rs = requests.get(imgPath)
        if rs.status_code == 200:
            data = rs.content
        else:
            print('url get request failed')
            return None
    headers = { "Content-Disposition": f"attachment; filename={filename}" , "Content-Type": str("image/" + extension)}
    rs = requests.post(url, auth=(wp_username, wp_password), headers=headers, data=data)
    print(rs)
    return (rs.json()['source_url'], rs.json()['id'])


filament_attribute_id = 3

categories = {
    23: '3D printed item',
    24: 'display item',
    41: 'laser engraving',
    20: 'Top view', # promoted
    15: 'Uncategorized',
    42: 'Functional item',
}

tags = {
    25: 'dragon',
    27: 'fidget',
    26: 'flexi',
}

wcapi = API(
    url="https://cool3dthings.com",
    consumer_key=woo_key,
    consumer_secret=woo_secret,
    version="wc/v3",
    verify_ssl=False
)


# resp = wcapi.get("products")
# print(resp.status_code)
# print(resp.json())

# print(wcapi.get("products/categories").json())
pp.pprint(wcapi.get("products/tags").json())


# print(wcapi.get("products/attributes").json())

# print(wcapi.get(f"products/attributes/{filament_attribute_id}/terms").json())

'''
# add new product

data = {
    "name": "Ship Your Idea",
    "type": "variable",
    "description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.",
    "short_description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
    "categories": [
        {
            "id": 9
        },
        {
            "id": 14
        }
    ],
    "images": [
        {
            "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_4_front.jpg"
        },
        {
            "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_4_back.jpg"
        },
        {
            "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_3_front.jpg"
        },
        {
            "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_3_back.jpg"
        }
    ],
    "attributes": [
        {
            "id": 6,
            "position": 0,
            "visible": False,
            "variation": True,
            "options": [
                "Black",
                "Green"
            ]
        },
        {
            "name": "Size",
            "position": 0,
            "visible": True,
            "variation": True,
            "options": [
                "S",
                "M"
            ]
        }
    ],
    "default_attributes": [
        {
            "id": 6,
            "option": "Black"
        },
        {
            "name": "Size",
            "option": "S"
        }
    ]
}

resp = wcapi.post("products", data).json()
data = resp.json()

product_id = data['id']


# add variation

data = {
    "regular_price": "9.00",
    "image": {
        "id": 423
    },
    "attributes": [
        {
            "id": 9,
            "option": "Black"
        }
    ]
}

print(wcapi.post(f"products/{product_id}/variations", data).json())



# add new filament color

data = {
    "name": "XXS"
}

print(wcapi.post(f"products/attributes/{filament_attribute_id}/terms", data).json())


# update all filaments to sort by name
data = {
    "create": [
        {
            "name": "XXS"
        },
        {
            "name": "S"
        }
    ],
    "update": [
        {
            "id": 19,
            "menu_order": 6
        }
    ],
    "delete": [
        21,
        20
    ]
}

print(wcapi.post(f"products/attributes/{filament_attribute_id}/terms/batch", data).json())





# create a tag

data = {
    "name": "Leather Shoes"
}

print(wcapi.post("products/tags", data).json())

'''