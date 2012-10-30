
<h3><b>Summary</b>{%if season.date%} ({{season.date.year}}){%end%}</h3>
<p>{{season.description}}</p>
<br/>
{% for k, episode in enumerate(season.episodes, 1) %}
<table class="table">
  <tr>
    <td style="width: 20px;"><b>{{k}}</b></td>
    <td style="width: 20px;">
      <a href="/player?episode_id={{episode._id}}">
      <i class="icon-play"></i>
      </a>
    </td>
    <td>
      <h4>{{episode.title}}</h4>
    </td>
  </tr>
</table>
{% end %}
