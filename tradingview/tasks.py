from celery import Celery

app = Celery(
    name='tasks',
    broker='db+sqlite:///celery.sqlite',
    backend='db+sqlite:///db.sqlite3')


@app.task
def absoluteSub(a, b):
    return print(abs(a - b))