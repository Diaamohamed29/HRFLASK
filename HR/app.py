from flask import Flask 
import os 





def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')

    app.secret_key = "secret key"
    
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'HR/static/uploads')  # 'os.getcwd()' gets the current working directory

# Ensure the uploads directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ## register blue print 
    from HR.blueprints.auth.routes import auth
    app.register_blueprint(auth,url_prefix='/')
    from HR.blueprints.user.routes import user
    app.register_blueprint(user,url_prefix='/user')
    from HR.blueprints.admin.routes import admin
    app.register_blueprint(admin,url_prefix='/admin')
    from HR.blueprints.super.routes import super
    app.register_blueprint(super,url_prefix='/super')
    from HR.blueprints.ceo.routes import ceo
    app.register_blueprint(ceo,url_prefix='/ceo')
    return app 
