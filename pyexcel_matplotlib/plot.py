import matplotlib
from io import BytesIO
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # flake8: noqa


class SimpleLayout:
    def __init__(self, value):
        pass

    def render_sheet(self, sheet,
                     x_in_column=0,
                     y_in_column=1,
                     **keywords):
        image_data = BytesIO()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(sheet.column[x_in_column],
                        sheet.column[y_in_column],
                        label=sheet.name)
        ax.legend(handles=[line])
        self._set_axis_labels(ax, **keywords)
        fig.savefig(image_data, format='svg')
        return image_data.getvalue()

    def render_book(self, book,
                    x_in_column=0,
                    y_in_column=1,
                    **keywords):
        image_data = BytesIO()
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
        fig.savefig(image_data, format='svg')
        return image_data.getvalue()

    def _set_axis_labels(self, axis, title="test", **keywords):
        axis.set_title(title)
        if 'x_title' in keywords:
            axis.set_xlabel(keywords['x_title'])
        if 'y_title' in keywords:
            axis.set_ylabel(keywords['y_title'])
