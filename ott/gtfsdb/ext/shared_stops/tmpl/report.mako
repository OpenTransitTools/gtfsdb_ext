${start_html()}
<h2>Found ${len(stops)} places where ${src_feed_id} shares a stop with other regional agency.</h2>
<br/>
${start_table()}
%for s in stops:
${table_row(s)}\
%endfor
${end_table()}
<h4>note these ${src_feed_id} stops appear to be inactive (not in the ${src_feed_id}.gtfs.zip): \
%for k,v in not_active.items():
  ${stop_url(k, v)} \
%endfor
</h4>
<h4>note these agencies are currently unsupported: ${', '.join(str(v) for v in unsupported.values())}</h4>
${end_html()}

<%def name="start_html()">\
<%
import datetime
now=datetime.datetime.now()
%>\
<!DOCTYPE html>
<html>
<head>
  <title>${src_feed_id} shared stops</title>
  <meta content="built ${now}"/>
</head>
<body>
</%def>


<%def name="end_html()">\
<%include file="/scripts.mako"/>
</body>
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
      <th>shared string</th>
    </tr>
  </thead>
  <tbody>
</%def>


<%def name="end_table()">\
  </tbody>
</table>
</%def>


<%def name="link(s)">${"*" if s.get('duplicate') else ""}<a href="https://rtp.trimet.org/rtp/#/nearby/${s.get('lat')},${s.get('lon')}" target="#">${s.get('feed_id')} ${s.get('stop_id')} ${"</a>" if s.get('stop_id')==s.get('stop_code') else " (<i>" + s.get('stop_code') + "</i>)</a>"}</%def>


<%def name="urls(ss)">\
%for i, s in enumerate(ss.get('stops')):
%if i > 0:
${link(s)}${"<B>,</B>&nbsp;" if i+1<len(ss.get('stops')) else ""}\
%endif
%endfor
</%def>


<%def name="table_row(s)">\
    <tr>
      <td>${s.get('desc')}</td>
      <td>${s.get('distance')}</td>
      <td>${link(s.get('stops', [])[0])}</td>
      <td>${urls(s)}</td>
      <td>${shared_stop_url(s.get('shared_id'))}</td>
    </tr>
</%def>


<%def name="stop_url(stop_id, feed_id)"><a href="https://trimet.org/ride/stop.html?stop_id=${stop_id}" target="#">${stop_id}</a> (${feed_id}) </%def>

<%def name="shared_stop_url(shared_id)">\
%if ":" in shared_id:
%for s in shared_id.split(","):
<a href="https://rtp.trimet.org/rtp/#/schedule/${s.split(':',1)[1]}" target="#${shared_id}">${s}</a>, \
%endfor
%endif
</%def>
