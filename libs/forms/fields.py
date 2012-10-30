import wtforms

class CSVListField(wtforms.fields.Field):
    widget = wtforms.widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        _u = unicode
        if valuelist:
            self.data = [_u(x.strip()) for x in valuelist[0].split(',') if x]
        else:
            self.data = []


class UnicodeField(wtforms.fields.Field):
    """
    """
    widget = wtforms.widgets.TextInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].decode('utf-8')
        else:
            self.data = u''

    def _value(self):
        return self.data.decode('utf-8') if self.data is not None else u''


class MultiCheckboxField(wtforms.SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = wtforms.widgets.ListWidget(prefix_label=False)
    option_widget = wtforms.widgets.CheckboxInput()

