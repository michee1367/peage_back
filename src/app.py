from flask import Flask, request, g, jsonify
from flask_migrate import Migrate
#from routes.metaRecornd import metaRecord
#from routes.record import record
#from routes.province import province
#from routes.territory import territory
#from routes.settings_unit import settings_unit
from routes.model_routes import model_api
from routes.user import users
from routes.auth import auth
#from routes.geom import geom
#from routes.form import form
#from routes.notification import notification
#from routes.settings_lang import settings_lang
from routes.pic import pic_route
from routes.kpi import kpi_route
#from routes.visit import visit
#from routes.doc import doc_route
#from routes.tiles import tiles

#from routes.all import all

#from models.machine import db
from models import db
#from commands.loadData import loadData
#from commands.loadSchema import loadSchema
#from commands.saveDataImport import saveData
from flasgger import Swagger 
import models
from services.auth_service import decode_jwt
#from commands.exportData import exportData
from flask_cors import CORS
from flask_session import Session

from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files

    db.init_app(app)  # Initializing the database
    jwt = JWTManager(app)
    Swagger(app)  # Initialiser Flasgge
    
    app.config['SWAGGER'] = {
        'title': 'Ma Documentation API',
        'uiversion': 3,
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Entrez votre token au format **Bearer &lt;token&gt;**'
            }
        }
    }
    CORS(app,resources={r"/*":{"origins": ["http://127.0.0.1:3000", "http://localhost:3000","https://anser-rdc.netlify.app"]}})
    
    app.config["SECRET_KEY"] = "secret_key"  # Clé secrète pour signer le JWT
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Autoriser le frontend (ex: http://localhost:3000 pour Nuxt) et l'application mobile
    #CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:8000"])

    #CLIENT_ID = "97244403358-qifgtdagq2eopvstnpqhac0dut84uroc.apps.googleusercontent.com"
    JWT_SECRET_KEY = "votre_jwt_secret_key"
    
    #app.config["CLIENT_ID"] = CLIENT_ID  
    app.config["JWT_SECRET_KEY"] = "votre_jwt_secret_key"
    
    return app


app = create_app()  # Creating the app
## middleware user
@app.before_request
def load_user_from_token():
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user, error = decode_jwt(token)
        if error :
            print("###############################[Authorisation:error]###############################################################")
            print(error)
            print("###################################################################################################################")
            #print(error)
        if user:
            g.current_user = user
        else:
            g.current_user = None
    else:
        g.current_user = None

# Registering the blueprint
#app.register_blueprint(metaRecord, url_prefix='/meta-records')
#app.register_blueprint(record, url_prefix='/records')
#app.register_blueprint(province, url_prefix='/records/provinces')
#app.register_blueprint(territory, url_prefix='/records/territories')
app.register_blueprint(model_api, url_prefix='/models')
#app.register_blueprint(geom, url_prefix='/geom')
#app.register_blueprint(notification, url_prefix='/notifications')
#app.register_blueprint(settings_unit, url_prefix='/settings_units')
#app.register_blueprint(settings_lang, url_prefix='/settings_langs')
app.register_blueprint(pic_route, url_prefix='/pics')
app.register_blueprint(kpi_route, url_prefix='/kpis')

#app.register_blueprint(doc_route, url_prefix='/docs')


app.register_blueprint(auth, url_prefix='/')
#app.register_blueprint(all, url_prefix='/')
app.register_blueprint(users, url_prefix='/users')
#app.register_blueprint(visit, url_prefix='/visits')

#app.register_blueprint(form, url_prefix='/forms')
#app.register_blueprint(tiles, url_prefix='/tiles')


#app.register_blueprint(loadData)
#app.register_blueprint(loadSchema)
#app.register_blueprint(exportData)
#app.register_blueprint(saveData)

migrate = Migrate(app, db)  # Initializing the migration


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)