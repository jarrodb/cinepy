import wtforms
from libs.forms.fields import UnicodeField


class EpisodeBaseForm(wtforms.Form):
    selected = wtforms.BooleanField()
    title = UnicodeField(
        u'Title',
        [wtforms.validators.length(max=100)],
        description='The title of the Episode'
        )

    description = wtforms.TextAreaField(
        u'Description',
        description='An optional episode description',
        )

class EpisodeForm(EpisodeBaseForm):
    filename = UnicodeField()
    file = UnicodeField()


class SeasonEpisodeForm(EpisodeBaseForm):
    def __init__(self, *args, **kwargs):
        super(SeasonEpisodeForm,self).__init__(*args, **kwargs)
        if not self['episode_id'].data:
            self['episode_id'].data = kwargs.get('_id', None)

    episode_id = wtforms.HiddenField()


class EpisodesImportForm(wtforms.Form):
    """ This is used for adding episodes to the database """
    media = wtforms.FieldList(wtforms.FormField(EpisodeForm))


class EpisodesSeasonForm(wtforms.Form):
    """ This is used for adding episodes to seasons """
    media = wtforms.FieldList(wtforms.FormField(SeasonEpisodeForm))

