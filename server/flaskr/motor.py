import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for 
)

motor = Blueprint('motor', __name__)

@motor.route("/move", methods = ["GET"])
def move(): 
	return "Moving..."
