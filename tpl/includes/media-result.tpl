        <li class="span3">
          <div style="text-align: center;" class="thumbnail">
           <div style="position: relative;">
            <a href="{{media.get_url()}}">
              <img height="270" src="{{media.get_poster_url()}}">
            </a>
            {% if media.is_movie() %}
            <a
              style="position: absolute; top: 85%; left: 11%; height:32px; width: 32px;"
              href="{{reverse_url('player')}}?movie_id={%raw media._id%}"
              >
              <img src="/static/images/play-over.png">
            </a>
            <a
              style="position: absolute; top: 85%; right: 11%; height:32px; width: 32px;"
              href="#"
              onClick="queue('{{reverse_url('api-queue')}}', '{{media._id}}', 'delete');"
              >
              <img src="/static/images/queue-over.png">
            </a>
            {% end %}
           </div>
            <div style="text-align: left; overflow: hidden; height:100px;" class="caption">
              <h4>{{media.title}}</h4>
              <br/>
              <p>{{media.description}}</p>
            </div>
          </div>
        </li>
