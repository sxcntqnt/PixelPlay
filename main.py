from website import create_app
from waitress import serve
from website import db

app = create_app()

app.debug = True

mode = 'dev'


if __name__ == "__main__":
   if mode == "dev":
      app.run(host='0.0.0.0',port=5000, debug=True)
   else:
        with app.app_context():
            app.config['APPLICATION_ROOT'] = '/website'
            serve(app, host='0.0.0.0', port=5000, threads=10)
