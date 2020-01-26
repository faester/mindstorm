import flaskr
import waitress

app=flaskr.create_app(basedir='/sys/class')


waitress.serve(app, host='0.0.0.0', port=8080)
