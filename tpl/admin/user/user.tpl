        <li class="span2">
          <div class="thumbnail">
            <img src="/static/images/default-profile.jpg">
            <div style="text-align: center;" class="caption">
              <h4 style="height:40px;">
                <a href="{{reverse_url('user', user._id)}}">
                  {{user.name}}
                </a>
              </h4>
              <p>{{user.usertype_display()}}<p>
            </div>
          </div>
        </li>

