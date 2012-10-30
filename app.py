import tornado.httpserver
import tornado.ioloop
import tornado.web
from mongokit import Connection
from settings import settings, register_models
from routes import routes

settings.connection = Connection(settings.mongo_server)
settings.connection.register(register_models)

if settings.mongo_user:
    # If a user exists, authenticate
    settings.connection[settings.mongo_dbname].authenticate(
        settings.mongo_user,
        settings.mongo_pass)

tornapp = tornado.web.Application(routes, **settings)

