import flaskr
import waitress

app=flaskr.create_app()

waitress.serve(app, host='0.0.0.0', port=8080)
