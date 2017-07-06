import os
import sys
import pyexcel as pe
from nose.tools import eq_

PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7
if PY26:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


def test_line_chart():
    title = 'Browser usage evolution (in %)'
    x_labels = map(str, range(2002, 2013))
    data = {
        'Firefox': [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1],
        'Chrome': [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3],  # flake8: noqa
        'IE': [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1],
        'Others': [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5]
    }
    pe.save_as(
        adict=data,
        dest_title=title,
        dest_x_labels=x_labels,
        dest_chart_type='line',
        dest_file_name='line.png',
        dest_no_prefix=True
    )
    _validate_and_remove('line.png')


def test_xy_lines():
    from math import cos
    data = {
        'x = cos(y)': [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)],
        'y = cos(x)': [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)],
        'x = 1':  [(1, -5), (1, 5)],
        'x = -1': [(-1, -5), (-1, 5)],
        'y = 1':  [(-5, 1), (5, 1)],
        'y = -1': [(-5, -1), (5, -1)]
    }
    pe.save_book_as(
        bookdict=data,
        dest_chart_type='xy',
        dest_title='XY Cosinus',
        dest_file_name='xy_cosinus.png',
        dest_no_prefix=True
    )
    _validate_and_remove('xy_cosinus.png')


def test_xy_line():
    from math import cos
    sheet_name = 'x = cos(y)'
    data = [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)]
    pe.save_as(
        array=data,
        sheet_name=sheet_name,
        dest_chart_type='xy',
        dest_title='XY Cosinus',
        dest_file_name='single_xy_cosinus.png',
        dest_no_prefix=True
    )
    _validate_and_remove('single_xy_cosinus.png')


def test_pie():
    title = 'Browser usage in February 2012 (in %)'
    data = OrderedDict()
    data['IE'] = [19.5]
    data['Firefox'] = [36.6]
    data['Chrome'] = [36.3]
    data['Safari'] = [4.5]
    data['Opera'] = [2.3]
    pe.save_as(
        adict=data,
        dest_title=title,
        dest_chart_type='pie',
        dest_file_name='pie.png'
    )
    _validate_and_remove('pie.png')


def _validate_and_remove(file_name):
    from filecmp import cmp
    status = cmp(file_name, _fixture_file(file_name))
    assert status is True
    os.unlink(file_name)


def _get_svg_graph_element(file_name):
    import lxml.etree as etree

    svg = etree.parse(file_name)
    root = svg.getroot()
    g = root.find('.//g', namespaces=root.nsmap)
    xml = etree.tostring(g, pretty_print=True)
    if PY2 is False:
        xml = xml.decode('utf-8')
    return xml


def _fixture_file(file_name):
    return os.path.join("docs", "source", "_static", file_name)
