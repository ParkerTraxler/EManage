from flask import Blueprint

manager_bp = Blueprint('manager', __name__)

from . import dashboard, ferpa, infochange, withdrawal, studentdrop