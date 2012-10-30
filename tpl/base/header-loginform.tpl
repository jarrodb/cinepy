          <div class="pull-right">
            <!-- The drop down menu -->
            <ul class="nav pull-right">
              <li class="divider-vertical"></li>
              <li class="dropdown {{ 'open' if 'error_msg' in globals() else ''}}">
                <a class="dropdown-toggle" href="#" data-toggle="dropdown">Login<strong class="caret"></strong></a>
                <div class="dropdown-menu" style="padding: 15px; padding-bottom: 0px;">
            <!-- Login Form -->
            <form action="{{reverse_url('login')}}" method="post" accept-charset="UTF-8">
            {% raw xsrf_form_html() %}
              <input id="user_username" style="margin-bottom: 15px;" type="text" name="username" size="30" placeholder="Username" />
              <input id="user_password" style="margin-bottom: 15px;" type="password" name="password" size="30" placeholder="Password" />
              <!--
              <input id="user_remember_me" style="float: left; margin-right: 10px;" type="checkbox" name="user[remember_me]" value="1" />
              <label class="string optional" for="user_remember_me"> Remember me</label>-->
              {% try %}
                {% if error_msg %}
              <div class="alert alert-error">{{error_msg}}</div>
                {% end %}
              {% except %}
              {% end %}
             <input class="btn btn-primary" style="clear: left; width: 100%; height: 32px; font-size: 13px;" type="submit" name="commit" value="Sign In" />
            </form>
            <!-- End Login Form -->
                </div>
              </li>
            </ul>
          </div>
          <script type="text/javascript">
            $(function() {
              // Setup drop down menu
              $('.dropdown-toggle').dropdown();
              // Fix input element click problem
              $('.dropdown input, .dropdown label').click(function(e) {
                e.stopPropagation();
              });
            });
          </script>
