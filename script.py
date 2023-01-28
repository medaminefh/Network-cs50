from sys import argv
from os import system

if len(argv) != 1 and argv[1] == 'dev':
    system('pip install -r requirements.txt')
    system('python3 manage.py makemigrations --settings=project4.settings-dev')
    system('python3 manage.py migrate --settings=project4.settings-dev')
    system('python3 manage.py migrate --settings=project4.settings-dev --run-syncdb')
    system('python3 manage.py runserver --settings=project4.settings-dev')
elif len(argv) != 1 and argv[1] == 'test':
    system("python3 manage.py test --settings=project4.settings-dev")
else:
    print("Nooo prod")