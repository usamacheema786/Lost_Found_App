from flask_migrate import Migrate
from run import app,db


migrate =Migrate(app,db)
