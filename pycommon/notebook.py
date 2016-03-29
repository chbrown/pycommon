def td(html):
    return '<td>%s</td>' % html

def th(html):
    return '<th>%s</th>' % html

def tr(tds):
    return '<tr>%s</tr>' % ''.join(tds)

def table(trs):
    return '<table>%s</table>' % ''.join(trs)


_escape_html_translations = {
    ord(u'<'): u'&lt;',
    ord(u'>'): u'&gt;',
    ord(u'&'): u'&amp;',
    # ord(u' '): u'&nbsp;',
}
def escape_html(string):
    return string.translate(_escape_html_translations)

# IPython notebook wrappers (display-ables)


class Table(object):
    '''
    rows should be a list of lists/tuples of strings

    E.g.:

        notebook.Table([('a', 'b'), ('c', 'd')])
    '''
    def __init__(self, rows):
        self.rows = rows

    def _repr_html_(self):
        return table(tr(td(cell) for cell in row) for row in self.rows)


class DictTable(object):
    '''
    records should be a list of dicts
    '''
    def __init__(self, records, keys=None, missing='<i style="color: #AAA">NA</i>'):
        self.records = records
        self.keys = keys
        self.missing = missing

    def _repr_html_(self):
        if self.keys is None:
            self.keys = set(key for record in self.records for key in record.keys())
        header_trs = [tr(th(key) for key in self.keys)]
        body_trs = [tr(td(record.get(key, self.missing)) for key in self.keys) for record in self.records]
        return table(header_trs + body_trs)


class String(object):
    '''
    string can be a bytestring or a unicode
    '''
    def __init__(self, string):
        self.string = string

    def _repr_html_(self):
        return escape_html(self.string)


def key_value(key, value):
    return u'<span style="padding-right: 10px"><b>%s</b>&rarr;%s</span>' % (
        escape_html(unicode(key)), escape_html(unicode(value)))

class Dict(object):
    '''
    mapping should be a dict or list of (key, value) pairs

    E.g.:

        notebook.Dict({'A': 1, 'B': '2'})
    '''
    def __init__(self, mapping):
        self.items = mapping.items() if isinstance(mapping, dict) else mapping

    def _repr_html_(self):
        return u'<div>%s</div>' % ' '.join(key_value(key, value) for key, value in self.items)
