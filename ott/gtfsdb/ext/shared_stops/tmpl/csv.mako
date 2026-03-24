stop,shared_string,distance
%for s in stops:
%if ":" in s.get('shared_id'):
${shared_stop_rows(s.get('shared_id'), s.get('distance'))}\
%endif
%endfor
\
<%def name="shared_stop_rows(shared_id, distance)">\
%for s in shared_id.split(","):
${s},"${shared_id}",${distance}
%endfor
</%def>