from databaseORM import Session, Vacancy, VacancySkill
from hh_api import vac_request

cur = Session()
result = vac_request()
res = cur.query(Vacancy).filter_by(vacancy=result['keywords']).all()
