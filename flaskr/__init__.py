import os
import psycopg2

# from env import * 
DATABASE_URL="postgres://mtlusctw:069PsmDQLgEaXPU1Jb_iI5HjjVNgCcft@surus.db.elephantsql.com/mtlusctw"
from flask import Flask


def create_app(test_config=None):   
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['DATABASE'] = DATABASE_URL
    app.config['SECRET_KEY'] = 'p2@fVP?BxP:Z,[(v'
    # app.config['DATABASE'] = os.environ.get('DATABASE_URL')
    
    
    if test_config is None:        
        app.config.from_pyfile('config.py', silent=True)
    else:       
        app.config.from_mapping(test_config)    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import wiki
    app.register_blueprint(wiki.bp)

    app.add_url_rule('/', endpoint='index')

    UPLOAD_FOLDER = '/workspaces/project-3/project-3/flaskr/static/Uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app
