      <form
        id="seriesform"
        {% if not seriesform.errors %}
        style="display: none;"
        {% end %}
        class="well"
        action="{{reverse_url('admin-series-one', series._id)}}"
        method="POST"
        >
        {% raw xsrf_form_html() %}
        {% for field in seriesform %}
          {% set kwargs = {'class_':'input-medium'} %}
          {% raw field.label() %}
          {% raw field(**kwargs) %}
          <p class="help-block">
            {% if field.errors %}
              <div style="color: red;">{{', '.join(field.errors)}}</div>
            {% else %}
              <small>{% raw field.description %}</small>
            {% end %}
          </p>
        {% end %}
        <input type="hidden" name="seriesform" value="seriesform">
        <input type="submit" class="btn btn-primary" value="Update Season">
      </form>
