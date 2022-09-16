from sqlite3 import connect
import json


def add_vacancy(cur):

    with open('result.json', mode='r') as f:
        result = json.load(f)

    cur.execute('select * from vacancy where vacancy.vacancy = ?', (result[0]['keywords'],))
    res = cur.fetchone()
    print(res)
    if res:
        if res[2] < result[0]['count']:
            cur.execute('update vacancy set count = ?, up = ?, down = ? where vacancy.id = ?',
                        (result[0]['count'], result[0]['от'], result[0]['до'], res[0]))
            print('Edit')
        else:
            print('Not edit')
    else:
        cur.execute('insert into vacancy values (null, ?, ?, ?, ?)',
                    (result[0]['keywords'], result[0]['count'], result[0]['от'], result[0]['до']))
        print('Done')
    return cur


def add_skills(cur, ):
    with open('result.json', mode='r') as f:
        result = json.load(f)

    for item in result[0]['Требования']:
        res = cur.execute('select * from skills where skills.name = ?', (item['Название'],))
        if not res.fetchone():
            print(item['Название'])
            cur.execute('insert into skills values (null, ?)', (item['Название'],))
    return cur


def add_vs(cur):
    with open('result.json', mode='r') as f:
        result = json.load(f)

    cur.execute('select id, count from vacancy where vacancy.vacancy = ?', (result[0]['keywords'],))
    vacancy_id, vacancy_count = cur.fetchone()
    for item in result[0]['Требования']:
        cur.execute('select id from skills where skills.name = ?', (item['Название'],))
        skill_id = cur.fetchone()[0]
        print(vacancy_id, skill_id)
        cur.execute('select * from vacancy_skills as vs where vs.id_vacancy = ? and vs.id_skill = ?',
                    (vacancy_id, skill_id))
        res = cur.fetchone()
        if not res:
            cur.execute('insert into vacancy_skills values (null, ?, ?, ?, ?)',
                        (vacancy_id, skill_id, item['количество'], item['доля']))
            print('vs done')
        elif vacancy_count < result[0]['count']:
            cur.execute('update vacancy_skills as vs set count = ?, percent = ? where vs.id_vacancy = ? and vs.id_skill = ?',
                        (item['количество'], item['доля'], vacancy_id, skill_id))
            print('vs edit')
        print('vs not edit')
    return cur

def add_area(cur):
    with open('area.txt', encoding='UTF-8') as file:
        area = file.read()

    res = cur.execute('select * from area where area.name = ?', (area,))
    if not res.fetchone():
        cur.execute('insert into area values (null, ?)', (area,))

    return cur





def add_row():

    con = connect('DB.sqlite')
    cur = con.cursor()
    cur = add_vacancy(cur)
    cur = add_skills(cur)
    cur = add_vs(cur)
    cur = add_area(cur)
    con.commit()
    con.close()

