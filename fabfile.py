from fabric import task


PROJ_DIR = '/srv/django_first'
VIRTUALENV_DIR = '/srv/.virtualenvs/django_korka/bin/activate'


@task
def deploy(c):
    c.run('cd {}; git pull'.format(PROJ_DIR))
    c.run('cd {}; source {}; pip install -r requirements.txt'.format(
        PROJ_DIR, VIRTUALENV_DIR
    ))
    c.sudo('supervisorctl restart django_first')
