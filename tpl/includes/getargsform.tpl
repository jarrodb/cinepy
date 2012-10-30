{% for k in handler.request.arguments %}
<input type="hidden" name="{{k}}" value="{{handler.get_argument(k)}}"/>
{% end %}
