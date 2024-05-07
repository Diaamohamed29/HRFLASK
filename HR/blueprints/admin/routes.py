from flask import request , render_template , redirect , url_for , Blueprint,session
from HR.db import connection , cursor 
from datetime import datetime , timedelta


admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route('/')
def index():
    return render_template('index.html')