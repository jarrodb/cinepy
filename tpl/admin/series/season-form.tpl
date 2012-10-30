      <form
        id="seasonform"
        {% if not seasonform.errors %}
        style="display: none;"
        {% end %}
        class="well"
        action="{{reverse_url('admin-series-one', series._id)}}"
        method="POST"
        >
        {% raw xsrf_form_html() %}
        <h3><p id="seasonform_number">Season </p></h3>
        {% for field in seasonform %}
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
        <input type="hidden" name="seasonform" value="seasonform">
        <input type="submit" class="btn btn-primary" value="Add Season">
        <input type="button" onClick="cancel_seasonform();" class="btn" value="Cancel">
      </form>
