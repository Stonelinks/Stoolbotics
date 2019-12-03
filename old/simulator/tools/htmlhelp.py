import help

def tdb(d):
    return '<td><b>' + d + '</b></td>'
def td(d):
    return '<td>' + d + '</td>'

s = '<table><tr><td><h4>Command</h4></td><td><h4>Usage</h4></td><td><h4>Description</h4></td></tr>'
for k, v in sorted(help.d.iteritems()):
  ref = v['reference']
  desc = v['description']
  s += '<tr>'
  s += tdb(k) + tdb(ref.replace('<', '&lt;').replace('>', '&gt;')) + td(desc.replace('<', '&lt;').replace('>', '&gt;'))
  s += '</tr>'
s += '</table>'
print s
