%for s in stops:
    %if s.get('distance') > 100:
      ${s}
    %elif len(s.get('stops')) > 2:
      ${s}
    %endif
%endfor
