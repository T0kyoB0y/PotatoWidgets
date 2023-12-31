from ..__Import import *
from ._Box import Box


class CenterBox(Box):
    def __init__(
        self,
        start=Gtk.Box(),
        center=Gtk.Box(),
        end=Gtk.Box(),
        orientation="h",
        classname="",
    ):
        Box.__init__(self, orientation=orientation, classname=classname)

        self._start_widget = None
        self._center_widget = None
        self._end_widget = None
        self.set_start_widget(start)
        self.set_center_widget(center)
        self.set_end_widget(end)

    def get_start_widget(self):
        return self._start_widget

    def set_start_widget(self, start):
        if self._start_widget:
            self._start_widget.destroy()

        self._start_widget = start

        if start:
            self.pack_start(start, True, True, 0)

    def get_end_widget(self):
        return self._end_widget

    def set_end_widget(self, end):
        if self._end_widget:
            self._end_widget.destroy()

        self._end_widget = end

        if end:
            self.pack_end(self._end_widget, True, True, 0)

    def get_center_widget(self):
        return self._center_widget

    def set_center_widget(self, center):
        if self._center_widget:
            self._center_widget.destroy()
        self._center_widget = center

        super().set_center_widget(center)
