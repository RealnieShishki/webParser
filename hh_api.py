import requests
from pycbrf import ExchangeRates
from areas_request import area_req
import re
from collections import Counter
from json import dump as jdump


def vac_request():
    with open('vac.txt', "r", encoding='UTF-8') as f:
        vacancy = f.read()

    DOMAIN = 'http://api.hh.ru/'
    url_vac = f'{DOMAIN}vacancies'
    rate = ExchangeRates()
    area_vac = area_req()

    params = {'text': vacancy,
          'area': area_vac}

    r = requests.get(url_vac, params=params).json()

    count_pages = r['pages']
    all_count = len(r['items'])
    result = {'keywords': vacancy,
               'count': all_count}
    skills = []
    sal = {'from': [], 'to': [], 'cur': []}

    for page in range(count_pages):
        param = {'text': vacancy,
                  'page': page}
        ress = requests.get(url_vac, params=param).json()
        all_count = len(ress['items'])
        result['count'] += all_count

        for res in ress['items']:
            skill = set()
            res_full = requests.get(res['url']).json()
            pp = res_full['description']
            pp_re = re.findall(r'\n[A-Za-z-?]+', pp)
            its = set(x.strip(' -').lower() for x in pp_re)

            for sk in res_full['key_skills']:
                skills.append(sk['name'].lower())
                skill.add(sk['name'].lower())

            for it in its:
                if not any(it in x for x in skill):
                    skills.append(it)

            if res_full['salary']:
                code = res_full['salary']['currency']
                if rate[code] is None:
                    code = 'RUR'
                k = 1 if code == 'RUR' else float(rate[code].value)
                sal['from'].append(k * res_full['salary']['from'] if res['salary']['from'] else k * res_full['salary']['to'])
                sal['to'].append(k * res_full['salary']['to'] if res['salary']['to'] else k * res_full['salary']['from'])

    sk2 = Counter(skills)
    up = sum(sal['from']) / len(sal['from'])
    down = sum(sal['to']) / len(sal['to'])
    result.update({'от': round(up, 2),
                  'до': round(down, 2)})

    add = []


    for name, count in sk2.most_common(5):
        add.append({'Название': name,
                    'количество': count,
                    'доля': round((count / result['count'])*100, 2)})
    result['Требования'] = add

    with open('result.json', mode='w') as f:
        jdump([result], f)


