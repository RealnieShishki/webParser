from databaseORM import Session, Vacancy, Skills, VacancySkill, Area


def add_vacancy(cur, result):

    res = cur.query(Vacancy).filter_by(vacancy=result['keywords']).first()
    if res:
        if res.count < result['count']:
            res.count = result['count']
            res.up = result['от']
            res.down = result['до']
            print('Edit')
        else:
            print('Not edit')
    else:
        cur.add(Vacancy(vacancy=result['keywords'], count=result['count'], up=result['от'], down=result['до']))
    return cur


def add_skills(cur, result):
    for item in result['Требования']:
        res = cur.query(Skills).filter_by(name=item['Название']).one_or_none()
        if not res:
            cur.add(Skills(name=item['Название']))
        else:
            print('skill not added')
    return cur


def add_vs(cur, result):

    res = cur.query(Vacancy).filter_by(vacancy=result['keywords']).first()
    vacancy_id, vacancy_count = res.id, res.count
    for item in result['Требования']:
        skill_id = cur.query(Skills).filter_by(name=item['Название']).first().id
        res = cur.query(VacancySkill).filter_by(id_vacancy=vacancy_id, id_skill=skill_id).one_or_none()
        if not res:
            cur.add(VacancySkill(id_vacancy=vacancy_id, id_skill=skill_id, count=item['количество'], percent=item['доля']))
        elif vacancy_count < result['count']:
            res.count = item['количество']
            res.percent = item['доля']
            print('vs edit')
        else:
            print('vs not edit')
    return cur

def add_area(cur):
    with open('area.txt', encoding='UTF-8') as file:
        area = file.read()
    areas = cur.query(Area).filter_by(name=area).first()
    if areas == area:
        print('Edit')
    else:
        cur.add(Area(name=area))

    return cur

def add_row(result):

    cur = Session()
    cur = add_vacancy(cur, result)
    cur = add_skills(cur, result)
    cur = add_vs(cur, result)
    cur = add_area(cur)
    cur.commit()
    cur.close()
