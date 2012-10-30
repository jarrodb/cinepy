<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Cinepy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Cinepy Family Entertainment">
    <meta name="author" content="">

    <link href="/static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }
        .sidebar-nav {
            padding: 9px 0;
        }
    </style>
    <link href="/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    </script>
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="https://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <link rel="shortcut icon" href="/static/bootstrap/ico/favicon.ico">
    <script src="/static/bootstrap/js/jquery.js"></script>
    {% block header_extra %}
    {% end %}
<body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="#">Cinepy</a>

          {% if current_user %}<!-- Authenticated User -->
          <div class="btn-group pull-right">
            <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
              <i class="icon-user"></i> {{current_user.get('email', 'Error')}}
              <span class="caret"></span>
            </a>
            <ul class="dropdown-menu">
              <li><a href="{{reverse_url('profile')}}">Profile</a></li>
              <li>
                <a href="{{reverse_url('user-edit', current_user._id)}}">
                  Account Settings
                </a>
              </li>
              <li class="divider"></li>
              <li><a href="{{reverse_url('logout')}}">Sign Out</a></li>
            </ul>
          </div>

          {% block privilege-nav %}
          {% if current_user.is_admin %}
          <div class="nav-collapse">
            <ul class="nav pull-right">
              <li class="dropdown">
                <a
                  href="#"
                  class="dropdown-toggle {% if nav_active == 'movies' %}active{%end%}"
                  data-toggle="dropdown"
                  style="color: red;"
                  >
                    Admin <b class="caret"></b>
                  </a>
                <ul class="dropdown-menu">
                  {% block admin-menu %}
                  <!--<li class="divider"></li>
                  <li><a href="#">Separated link</a></li>-->
                  {% end %}
                  <li><a href="{{reverse_url('admin-movie-add')}}">
                    Manage Movies
                  </a></li>
                  <li><a href="{{reverse_url('admin-series')}}">
                    Manage Series
                  </a></li>
                  <li><a href="{{reverse_url('admin-users')}}">
                    Manage Users
                  </a></li>
                </ul>
              </li>
              <li class="divider-vertical"></li>
            </ul>
          </div>
          {% end %}
          {% end %}

          {% else %}
          {% include 'header-loginform.tpl' %}
          {% end %}
          <div class="nav-collapse">
            <ul class="nav">
              <li class="{% if nav_active == 'home' %}active{%end%}">
                <a href="/">Home</a>
              </li>
              {% if current_user %}
              <li class="{% if nav_active == 'movies' %}active{%end%}">
                <a href="{{reverse_url('movies')}}">Movies</a>
              </li>
              {% end %}
            </ul>
            {% if current_user %}
            <form class="navbar-search pull-left" method="GET" action="{{reverse_url('search')}}">
              <input
                name="query"
                type="text"
                class="search-query span3"
                {% if query %}
                value="{{query}}"
                {% else %}
                placeholder="Search Titles or Actors..."
                {% end %}
                >
            </form>
            {% end %}
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
    {% if updated %}
      <div id="update" style="text-align: center;" class="alert alert-success">
        <a class="close" data-dismiss="alert" href="#">×</a>
        <p><strong>Update Successful</strong> {{updated}}</p>
      </div>
      <script type="text/javascript">
        $("#update").alert();
        window.setTimeout(function() { $("#update").alert('close'); }, 2000);
      </script>

    {% end %}
