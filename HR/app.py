from flask import Flask 






def create_app():
    app = Flask(__name__,template_folder='templates')

    app.secret_key = "secret key"
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
