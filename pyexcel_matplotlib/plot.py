"""
    pyexcel_matplotlib
    ~~~~~~~~~~~~~~~~~~~

    chart drawing plugin for pyexcel

    :copyright: (c) 2016-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for further details
"""
import matplotlib
from io import BytesIO
matplotlib.use('Agg')

import matplotlib.pyplot as plt  # flake8: noqa

from lml.plugin import PluginInfo, PluginManager

from pyexcel.renderer import BinaryRenderer


DEFAULT_TITLE = 'pyexcel chart rendered by pygal'
KEYWORD_CHART_TYPE = 'chart_type'
DEFAULT_CHART_TYPE = 'bar'


class Plotter(object):
    def __init__(self, chart_type, file_type, image_stream):
        self._chart_type = chart_type
        self._file_type = file_type
        self._image_stream = image_stream


@PluginInfo('plot', tags=['pie'])
class Pie(Plotter):
    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     label_y_in_row=0, **keywords):
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(label_y_in_row)
        the_dict = sheet.to_dict()
        fig, ax = plt.subplots()
        ax.pie(the_dict.values(), labels=the_dict.keys(), **keywords)
        ax.axis('equal')
        ax.set_title(title)
        fig.savefig(self._image_stream, format=self._file_type)


@PluginInfo('plot', tags=['xy'])
class XY(Plotter):
    def render_sheet(self, sheet,
                     x_in_column=0,
                     y_in_column=1,
                     **keywords):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(sheet.column[x_in_column],
                        sheet.column[y_in_column],
                        label=sheet.name)
        ax.legend(handles=[line])
        self._set_axis_labels(ax, **keywords)
        fig.savefig(self._image_stream, format=self._file_type)

    def render_book(self, book,
                    x_in_column=0,
                    y_in_column=1,
                    **keywords):
        from pyexcel.book import to_book
        line_handles = []
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for sheet in to_book(book):
            line_handle, = ax.plot(
                sheet.column[x_in_column],
                sheet.column[y_in_column],
                label=sheet.name)
            line_handles.append(line_handle)
        ax.legend(handles=line_handles)
        self._set_axis_labels(ax, **keywords)
        fig.savefig(self._image_stream, format=self._file_type)

    def _set_axis_labels(self, axis, title="test", **keywords):
        axis.set_title(title)
        if 'x_title' in keywords:
            axis.set_xlabel(keywords['x_title'])
        if 'y_title' in keywords:
            axis.set_ylabel(keywords['y_title'])


@PluginInfo('plot',
            tags=['line'])
class Line(Plotter):
    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     label_x_in_column=0, label_y_in_row=0,
                     **keywords):
        params = {}
        self.params = {}
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(label_y_in_row)
        if len(sheet.rownames) == 0:
            sheet.name_rows_by_column(label_x_in_column)
        params['x_labels'] = sheet.rownames
        the_dict = sheet.to_dict()
        fig, ax = plt.subplots()
        for key in the_dict:
            data_array = [value for value in the_dict[key] if value != '']
            ax.plot(range(len(data_array)), data_array, label=key)
        ax.set_title(title)
        fig.savefig(self._image_stream, format=self._file_type)


class PlotManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self, 'plot')

    def get_a_plugin(self, key, file_type, image_stream,
                     **keywords):
        self._logger.debug("get a plugin called")
        plugin = self.load_me_now(key)
        return plugin(key, file_type, image_stream)

    def raise_exception(self, key):
        raise Exception("No support for " + key)


MANAGER = PlotManager()


class MatPlotter(BinaryRenderer):
    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     chart_type=DEFAULT_CHART_TYPE,
                     **keywords):
        plotter = MANAGER.get_a_plugin(chart_type,
                                       file_type=self._file_type,
                                       image_stream=self._stream)
        plotter.render_sheet(
            sheet, title=title, **keywords)

    def render_book(self, book, title=DEFAULT_TITLE,
                    chart_type=DEFAULT_CHART_TYPE,
                    **keywords):
        plotter = MANAGER.get_a_plugin(chart_type,
                                       file_type=self._file_type,
                                       image_stream=self._stream)
        plotter.render_book(
            book, title=title, **keywords)

