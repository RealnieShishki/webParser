from flask import Flask, render_template, request
from hh_api import vac_request
import json

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
    with open('vac.txt', mode='w') as f:
        f.write(f'{vac_form}')
    area_form = request.form['input_area']
    with open('area.txt', mode='w') as f:
        f.write(f'{area_form}')
    return render_template('result.html')

@app.route('/result/')
def result():
    vac_request()
    with open('result.json') as f:
        data = json.load(f)
    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
