from flask import Flask, render_template, request
from hh_api import vac_request
from add_row import add_row
from databaseORM import Session, Vacancy, VacancySkill
cur = Session()
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')

@app.route('/form/', methods=['GET'])
def form_get():
    return render_template('form.html')

@app.route('/form/', methods=['POST'])
def form_post():
    vac_form = request.form['input_vacancy']

    area_form = request.form['input_area']
    with open('area.txt', mode='w', encoding='UTF-8') as f:
        f.write(f'{area_form}')
    data = vac_request(vac_form)
    add_row(data)
    res = cur.query(Vacancy).filter_by(vacancy=data['keywords']).first()
    print(res)

    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
