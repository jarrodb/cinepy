
      <div class="row-fluid">
        {% if not count and rw_movie %}
        <div style="text-align: center;" class="span3">
          <div style="text-align: center;"><h3>Recently Watched</h3><br/></div> 
          <a href="/movie/{{rw_movie._id}}">
            <img height="200" src="{{rw_movie.get_poster_url()}}" alt="">
          </a>
          <div class="">{{rw_movie.title}}</div>
          <div style="margin: 0 auto; width: 80%;" class="progress ">
            <div class="bar" style="width: {{rw_movie.percent}}%;"></div>
          </div>
        </div>
        <div class="span9">
        {% else %}
        <div class="span12">
        {% end %}
        <div style="margin-left: 40px;"><h3>{{genre}} Movies</h3><br/></div>
        <div id="{{genre}}Carousel" class="carousel slide">
          <div class="carousel-inner">
            {% for num, movie_page in enumerate(movies) %}
            <div class="{% if num == 0 %}active {%end%}item">
              <div class="row-fluid">
              <div class="span12">
                {% for movie in movie_page %}
                  <div class=" span3">
                    <a href="/movie/{{movie._id}}">
                      <img height="200" src="{{movie.get_poster_url()}}" alt="">
                    </a>
                    <h5 style="height: 100px;">{{movie.title}}</h5>
                  </div>
                {% end %}
              </div>
              </div>
            </div>
            {% end %}
          </div>
          <a style="margin-left: -1em;" class="carousel-control left" href="#{{genre}}Carousel" data-slide="prev">&lsaquo;</a>
          <a style="margin-right: -1em;" class="carousel-control right" href="#{{genre}}Carousel" data-slide="next">&rsaquo;</a>
        </div>

        </div>
      </div>
      <script type="text/javascript">
        $('#{{genre}}Carousel').carousel({
          interval: 3000
        });
      </script>

