      <!-- Main hero unit for a primary marketing message or call to action -->
      <div style="" class="hero-unit">
        <div class="row">
          <div style="text-align: center;" class="span4">
            <div style="margin: 0 auto;" class="item">
              <a
                style=""
                class="item"
                {% if media.is_movie() %}
                href="{{reverse_url('player')}}?movie_id={%raw media._id%}{%if time%}&time={{time}}{%end%}
                {% end %}
                ">
               <img src="{{media.get_poster_url()}}">
               <span class="play"></span>
              </a>
              {% if media.is_series() %}
               <h2><small>
                 <b>{{media.get_series_display()}}</b>
               </small></h2>
              {% else %}
               {% if time and percent %}
                 <div style="margin: 10px auto; width: 80%;" class="progress ">
                   <div class="bar" style="width: {{percent}}%;"></div>
                 </div>
               {% end %}
              {% end %}
            </div>
            <br/>
            {% if media.get('trailer_id', None) %}
            <a class="btn" data-toggle="modal" href="#trailer">
              Watch Trailer
            </a>
            {% end %}
            {% if current_user.is_atleast('moderator') and media.is_movie() %}
            <a class="btn btn-inverse" href="{{reverse_url('movie-edit', media._id)}}">
              Edit Movie
            </a>
            {% end %}
          </div>
          <div class="span6">
            <h2>{{media.title}}</h2>
            <p>
              {{media.get_date_formatted()}}
              <span style="margin: -5px 15px 0 15px;" class="btn btn-small btn-inverse">
                <b>{{media.rating.upper()}}</b>
              </span>
              {{media.get_length_formatted()}}
            </p>
            <p><small>
              {% for g in media.genres %}
                <b>{{g}}</b> &nbsp
              {%end%}
            </small></p>
            <p>{{media.description}}</p>
            {% if media.actors %}
            <div class="row-fluid">
              <div class="span2"><b>Actors</b></div>
              <div class="span4">
                  {% for actor in media.actors %}{{actor}}<br>{%end %}
              </div>
            </div>
            <br>
            {% end %}
            {% if media.directors %}
            <div class="row-fluid">
              <div class="span2"><b>Directors</b></div>
              <div class="span4">
                  {% for director in media.directors %}{{director}}<br>{%end %}
              </div>
            </div>
            {% end %}
          </div>
        </div>
      </div>

    {% if media.is_movie() %}
    <div class="modal large hide" id="trailer">
      <div style="text-align: center;" class="modal-header">
        <h3>{{media.title}} Trailer</h3>
      </div>
      <div class="modal-body">
        {% if media.get('trailer_id', None) %}
        <iframe type="text/html" width="530" height="331"  src="http://www.youtube.com/embed/{{media.trailer_id}}" frameborder="0">
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
    {% else %}
    {% end %}
