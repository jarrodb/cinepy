      <style>
        .page-direction-left {
            text-decoration: none;
            font-size: 40px;
            margin-right: 10px;
        }
        .page-direction-right {
            text-decoration: none;
            font-size: 40px;
            margin-left: 10px;
        }
      </style>
      <div style="text-align: center;" class="row">
        <div class="span9 btn-toolbar">
          {% if page.has_previous %}
            <a title="first page" class="page-direction-left" href="{{handler.get_args_uri(exclude=['page'])}}page=1">&laquo;</a>
            <a title="page left" class="page-direction-left" href="{{handler.get_args_uri(exclude=['page'])}}page={{page.previous_page}}">&lsaquo;</a>
          {% else %}
          <span class="page-direction-left">&laquo;</span>
          <span class="page-direction-left">
            {% set prev_letter = swbtn %}
            {% if swbtn == '0' %}
              {% set letter = '#' %}
            {% else %}
              {% set letter = swbtn %}
            {% end %}
            {% if len(movie_letters) >= 2 %}
              {% if letter == movie_letters[0] %}
                {% set prev_letter = movie_letters[-1] %}
              {% else %}
                {% set i = movie_letters.index(letter)-1 %}
                {% set prev_letter = movie_letters[i] %}
              {% end %}
            {% end %}
            {% if prev_letter == '#'%}{% set prev_letter = '0' %}{%end%}
            <a title="page left" class="page-direction-left" href="{{handler.get_args_uri(exclude=['page','sw'])}}sw={{prev_letter}}">
              &lsaquo;
            </a>
          </span>
          {% end %}
          <div class="btn-group">
            {% for c in movie_letters %}
              <button
                style="padding: 3px;"
                class="btn {% if c == swbtn or ('0' == swbtn and c == '#') %}active{%end%}"
                >
                <a style="padding: 3px;" href="{{handler.get_args_uri(exclude=['page','sw'])}}sw={% if c == '#' %}0{%else%}{{c}}{%end%}">{{c}}</a>
              </button>
            {% end %}

          </div>

          {% if page.has_next %}
            <a title="page right" class="page-direction-right" href="{{handler.get_args_uri(exclude=['page'])}}page={{page.next_page}}">&rsaquo;</a>
            <a title="last page" class="page-direction-right" href="{{handler.get_args_uri(exclude=['page'])}}page={{page.page_range[-1]}}">&raquo;</a>
          {% else %}
            {% set next_letter = swbtn %}
            {% if swbtn == '0' %}
              {% set letter = '#' %}
            {% else %}
              {% set letter = swbtn %}
            {% end %}
            {% if len(movie_letters) >= 2 %}
              {% if letter == movie_letters[-1] %}
                {% set next_letter = movie_letters[0] %}
              {% else %}
                {% set i = movie_letters.index(letter)+1 %}
                {% set next_letter = movie_letters[i] %}
              {% end %}
            {% end %}
            {% if next_letter == '#'%}{% set next_letter = '0' %}{%end%}
            <span class="page-direction-right">
              <a title="page right" class="page-direction-right" href="{{handler.get_args_uri(exclude=['page','sw'])}}sw={{next_letter}}">
              &rsaquo;
              </a>
            </span>
            <span class="page-direction-right">&raquo;</span>
          {% end %}

        </div>
      </div>
