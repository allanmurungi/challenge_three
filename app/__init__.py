from flask import Flask

app=Flask(__name__);

from app import routes



from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'mga'

jwt = JWTManager(app)




app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']




