{% extends "../base/base.tpl" %}
  {% block header_extra %}
  <script type="text/javascript"
    src="/static/bootstrap/js/bootstrap-modal.js">
  </script>
  <script type="text/javascript"
    src="/static/bootstrap/js/bootstrap-transition.js">
  </script>
  {% end %}
  {% block admin-menu %}
    <li>
      <a href="{{reverse_url('user-edit', user._id)}}">Edit User</a>
    </li>
    <li class="divider"></li>
  {% end %}
