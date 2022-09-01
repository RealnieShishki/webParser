from sqlite3 import connect

cursor = connect('DB.sqlite').cursor()

cursor.executescript('''
    create table vacancy (
    id integer primary key,
    vacancy varchar(50) not null,
    count real,
    up real,
    down real);

    create table skills (
    id integer primary key,
    name varchar(255)
    );

    create table vacancy_skills (
    id integer primary key,
    id_vacancy integer,
    id_skill integer,
    count real,
    percent real,
    foreign key (id_vacancy) references vacancy (id)
    foreign key (id_skill) references skills (id)
    );

    create table area (
    id integer primary key,
    name varchar(50) unique,
    ind integer
    );
''')

cursor.close()
