      <!-- Main hero unit for a primary marketing message or call to action -->
      <div style="" class="hero-unit">
        <div class="row">
          <div style="text-align: center;" class="span4">
            <div style="margin: 0 auto;" class="item">
              <a style="" class="item" href="{{reverse_url('player')}}?movie_id={%raw movie._id%}">
               <img src="{{movie.get_poster_url()}}">
               <span class="play"></span>
              </a>
            </div>
            <br/>
            {% if movie.get('trailer_id', None) %}
            <a class="btn" data-toggle="modal" href="#trailer">
              Watch Trailer
            </a>
            {% end %}
            {% if current_user.is_atleast('moderator') %}
            <a class="btn btn-inverse" href="{{reverse_url('movie-edit', movie._id)}}">
              Edit Movie
            </a>
            {% end %}
          </div>
          <div class="span6">
            <h2>{{movie.title}}</h2>
            <p>
              {{movie.get_date_formatted()}}
              <span style="margin: -5px 15px 0 15px;" class="btn btn-small btn-inverse">
                <b>{{movie.rating.upper()}}</b>
              </span>
              {{movie.get_length_formatted()}}
            </p>
            <p><small>
              {% for g in movie.genres %}
                <b>{{g}}</b> &nbsp
              {%end%}
            </small></p>
            <p>{{movie.description}}</p>
            {% if movie.actors %}
            <div class="row-fluid">
              <div class="span2"><b>Actors</b></div>
              <div class="span4">
                  {% for actor in movie.actors %}{{actor}}<br>{%end %}
              </div>
            </div>
            <br>
            {% end %}
            {% if movie.directors %}
            <div class="row-fluid">
              <div class="span2"><b>Directors</b></div>
              <div class="span4">
                  {% for director in movie.directors %}{{director}}<br>{%end %}
              </div>
            </div>
            {% end %}
          </div>
        </div>
      </div>

    <div class="modal large hide" id="trailer">
      <div style="text-align: center;" class="modal-header">
        <h3>{{movie.title}} Trailer</h3>
      </div>
      <div class="modal-body">
        {% if movie.get('trailer_id', None) %}
        <iframe type="text/html" width="530" height="331"  src="http://www.youtube.com/embed/{{movie.trailer_id}}" frameborder="0">
        </iframe>
        {% else %}
        <div style="text-align: center; margin-top: 10px;" class="">
            No trailer information found.
        </div>
        {% end %}
      </div>
    </div>
    <script type="text/javascript">
        $('#myTab a').click(function (e) {
            e.preventDefault();
                $(this).tab('show');
            })
        $('#trailer').modal()
    </script>
