from ..__Import import *
from ..Variable import Listener, Poll, Variable
from ._Common._BasicProps import BasicProps


class Label(Gtk.Label, BasicProps):
    def __init__(
        self,
        text="",
        yalign=0.5,
        xalign=0.5,
        angle=0.0,
        maxchars=None,
        attributes=None,
        css=None,
        halign="fill",
        valign="fill",
        hexpand=False,
        vexpand=False,
        visible=True,
        classname="",
    ):
        Gtk.Label.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=None,
            visible=visible,
            classname=classname,
        )
        self.set_text(text)
        self.set_yalign(yalign)
        self.set_xalign(xalign)
        self.set_selectable(False)
        self.set_angle(angle)
        self.set_max_width_chars(maxchars) if maxchars else None

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
                callback = {
                    "text": self.set_text,
                    "yalign": self.set_yalign,
                    "xalign": self.set_xalign,
                    "angle": self.set_angle,
                    "limit": self.set_max_width_chars,
                }.get(key)

                self.bind(value, callback) if callback else None

    def set_text(self, text):
        super().set_text(str(text))
