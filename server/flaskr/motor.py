import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for 
)

bp = Blueprint('motor', __name__, url_prefix='/motor')

@bp.route("/move", methods = ["GET"])
def move(): 
	return "Moving..."
