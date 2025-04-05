<%def name="link(s)"><a href="https://rtp.trimet.org/rtp/#/nearby/${s.get('lat')},${s.get('lon')}">${s.get('feed_id')} ${s.get('stop_code')}\
%if s.get('stop_id') != s.get('stop_code'):
 (id ${s.get('stop_id')})\
%endif
</a></%def>

<%def name="stop(s, z)">\
${s.get('desc')} ${link(s.get('stops')[0])} and ${link(z)} are ${'%.2f'%(z.get('distance'))} meters apart\
</%def>\
\
<%def name="loopr(n, k=10000)">\
The following are ${n} to ${k} meters apart:
%for s in stops:
%if s.get('distance') >= n and s.get('distance') < k:
${stop(s, s.get('stops')[1])}
%elif len(s.get('stops')) > 2:
%for z in s.get('stops'):
%if z.get('distance') >= n and z.get('distance') < k:
${stop(s, z)}
%endif
%endfor
%endif
%endfor
</%def>\

${loopr(100)}

${loopr(15, 100)}

${loopr(5, 15)}

${loopr(1, 5)}

${loopr(0, 1)}
