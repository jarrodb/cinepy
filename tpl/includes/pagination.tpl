        <div class="pull-right pagination">
          <ul>
            {% if page.has_previous %}
            <li>
              <a href="?{% if query %}query={{query}}&{%end%}page={{page.previous_page}}">
                Prev
              </a>
            </li>
            <li>
              <a href="?{% if query %}query={{query}}&{%end%}page={{page.previous_page}}">
                {{page.previous_page}}
              </a>
            </li>
            {% end %}
            <li class="active">
              <a href="?{% if query %}query={{query}}&{%end%}page={{page.current_page}}">
                {{page.current_page}}
              </a>
            </li>
            {% if page.has_next %}
            <li>
              <a href="?{% if query %}query={{query}}&{%end%}page={{page.next_page}}">
                {{page.next_page}}
              </a>
            </li>
            <li>
              <a href="?{% if query %}query={{query}}&{%end%}page={{page.next_page}}">
                Next
              </a>
            </li>
            {% end %}
          </ul>
        </div>

