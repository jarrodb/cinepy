?{% for k in handler.request.arguments %}{{k}}={{handler.get_argument(k)}}&{%end%}
