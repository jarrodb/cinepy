from tornado import escape
from tornado import web
from mongokit import ObjectId
from libs.torn.base import ViewHandler, SeriesBaseHandler
from libs.torn.forms import TornadoMultiDict
from libs.torn.decorators import user_passes
from libs.models.pager import Paginator
from libs.series import MediaStager, MediaFile
from forms.series import SeriesForm, SeasonForm
from forms.episode import EpisodesImportForm,EpisodesSeasonForm
from settings import settings
import os
import re


class EpisodeHandler(SeriesBaseHandler):
    tpl = 'admin/episodes/episodes.html'

    RESULTS_PER_PAGE = 50

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        pager = None
        page = int(self.get_argument('page', 1))
        episodes = MediaStager(settings.series_staging_path)
        episodes.limit(self.RESULTS_PER_PAGE)
        if page > 1:
            episodes.skip(self.RESULTS_PER_PAGE * (page-1))

        pager = Paginator(episodes, page, self.RESULTS_PER_PAGE)

        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'addepisodes',
            'episodesform': EpisodesImportForm(obj=episodes),
            'page': pager,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def post(self):
        episodesform = EpisodesImportForm(
            TornadoMultiDict(self.request.arguments)
            )
        count = 0
        try:
            episode_add_list = []
            for eform in episodesform.media:
                if eform.selected.data:
                    form = eform.form
                    self._validate_or_exception(form)
                    episode_add_list.append(form)
                    count += 1

            for eform in episode_add_list:
                self._add_episode_from_form(eform)

        except Exception, e:
            class Page: pass
            page = Page()
            page.is_paginated = False

            self.render(self.tpl, **{
                'error': e,
                'nav_active': 'admin',
                'menu_active': 'addepisodes',
                'episodesform': episodesform,
                'page': page,
                })
        else:
            if count:
                self.set_secure_cookie('updated', 'Episodes have been imported')
            self.redirect(self.reverse_url('admin-episodes-add'))

    def _add_episode_from_form(self, form):
        try:
            episode = self.db.Episode()

            # Create a MovieFile object for moving
            mfile = MediaFile(form.filename.data)

            # Populate empty movie object with formdata
            self._update_doc_from_form(episode, form)

            # Move the file to the production episode path
            filename = mfile.move_file_to(settings.series_media_path)

            # Assign new filename and save the episode to the database
            episode.filename = filename
            episode.save()

        except Exception, e:
            # If something failed, delete the DB entry.
            if episode.has_key('_id'):
                episode.delete()

            # Pass the exception back up the chain
            raise



class AddHandler(SeriesBaseHandler):
    tpl = 'admin/series/add.html'

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'addseries',
            'seriesform': SeriesForm(),
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def post(self):
        seriesform = SeriesForm(TornadoMultiDict(self.request.arguments))
        try:
            self._validate_or_exception(seriesform)
            _series = self.db.Series()
            self._update_doc_from_form(_series, seriesform)
            if seriesform.poster_url.data:
                poster_url = seriesform.poster_url.data
                poster_fn = self._get_new_poster_file(_series.title)
                self._download_poster_image(poster_url, poster_fn)
                _series.poster = poster_fn
            _series.save()
        except Exception, e:
            self.render(self.tpl, **{
                'error': e,
                'nav_active': 'admin',
                'menu_active': 'addseries',
                'seriesform': seriesform,
                })
        else:
            self.set_secure_cookie('updated', 'Series as been added!')
            self.redirect(self.reverse_url('admin-series-one', _series._id))


class OneSeriesHandler(SeriesBaseHandler):
    tpl = 'admin/series/oneseries.html'

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self, series_id):
        series = self._get_series(series_id)
        episodes = self.db.Episode.find({'series':None}) # unassigned

        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'series',
            'series': series,
            'seriesform': SeriesForm(obj=series),
            'seasonform': SeasonForm(),
            'episodesform': EpisodesSeasonForm(**{'media':episodes}),
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def post(self, series_id):
        series = self._get_series(series_id)
        season = self.db.Season()
        seasonform = SeasonForm()
        seriesform = SeriesForm(TornadoMultiDict(self.request.arguments))
        #episodes = self.db.Episode.find({'series':None})
        episodesform = None
        updated = 'Thanks for posting'
        try:
            torn_post_args = TornadoMultiDict(self.request.arguments)
            if self.get_argument('seasonform', None):
                seasonform = SeasonForm(torn_post_args)
                self._validate_or_exception(seasonform)
                self._update_doc_from_form(season, seasonform)
                season.save()
                series.seasons.append(season)
                series.save()
                updated = 'Season has been added'
            elif self.get_argument('seriesform', None):
                self._validate_or_exception(seriesform)
                self._update_doc_from_form(series, seriesform)
                if seriesform.poster_url.data:
                    poster_url = seriesform.poster_url.data
                    poster_fn = self._get_new_poster_file(series.title)
                    self._download_poster_image(poster_url, poster_fn)
                    series.poster = poster_fn
                series.save()
                updated = 'Series has been updated'
            elif self.get_argument('seasonid', None):
                seasonid = self.get_argument('seasonid')
                # Adding Episodes to a season
                episodesform = EpisodesSeasonForm(torn_post_args)
                count = 0
                episode_add_list = []
                for eform in episodesform.media:
                    if eform.selected.data:
                        form = eform.form
                        self._validate_or_exception(form)
                        episode_add_list.append(form)
                        count += 1

                season = self.db.Season.one({'_id': ObjectId(seasonid)})

                for eform in episode_add_list:
                    eid = eform.episode_id.data
                    e = self.db.Episode.one({'_id': ObjectId(eid)})
                    self._update_doc_from_form(e, eform)
                    e.series = ObjectId(series_id)
                    e.save()
                    season.episodes.append(e)
                    season.save()

        except Exception, e:
            if season.has_key('_id'):
                season.delete()

            self.render(self.tpl, **{
                'error': e,
                'nav_active': 'admin',
                'menu_active': 'series',
                'series': series,
                'episodes': episodes,
                'episodesform': episodesform,
                'seriesform': seriesform,
                'seasonform': seasonform,
                })
        else:
            self.set_secure_cookie('updated', updated)
            self.redirect(self.reverse_url('admin-series-one', series_id))


class SeriesHandler(SeriesBaseHandler):
    tpl = 'admin/series/series.html'

    RESULTS_PER_PAGE = 9

    @web.authenticated
    @user_passes(lambda user: user.is_admin)
    def get(self):
        page = self.get_argument('page', 1)
        query = self.get_argument('query', None)
        results = self._search_series(query)
        page = Paginator(results, page, self.RESULTS_PER_PAGE)

        self.render(self.tpl, **{
            'nav_active': 'admin',
            'menu_active': 'series',
            'page': page,
            'query': query,
            'updated': self.get_and_clear_secure_cookie('updated'),
            })

    def _search_series(self, query):
        _q = {'mediatype': 2}
        if query:
            _q['title'] = re.compile(query, re.IGNORECASE)
        return self.db.Series.find(_q)

