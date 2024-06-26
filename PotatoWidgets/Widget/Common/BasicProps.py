from ...Imports import *
from ...Methods import get_screen_size, parse_screen_size
from ...Variable import Listener, Poll, Variable


class BasicProps(Gtk.Widget):
    def __init__(
        self,
        halign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        valign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        hexpand: bool = False,
        vexpand: bool = False,
        classname: str = "",
        # tooltip,
        css: str = "",
        visible: bool = True,
        active: bool = True,
        size: Union[int, str, List[Union[int, str]], List[int]] = 0,
        attributes: Callable = lambda self: self,
    ) -> None:
        Gtk.Widget.__init__(self)
        self._default_classnames = self.get_style_context().list_classes()
        self.set_hexpand(hexpand)
        self.set_vexpand(vexpand)
        self.set_halign(halign)
        self.set_valign(valign)
        self.set_visible(visible)
        self.set_active(active)
        self.set_size(size) if size else None
        self.set_classname(classname)
        self._rand_classname = ""

        self.set_css(css) if css else None

        for key, value in locals().items():
            callback = {
                "halign": self.set_halign,
                "valign": self.set_valign,
                "hexpand": self.set_hexpand,
                "vexpand": self.set_vexpand,
                "active": self.set_sensitive,
                "visible": self.set_visible,
                "size": self.set_size,
                "classname": self.set_classname,
            }.get(key)
            if callback:
                if isinstance(value, (Listener, Poll, Variable)):
                    self.bind(value, callback)

        attributes(self)

    def set_size(self, size: Union[int, str, List[Union[int, str]], List[int]]) -> None:
        if size is not None:
            if isinstance(size, (int, str)):
                size = [size, size]
            elif isinstance(size, (list)):
                if len(size) == 1:
                    size = [size[0], size[0]]
                elif len(size) >= 2:
                    size = size[:2]

            width, height = get_screen_size()
            _width = parse_screen_size(size[0], width)
            _height = parse_screen_size(size[1], height)

            self.set_size_request(_width, _height)

    def set_halign(self, align: Union[str, Gtk.Align] = "fill") -> None:

        if isinstance(align, (str)):
            _alignment = {
                "fill": Gtk.Align.FILL,
                "start": Gtk.Align.START,
                "end": Gtk.Align.END,
                "center": Gtk.Align.CENTER,
                "baseline": Gtk.Align.BASELINE,
            }.get(align, Gtk.Align.FILL)
        else:
            _alignment = align

        super().set_halign(_alignment)

    def set_valign(self, align: Union[str, Gtk.Align] = Gtk.Align.FILL) -> None:

        if isinstance(align, (str)):
            _alignment = {
                "fill": Gtk.Align.FILL,
                "start": Gtk.Align.START,
                "end": Gtk.Align.END,
                "center": Gtk.Align.CENTER,
                "baseline": Gtk.Align.BASELINE,
            }.get(align, Gtk.Align.FILL)
        else:
            _alignment = align

        super().set_valign(_alignment)

    def set_active(self, param: bool) -> None:
        super().set_sensitive(param)

    def set_classname(self, classname: str) -> None:

        if isinstance(classname, (str)):
            context = self.get_style_context()
            [
                context.remove_class(i)
                for i in context.list_classes()
                if i not in self._default_classnames
            ]

            for j in classname.split(" "):
                if j != " ":
                    context.add_class(j)

    def get_classname(self) -> str:
        return " ".join(
            i
            for i in self.get_style_context().list_classes()
            if i not in self._default_classnames
        )

    def _add_randclassname(self) -> None:
        if not self._rand_classname:
            context = self.get_style_context()

            self._rand_classname = (
                self.get_name().replace("+", "_") + "_" + str(randint(1111, 9999))
            )
            context.add_class(self._rand_classname)

    def set_css(self, css_rules) -> None:
        self._add_randclassname()

        if css_rules and self._rand_classname:
            context = self.get_style_context()

            try:
                css_style = f".{self._rand_classname} {{{css_rules}}}"

                provider = Gtk.CssProvider()
                provider.load_from_data(css_style.encode())

                context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

            except Exception as e:
                print(e)

    def bind(
        self,
        variable: Union[Listener, Poll, Variable],
        callback: Callable,
        *args,
        **kwargs,
    ) -> None:
        variable.bind(callback, *args, **kwargs)
        # self.connect("destroy", lambda _: variable.run_dispose())

    def attributes(self, callback: Callable) -> None:
        callback(self)
