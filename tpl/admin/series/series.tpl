        <li class="span2">
          <div style="text-align: center;" class="thumbnail">
            <a href="{{reverse_url('admin-series-one',series._id)}}">
              <img height="200" src="{{series.get_poster_url()}}" alt="">
            </a>
            <div style="text-align: left; overflow: hidden; height:80px;" class="caption">
              <h4>{{series.title}}</h4>
              <br/>
              <p>{{series.description}}</p>
            </div>
          </div>
        </li>
