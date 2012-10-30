import wtforms
from libs.forms.fields import UnicodeField, CSVListField

SERIES_RATINGS = (
    (u'none','None Selected'),
    (u'tv-y','TV-Y'),
    (u'tv-y7','TV-Y7'),
    (u'tv-g','TV-G'),
    (u'tv-pg','TV-PG'),
    (u'tv-14','TV-14'),
    (u'tv-ma','TV-MA'),
    (u'unrated','unrated'),
    )

SERIES_TYPE = (
    (1,'TV Series'),
    (2,'Mini-series'),
    )

class SeriesForm(wtforms.Form):

    title = UnicodeField(
        u'Title',
        [wtforms.validators.length(max=100)],
        description='The title of the series'
        )

    seriestype = wtforms.SelectField(
        u'Series Type',
        choices=SERIES_TYPE,
        coerce=int,
        )

    description = wtforms.TextAreaField(
        u'Description',
        description='A short description for the series',
        )

    date = wtforms.DateField(
        format='%Y-%m-%d',
        description='YYYY-MM-DD - Release Date',
        )

    genres = CSVListField(
        u'Genres',
        description='Comma separated Genres',
        )

    rating = wtforms.SelectField(u'Rating', choices=SERIES_RATINGS)

    actors = CSVListField(
        u'Actors',
        description='Comma separated list of Actors (ex. Name1, Name2, Name3)'
        )

    writers = CSVListField(
        u'Writers',
        description='Comma separated list of Writers'
        )

    poster_url = UnicodeField(
        u'Poster URL',
        [
            wtforms.validators.URL(require_tld=True, message=u'Invalid URL.'),
            wtforms.validators.Optional(),
            ],
        description=u'Enter the URL to a poster image',
        )

class SeasonForm(wtforms.Form):

    description = UnicodeField(
        u'Description',
        description='Summary of the season',
        )

    date = wtforms.DateField(
        format='%Y',
        description='YYYY - Release Year',
        )


class MoviePosterForm(wtforms.Form):
    poster = UnicodeField(
        u'URL Link to Poster Image',
        [
            wtforms.validators.URL(require_tld=True, message=u'Invalid URL.'),
            wtforms.validators.Regexp(r'.*\.(jpg|jpeg|gif|png)$', flags=2, message=u'Invalid input.')
            ],
        description='Please use http://amazon.com/ for artwork',
        )


