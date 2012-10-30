      <!-- -->
      <div>
        <a class="btn btn-small" href="{{movie.get_url()}}"><i class="icon-arrow-left"></i> Back to movie</a>
      </div>
      <div class="row">
        <div class="span4">
          <p><img id="poster_url" src="{{movie.get_poster_url()}}"></p>
          <form id="poster" method="POST" action="{{reverse_url('movie-edit', movie._id)}}">
            {% raw xsrf_form_html() %}
            <fieldset>
              <div class="control-group">
                {% raw posterform.poster.label() %}
                <div class="controls">
                {% raw posterform.poster() %}
                <p class="help-block">
                  {% if posterform.poster.errors %}
                    <div class="error">
                      {{posterform.poster.errors}}
                    </div>
                  {% else %}
                    {% raw posterform.poster.description %}
                  {% end %}
                </p>
                </div>
              <input type="hidden" name="posterform" value="true">
              <button type="submit" class="btn btn-primary">Update Poster</button>
              </div>
            </fieldset>
          </form>
        </div>
        <div class="span8">
          {% if error %}
            <div style="text-align: center;" class="alert alert-error">
              {{error}}
            </div>
          {% end %}
          <form id="movie_form" class="well form-horizontal" method="POST" action="{{reverse_url('movie-edit', movie._id)}}">
          {% raw xsrf_form_html() %}
            <fieldset>
              {% for field in movieform %}
              {% if field.type == 'HiddenField' %}
                {% raw field %}
                {% if field.errors %}
                  <p class="error">{{field.errors}}</p>
                {% end %}
              {% else %}
                {% set kwargs = {'class_':'input-xlarge'} %}
                {% if field.name == 'genres' %}
                  {% set kwargs = {'class_':'input-xlarge','data-provide':'typeahead', 'data-mode':'multiple', 'data-items':'4', 'data-source':'["Action","Adventure","Animated","Classic","Comedy","Crime","Family","Fantasty","Horror","Love","Musical","Science Fiction","Thriller","Western"]'} %}
                {% elif field.name == 'description' %}
                  {% set kwargs['rows'] = 8 %}
                {% end %}

              <div class="control-group">
                {% raw field.label(class_='control-label') %}
                <div class="controls">
                  {% raw field(**kwargs) %}
                  <p class="help-block">
                    {% if field.errors %}
                    <div class="error">{{field.errors}}</div>
                    {% else %}
                    {% raw field.description %}
                    {% end %}
                  </p>
                </div>
              </div>
              {% end %}
              {% end %}

              <div class="form-actions">
                <input type="hidden" name="movieform" value="true">
                <button type="submit" class="btn btn-primary">Update Data</button>
                <input type="button" class="btn" value="Import Data" onClick="meta_data_for_title('movie_form', '{% raw movie.title.replace("'","\\'") %}');">
              </div>
            </fieldset>
          </form>
        </div>
      </div>

      <script type="text/javascript">
        //$('.typeahead').typeahead({
        $('#genres').typeahead()
        $('#dp').datepicker();
      </script>

      <!-- -->
