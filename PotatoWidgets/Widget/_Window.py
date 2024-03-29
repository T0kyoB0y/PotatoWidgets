from ..Imports import *
from ..Variable import Listener, Poll, Variable

cleantextX = lambda x, perheight: (
    perheight(str(x).replace("%", ""))
    if "%" in str(x)
    else float(str(x).replace("px", ""))
)
cleantextY = lambda x, perwidth: (
    perwidth(str(x).replace("%", ""))
    if "%" in str(x)
    else float(str(x).replace("px", ""))
)


class Window(Gtk.Window):
    def __init__(
        self,
        size=[0, 0],
        at={},
        position="center",
        layer="top",
        exclusive=False,
        children=None,
        monitor=0,
        parent=None,
        focusable="none",
        popup=False,
        namespace="gtk-layer-shell",
        attributes=None,
        **kwargs,
    ):
        Gtk.Window.__init__(self)
        self.monitor = monitor
        self._screen_width, self._screen_height = self.__calculateResolution(
            self.monitor
        )
        self._perheight = lambda x: (float(x) * self._screen_height) / 100
        self._perwidth = lambda x: (float(x) * self._screen_width) / 100
        self.properties = self.__adjustProps(
            {
                "size": size,
                "at": at,
                "position": position,
                "layer": layer,
                "exclusive": exclusive,
                "namespace": namespace,
            }
        )
        self.add(children) if children else None
        # Other settings for the window
        # Useful for popups or something like that
        self.set_transient_for(parent) if parent else None
        self.set_destroy_with_parent(True if parent else False)

        # GtkLayerShell SETTING, etc...
        if not locals().get("disable_gtklayershell", False):
            GtkLayerShell.init_for_window(self)
            GtkLayerShell.set_namespace(self, self.properties.get("namespace"))
            GtkLayerShell.set_layer(
                self, self.__clasif_layer(self.properties.get("layer", "top"))
            )

        self.__clasif_position(self.properties.get("position", "center"))
        self.__clasif_exclusive(self.properties.get("exclusive", False))
        self.__clasif_at(self.properties.get("at", False))
        self.set_size_request(
            max(self.properties["size"][0], 10), max(self.properties["size"][1], 10)
        )

        # self.connect("destroy", Gtk.main_quit)

        self.set_focusable(focusable)
        self.set_popup(popup)
        attributes(self) if attributes else None

        if self.popup:
            # Connect the key-press-event signal to handle the Escape key
            self.connect("key-press-event", self.on_key_press)
            # Connect the button-press-event signal to handle clicks outside the window
            self.connect("button-press-event", self.on_button_press)

        self.close()

    def on_key_press(self, _, event):
        # Handle key-press-event signal (Escape key)
        if event.keyval == Gdk.KEY_Escape:
            self.close()

    def on_button_press(self, _, event):
        # Handle button-press-event signal (click outside the window)
        if (
            event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1
        ):  # Left mouse button
            x, y = event.x_root, event.y_root
            frame_extents = self.get_window().get_frame_extents()
            if (
                x < frame_extents.x
                or x >= frame_extents.x + frame_extents.width
                or y < frame_extents.y
                or y >= frame_extents.y + frame_extents.height
            ):
                self.close()

    def set_focusable(self, focusable):
        focusable_mode = {
            "onfocus": GtkLayerShell.KeyboardMode.ON_DEMAND,
            "force": GtkLayerShell.KeyboardMode.EXCLUSIVE,
            "none": GtkLayerShell.KeyboardMode.NONE,
        }.get(focusable, GtkLayerShell.KeyboardMode.NONE)

        GtkLayerShell.set_keyboard_mode(self, focusable_mode)

    def set_popup(self, popup):
        self.popup = popup
        if popup:
            # Set the window type hint to POPUP
            self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        else:
            # Set the window type hint to NORMAL
            self.set_type_hint(Gdk.WindowTypeHint.NORMAL)

    def __adjustProps(self, props):
        at = props.get("at", {"top": 0, "bottom": 0, "left": 0, "right": 0})

        at["top"] = cleantextY(at.get("top", 0), self._perwidth)
        at["bottom"] = cleantextY(at.get("bottom", 0), self._perwidth)
        at["left"] = cleantextX(at.get("left", 0), self._perheight)
        at["right"] = cleantextX(at.get("right", 0), self._perheight)

        size = props.get("size", [0, 0])

        props["size"] = [
            cleantextX(size[0], self._perwidth),
            cleantextY(size[1], self._perheight),
        ]
        props["at"] = at

        return props

    def __calculateResolution(self, monitor):
        display = Gdk.Display.get_default()
        n_monitors = display.get_n_monitors()

        if monitor < 0 or monitor >= n_monitors:
            raise ValueError(f"Invalid monitor index: {monitor}")

        monitors = [display.get_monitor(i).get_geometry() for i in range(n_monitors)]
        selected_monitor = monitors[monitor]

        return selected_monitor.width, selected_monitor.height

    def __clasif_layer(self, layer):
        if layer.lower() in ["background", "bg"]:
            return GtkLayerShell.Layer.BACKGROUND
        elif layer.lower() in ["bottom", "bt"]:
            return GtkLayerShell.Layer.BOTTOM
        elif layer.lower() in ["top", "tp"]:
            return GtkLayerShell.Layer.TOP
        elif layer.lower() in ["overlay", "ov"]:
            return GtkLayerShell.Layer.OVERLAY

    def __clasif_position(self, position):
        for i in position.lower().split(" "):
            if i in ["top", "tp"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)

            elif i in ["bottom", "bt"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)

            elif i in ["left", "lf"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)

            elif i in ["right", "rg"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)

            elif i in ["center", "ct"]:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, False)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, False)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, False)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)

    def __clasif_exclusive(self, exclusivity):
        if exclusivity == True:
            return GtkLayerShell.auto_exclusive_zone_enable(self)
        elif isinstance(exclusivity, int):
            return GtkLayerShell.set_exclusive_zone(self, exclusivity)
        else:
            return

    def __clasif_at(self, at):
        if at:
            for key, value in at.items():
                if key in ["top", "tp"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, value)

                elif key in ["bottom", "bt"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.BOTTOM, value)

                elif key in ["left", "lf"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, value)

                elif key in ["right", "rg"]:
                    GtkLayerShell.set_margin(self, GtkLayerShell.Edge.RIGHT, value)

                elif key in ["center", "ct"]:
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, False)
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, False)
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, False)
                    GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, False)

    def bind(self, var, callback):
        if isinstance(var, (Listener, Variable, Poll)):
            var.connect(
                "valuechanged", lambda x: GLib.idle_add(lambda: callback(x.get_value()))
            )

    def open(self, duration=0):
        self.show()

        if duration > 0:
            GLib.timeout_add(duration, lambda: self.close())

    def close(self):
        self.hide()

    def toggle(self):
        if self.get_visible():
            self.close()
        else:
            self.open()

    def __str__(self) -> str:
        return str(self.properties["namespace"])

    def __repr__(self) -> str:
        return str(self.properties["namespace"])
