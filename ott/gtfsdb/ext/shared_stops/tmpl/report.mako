<%def name="start_html(src_agency='TRIMET')">\
<html>
<head>
  <title>Shared stops between ${src_agency} and other regional agencies</title>
</head>
<body>
</%def>
<%def name="end_html()">\
</body>
<%include file="/scripts.mako"/>
</html>
</%def>
<%def name="start_table()">\
<table class="sortable demo">
  <thead>
    <tr>
      <th>stop id</th>
      <th>distance (meters)</th>
      <th>source stop</th>
      <th>shared with</th>
    </tr>
  </thead>
  <tbody>
</%def>
<%def name="end_table()">\
  </tbody>
</table>
</%def>
<%def name="link(s)"><a href="https://rtp.trimet.org/rtp/#/nearby/${s.get('lat')},${s.get('lon')}" target="#">${s.get('feed_id')} ${s.get('stop_code')}\
%if s.get('stop_id') != s.get('stop_code'):
 (id ${s.get('stop_id')})\
%endif
</a>
</%def>
<%def name="urls(s)">\
%for i, ss in enumerate(s.get('stops')):
%if i == 0: 
<td>${link(ss)}</td>
%endif
%endfor
<td>
%for i, ss in enumerate(s.get('stops')):
%if i > 0:
${link(ss)}
%endif
%endfor
%if i > 1:
* (${i} stops)
%endif
</td>
</%def>
<%def name="table_row(s)">\
    <tr>
      <td>${s.get('desc')}</td>
      <td>${s.get('distance')}</td>
      ${urls(s)}
    </tr>
</%def>
<%def name="stop_url(stop_id, feed_id)"><a href="https://trimet.org/ride/stop.html?stop_id=${stop_id}" target="#">${stop_id}</a> (${feed_id}) </%def>

${start_html()}
<h2>There are ${len(stops)} shared stops that were found.</h2>
</br>
${start_table()}
%for s in stops:
${table_row(s)}\
%endfor
${end_table()}
<h4>note these agencies are currently unsupported: ${', '.join(str(v) for v in unsupported.values())}</h4>
<h4>note these stops appear to be inactive (not in my GTFS): \
%for k,v in no_stop.items():
  ${stop_url(k, v)} \
%endfor
</h4>
${end_html()}