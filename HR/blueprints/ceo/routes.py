from flask import request , render_template , redirect , url_for , Blueprint,session,jsonify,flash
from HR.db import connection , cursor ,connect_to_zkteco
from datetime import datetime , timedelta


ceo = Blueprint("ceo", __name__, template_folder="templates")

