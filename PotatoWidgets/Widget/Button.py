from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Button(Gtk.Button, BasicProps):
    def __init__(
        self,
        children: Union[Gtk.Widget, None],
        onclick: Union[Callable, None] = None,
        onmiddleclick: Union[Callable, None] = None,
        onhover: Union[Callable, None] = None,
        onhoverlost: Union[Callable, None] = None,
        primaryhold: Union[Callable, None] = None,
        primaryrelease: Union[Callable, None] = None,
        secondaryhold: Union[Callable, None] = None,
        secondaryrelease: Union[Callable, None] = None,
        attributes: Callable = lambda self: self,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        css: str = "",
        classname: str = "",
        halign: str = "fill",
        valign: str = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        active: bool = True,
        visible: bool = True,
    ):
        Gtk.Button.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            size=size,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=active,
            visible=visible,
            classname=classname,
        )

        attributes(self) if attributes else None

        if children:
            self.add(children)

        self.dict = {
            "onclick": onclick,
            "onmiddleclick": onmiddleclick,
            "onhover": onhover,
            "onhoverlost": onhoverlost,
            "primaryhold": primaryhold,
            "primaryrelease": primaryrelease,
            "secondaryhold": secondaryhold,
            "secondaryrelease": secondaryrelease,
        }

        self.connect("clicked", self.__click_event_idle) if onclick else None

        self.connect(
            "button-press-event",
            self.__press_event,
        )

        self.connect(
            "button-release-event",
            self.__release_event,
        )

        self.connect(
            "enter-notify-event",
            self.__enter_event,
        )

        self.connect(
            "leave-notify-event",
            self.__leave_event,
        )

    def __clasif_args(self, widget, event, callback: Callable) -> None:
        arg_num = callback.__code__.co_argcount
        arg_tuple = callback.__code__.co_varnames[:arg_num]

        if arg_num == 2:
            callback(widget=widget, event=event)

        elif arg_num == 1:
            if "widget" in arg_tuple and widget:
                callback(widget=widget)
            elif "event" in arg_tuple and event:
                callback(event=event)
            else:
                callback(event)
        else:
            callback()

    def __click_event_idle(self, event):
        callback = self.dict.get("onclick")

        if callback:
            self.__clasif_args(widget=False, event=event, callback=callback)

    def __press_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryhold")
        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryhold")
        elif event.button == Gdk.BUTTON_MIDDLE:
            callback = self.dict.get("onmiddleclick")
        else:
            callback = None

        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

    def __release_event(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            callback = self.dict.get("primaryrelease")

        elif event.button == Gdk.BUTTON_SECONDARY:
            callback = self.dict.get("secondaryrelease")
        else:
            callback = None

        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

    def __enter_event(self, widget, event):
        callback = self.dict.get("onhover")
        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)

    def __leave_event(self, widget, event):
        callback = self.dict.get("onhoverlost")

        if callback:
            self.__clasif_args(widget=widget, event=event, callback=callback)
