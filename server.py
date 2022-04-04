from distutils.log import debug
from app.app import setup, main_app


application = setup(main_app)


application.run(host="0.0.0.0", port=5000, debug=True)
