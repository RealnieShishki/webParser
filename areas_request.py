import requests

def area_req():
    DOMAIN = 'http://api.hh.ru/'
    country_url = f'{DOMAIN}areas/'
    with open('area.txt', 'r', encoding='UTF-8') as f:
        area = f.read()
    if area.islower:
        area = area.capitalize()
    result = requests.get(country_url).json()
    area_id = []
    for i in result:
        areas = i.get('areas')
        for j in areas:
            areas = j.get('areas')
            if j.get('name') == area:
                area_id.append(j.get('id'))
            else:
                for k in areas:
                    if k.get('name') == area:
                        area_id.append(k.get('id'))

    return area_id


