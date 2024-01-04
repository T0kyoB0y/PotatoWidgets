from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Icon(Gtk.Image, BasicProps):
    def __init__(
        self,
        icon=None,
        size=20,
        attributes=None,
        halign="fill",
        valign="fill",
        visible=True,
        classname="",
    ):
        Gtk.Image.__init__(self)
        BasicProps.__init__(
            self,
            halign=halign,
            valign=valign,
            hexpand=False,
            vexpand=False,
            active=True,
            visible=visible,
            classname=classname,
            size=None,
        )
        self.size = size
        self.icon = icon

        self.__reload_icon()
        attributes(self) if attributes else None

        for key, value in locals().items():
            if key not in [
                "self",
                "halign",
                "valign",
                "hexpand",
                "vexpand",
                "visible",
                "active",
                "visible",
                "classname",
            ] and isinstance(value, (Listener, Poll, Variable)):
                if key == "icon":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_icon(x)),
                    )
                elif key == "size":
                    value.connect(
                        "valuechanged",
                        lambda x: GLib.idle_add(lambda: self.set_size(x)),
                    )

    def __reload_icon(self):
        self.set_from_icon_name(self.icon, 5)
        self.set_pixel_size(self.size)

    def set_icon(self, x):
        self.icon = x
        self.__reload_icon()

    def set_size(self, x):
        self.size = x
        self.__reload_icon()
