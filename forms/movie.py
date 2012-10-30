import wtforms
from libs.forms.fields import UnicodeField, CSVListField

# If you update this list, update the template
MOVIE_GENRES = (
    ('action','Action'),
    ('adventure','Adventure'),
    ('animated','Animated'),
    ('classic','Classic'),
    ('comedy','Comedy'),
    ('crime','Crime'),
    ('family','Family'),
    ('fantasy','Fantasy'),
    ('horror','Horror'),
    ('love','Love'),
    ('musical','Musical'),
    ('science fiction','Science Fiction'),
    ('thriller','Thriller'),
    ('western','Western'),
    )

MOVIE_RATINGS = (
    (u'none','None Selected'),
    (u'g','G'),
    (u'pg','PG'),
    (u'pg-13','PG-13'),
    (u'r','R'),
    (u'nc-17','NC-17'),
    (u'unrated','Unrated'),
    )



class MovieSearchForm(wtforms.Form):
    title = wtforms.TextField(
        u'Title',
        [wtforms.validators.length(max=50)]
        )

    adname = wtforms.TextField(
        u'Actor or Director Name',
        [wtforms.validators.length(max=50)]
        )

    genres = wtforms.SelectMultipleField(
        u'Genre',
        choices=MOVIE_GENRES,
        )

    rating = wtforms.SelectMultipleField(
        u'Ratings',
        choices=MOVIE_RATINGS[1:],
        )

    search = wtforms.HiddenField(
        u'search',
        )


class MovieForm(wtforms.Form):

    title = UnicodeField(
        u'Title',
        [wtforms.validators.length(max=100)],
        description='The title of the movie'
        )

    sort_title = UnicodeField(
        u'Sort Title',
        [wtforms.validators.length(max=100)],
        description='This will influence how the movie is sorted. (optional)'
        )

    description = wtforms.TextAreaField(
        u'Description',
        description='A short description for the movie',
        )

    date = wtforms.DateField(
        format='%Y-%m-%d',
        description='YYYY-MM-DD',
        )

    length = UnicodeField(
        u'Length',
        [wtforms.validators.length(max=10)],
        description="HH:MM:SS",
        )

    genres = CSVListField(
        u'Genres',
        description='Comma separated Genres',
        )

    rating = wtforms.SelectField(u'Rating', choices=MOVIE_RATINGS)

    actors = CSVListField(
        u'Actors',
        description='Comma separated list of Actors (ex. Name1, Name2, Name3)'
        )
    directors = CSVListField(
        u'Directors',
        description='Comma separated list of Directors'
        )

    trailer_id = UnicodeField(
        u'Trailer ID',
        [wtforms.validators.length(max=20)],
        description="http://www.youtube.com/watch?v=<b>sftuxbvGwiU</b>",
        )

    enabled = wtforms.BooleanField(
        u'Enabled',
        default=True,
        )

    poster_url = wtforms.HiddenField(
        u'Poster URL',
        [
            wtforms.validators.URL(require_tld=True, message=u'Invalid URL.'),
            wtforms.validators.Optional(),
            ]
        )

#    sort_title = UnicodeField(
#        u'Sort Title',
#        [wtforms.validators.length(max=100)],
#        description='Used for sorting purposes.'
#        )


class MovieImportForm(MovieForm):
    selected = wtforms.BooleanField()
    filename = UnicodeField()
    file = UnicodeField()


class MoviesImportForm(wtforms.Form):
    movies = wtforms.FieldList(wtforms.FormField(MovieImportForm))


class MoviePosterForm(wtforms.Form):
    poster = UnicodeField(
        u'URL Link to Poster Image',
        [
            wtforms.validators.URL(require_tld=True, message=u'Invalid URL.'),
            wtforms.validators.Regexp(r'.*\.(jpg|jpeg|gif|png)$', flags=2, message=u'Invalid input.')
            ],
        description='Please use http://amazon.com/ for artwork',
        )


