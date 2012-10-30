# URL Routes
from tornado.web import URLSpec #, StaticFileHandler
from libs.torn.handler import StaticFileHandler
from settings import settings
import views
import api

routes = [
    URLSpec(r"/", views.index.IndexHandler, name="index"),
    # User
    URLSpec(r"/user", views.user.UserHandler, name="profile"),
    URLSpec(r"/user/([a-zA-Z0-9]+)", views.user.UserHandler, name="user"),
    URLSpec(
        r"/user/([a-zA-Z0-9]+)/edit",
        views.user.EditHandler,
        name="user-edit"
        ),
    URLSpec(r"/queue", views.user.QueueHandler, name="queue"),
    URLSpec(
        r"/user/([a-zA-Z0-9]+)/queue",
        views.user.QueueHandler,
        name="user-queue"
        ),
    # Movie
    URLSpec(r"/movie/([a-zA-Z0-9]+)", views.movie.MovieHandler, name="movie"),
    URLSpec(
        r"/movie/([a-zA-Z0-9]+)/edit",
        views.movie.MovieEditHandler,
        name="movie-edit"
        ),
    URLSpec(r"/movies", views.movie.MoviesHandler, name="movies"),
    # Series
    URLSpec(r"/series/([a-zA-Z0-9]+)", views.series.SeriesHandler, name="series"),
    # Player
    URLSpec(r"/player", views.player.PlayerHandler, name="player"),

    # Search
    URLSpec(r"/search", views.search.SearchHandler, name="search"),
    # Recent
    URLSpec(r"/recent", views.recent.RecentHandler, name="recent"),
    # Auth
    URLSpec(r"/login", views.auth.LoginHandler, name="login"),
    URLSpec(r"/logout", views.auth.LogoutHandler, name="logout"),
    ]

# API
routes.extend([
    URLSpec(r"/api/movie/meta", api.movie.MetaHandler, name="api-movie-meta"),
    URLSpec(r"/api/movie/time", api.movie.TimeHandler, name="api-movie-time"),
    URLSpec(r"/api/queue", api.queue.QueueHandler, name="api-queue"),
    ])

# Admin - Move?
routes.extend([
    URLSpec(r"/admin/user", views.admin.user.UsersHandler, name="admin-users"),
    URLSpec(
        r"/admin/user/add",
        views.admin.user.AddHandler,
        name="admin-user-add"
        ),
    URLSpec(
        r"/admin/tracker",
        views.admin.tracker.TrackerHandler,
        name="admin-user-tracker"
        ),
    URLSpec(
        r"/admin/movie/add",
        views.admin.movie.AddHandler,
        name="admin-movie-add"
        ),
    URLSpec(
        r"/admin/series",
        views.admin.series.SeriesHandler,
        name="admin-series"
        ),
    URLSpec(
        r"/admin/series/one/([a-zA-Z0-9]+)",
        views.admin.series.OneSeriesHandler,
        name="admin-series-one"
        ),
    URLSpec(
        r"/admin/series/add",
        views.admin.series.AddHandler,
        name="admin-series-add"
        ),
    URLSpec(
        r"/admin/episodes",
        views.admin.series.EpisodeHandler,
        name="admin-episodes-add"
        ),
    ])

if settings.debug:
# for development only
    routes.append(
        (r"/static/(.*)", StaticFileHandler, dict(path=settings.static_path))
    )
    routes.append(
        (r"/media/movies/(.*)", StaticFileHandler, dict(path="/Users/jarrod/Movies"))
    )
