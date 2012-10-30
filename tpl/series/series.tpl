
<div class="">
  {% if media.is_tvseries() %}

  <ul class="nav nav-tabs" id="myTab">
    {% for i in xrange(1, len(media.seasons)+1) %}
      <li {% if i == 1 %}class="active"{%end%}>
        <a href="#season_{{i}}" data-toggle="tab" >
          Season {{i}}
        </a>
      </li>
    {% end %}
  </ul>

  <div class="tab-content">
    {% for i, season in enumerate(media.seasons, 1) %}
      <div class="tab-pane {% if i == 1%}active{% end%}" id="season_{{i}}">
        {% include 'season.tpl' %}
      </div>
    {% end %}
  </div>

  <script>
    $(function () {
      $('#myTab a:last').tab('show');
    })
  </script>

  {% elif media.is_miniseries %}
    {% comment One Season %}
    {% set season = media.seasons[0] %}
    {% include 'season.tpl' %}
  {% end %}

</div>
