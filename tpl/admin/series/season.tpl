    <div class="accordion-group">
      <div class="accordion-heading">
        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse{{season_index}}">
          Season {{season_index}}
        </a>
      </div>
      <div
        id="collapse{{season_index}}"
        class="accordion-body collapse {%if season_index == 1%}in{%end%}">
        <div class="accordion-inner">
          <p>Episodes</p>
          {% for e in season.episodes %}
            <p>{{e.title}}</p>
          {% end %}
          <form
            id="season_{{season._id}}"
            class="well"
            action="{{reverse_url('admin-series-one', series._id)}}"
            method="POST"
            >
            {% raw xsrf_form_html() %}

<ul style="list-style-type: none;" id="sortable_{{season_index}}">
  {% for e in episodesform.media %}
  <li style="" class="ui-state-default">
    {% raw e.selected %} {% raw e.title %}
    {% raw e.episode_id %}
  </li>
  {% end %}
</ul>
            <input type="hidden" name="seasonid" value="{{season._id}}">
            <input type="submit" value="add them">
          </form>
        </div>
      </div>
    </div>
