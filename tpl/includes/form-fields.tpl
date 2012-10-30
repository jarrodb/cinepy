          {% for field in form %}
            {% try %}
              {% if field.name in formdata %}
                {% set kwargs = formdata[field.name] %}
              {% else %}
                {% set kwargs = {'class_':'input-xlarge'} %}
              {% end %}
            {% except %}
                {% set kwargs = {'class_':'input-xlarge'} %}
            {% end %}
            {% if field.type == 'HiddenField' %}
              {% raw field %}
            {% else %}
            <div class="control-group">
              {% raw field.label(class_='control-label') %}
              <div class="controls">
                {% raw field(**kwargs) %}
                <p class="help-block">
                {% if field.errors %}
                <div style="color: red;">{{', '.join(field.errors)}}</div>
                {% else %}
                {% raw field.description %}
                {% end %}
                </p>
              </div>
            </div>
            {% end %}
          {% end %}
