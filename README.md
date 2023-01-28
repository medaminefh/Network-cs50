# Tweet clone

## The 4th project of the CS50 web programming with python and javascript

### run the program (locally)

```bash
# install dependencies
pip install -r requirements.txt

# make migrations locally(create db & tables)
python3 manage.py makemigrations --settings=project4.settings-dev
python3 manage.py migrate --settings=project4.settings-dev
# sync the db
python3 manage.py migrate --settings=project4.settings-dev --run-syncdb

# run the server
python3 manage.py runserver --settings=project4.settings-dev
```

### Or just

`python3 script dev`

[Video on Youtube](https://www.youtube.com/watch?v=xAGifUpNd9o)
