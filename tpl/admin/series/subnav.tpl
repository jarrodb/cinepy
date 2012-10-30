   <div style="text-align: right;" class="subnav row">
    <ul class="nav nav-pills pull-right">
      <li class="">
        <a href="#" onClick="setup_seriesform(); return false;">
          <i class="icon-pencil"></i>
          Edit Series
        </a>
      </li>
      {% if series.seriestype == 1 or len(series.seasons) == 0 %}
      <li id="nav-add-season" class="">
        <a href="#" OnClick="setup_seasonform(); return false;">
          <i class="icon-plus"></i>
          Add Season
        </a>
      </li>
      {% end %}
    </ul>
  </div>
