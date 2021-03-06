import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY', default='dev')
    STORAGE_MODE = 'json'  # json ou sqlite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = r'sqlite:///d:\python\examples\SampleFlask\app\db\clients.db'
    #Heroku
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '/app/db/clients.db')