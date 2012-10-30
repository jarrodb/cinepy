from os import path
from tornado.util import ObjectDict
from libs import dependencies
from models import register_models

settings_ = dict(
    debug = True,

    #instance_ipv4 = '10.77.77.111',
    instance_ipv4 = '127.0.0.1',
    #instance_ipv4 = '192.168.1.165',
    instance_port = 8888,

    cookie_secret = 'set_this_in_settings_prod',
    xsrf_cookies = True,

    static_path = path.join(path.dirname(__file__), "static"),
    template_path = path.join(path.dirname(__file__), "tpl"),

    site_url = 'http://127.0.0.1:8888',
    login_url = '/login',

    mongo_server = 'localhost:27017',
    mongo_dbname = 'cinepy',
    mongo_user = None,
    mongo_pass = None,

    movie_media_path = '/movies',
    series_media_path = '/movies',
    movie_staging_path = '/staging/movies',
    series_staging_path = '/staging/series',
    )

# local overrides untracked by the project
try:
    from settings_prod import settings as settings_prod
    settings_.update(settings_prod)
except ImportError:
    pass

settings = ObjectDict(settings_)

