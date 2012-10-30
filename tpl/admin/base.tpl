{% include "../base/header.tpl" %}
  {% block content %}
      <div class="row">
        <div class="span2">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Movies</li>
              <li class="{% if menu_active == 'addmovie' %}active{%end%}">
                <a href="{{reverse_url('admin-movie-add')}}">
                  Add Movies
                </a>
              </li>
              <li class="nav-header">Series</li>
              <li class="{% if menu_active == 'series' %}active{%end%}">
                <a href="{{reverse_url('admin-series')}}">
                  List Series
                </a>
              </li>
              <li class="{% if menu_active == 'addseries' %}active{%end%}">
                <a href="{{reverse_url('admin-series-add')}}">
                  Add Series
                </a>
              </li>
              <li class="{% if menu_active == 'addepisodes' %}active{%end%}">
                <a href="{{reverse_url('admin-episodes-add')}}">
                  Add Episodes
                </a>
              </li>
              <li class="nav-header">Users</li>
              <li class="{% if menu_active == 'listusers' %}active{%end%}">
                <a href="{{reverse_url('admin-users')}}">List Users</a>
              </li>
              <li class="{% if menu_active == 'adduser' %}active{%end%}">
                <a href="{{reverse_url('admin-user-add')}}">Add Users</a>
              </li>
              <li class="{% if menu_active == 'trackusers' %}active{%end%}">
                <a href="{{reverse_url('admin-user-tracker')}}">Track Users</a>
              </li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span10">
          {% block admin-content %}
          {% end %}
        </div><!--/span-->
      </div>
  {% end %}

{% include "../base/footer.tpl" %}
