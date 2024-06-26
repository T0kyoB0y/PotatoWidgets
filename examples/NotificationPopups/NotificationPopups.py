from PotatoWidgets import Widget, lookup_icon
from PotatoWidgets.Services import Notification as NotificationClass
from PotatoWidgets.Services import NotificationsService


def Notification(notif: NotificationClass):  # to have autocompletion

    if not notif:
        return

    if notif.image:
        if notif.image.endswith((".png", ".jpg")):
            IMAGE_WIDGET = Widget.Box(
                css=f"""
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center;
                    background-image: url("{notif.image}");
                    """,
                size=60,
                halign="center",
                valign="center",
                classname="image",
            )
        else:
            IMAGE_WIDGET = Widget.Icon(notif.image, 60)
    else:
        IMAGE_WIDGET = Widget.Image(lookup_icon(notif.name), 60)

    if notif.actions:
        _actions = Widget.Box(
            homogeneous=True,
            spacing=5,
            children=[
                (
                    lambda action: Widget.Button(
                        onclick=lambda: notif.action(action["id"]),
                        classname="actionbutton",
                        children=Widget.Label(action["label"]),
                    )
                )(i)
                for i in notif.actions
            ],
        )
    else:
        _actions = None

    return Widget.Button(
        classname="notification",
        primaryrelease=lambda: notif.dismiss(),
        attributes=lambda self: setattr(self, "id", notif.id),
        children=Widget.Box(
            orientation="v",
            spacing=10,
            children=[
                Widget.Box(
                    spacing=10,
                    children=[
                        IMAGE_WIDGET,
                        Widget.Box(
                            orientation="v",
                            valign="center",
                            spacing=5,
                            children=[
                                Widget.Label(
                                    notif.summary,
                                    justify="left",
                                    classname="header",
                                    xalign=0,
                                ),
                                Widget.Label(
                                    notif.body,
                                    wrap=True,
                                    justify="left",
                                    xalign=0,
                                    classname="content",
                                ),
                            ],
                        ),
                    ],
                ),
                _actions,
            ],
        ),
    )


NotificationsPopup = Widget.Window(
    layer="notification",
    position="top right",
    size=[450, 50],
    at={"right": 10, "top": 10},
    children=Widget.Box(
        orientation="v",
        spacing=10,
        classname="notifications-container",
        attributes=lambda self: (
            NotificationsService.connect(
                "popup",
                lambda instance, id: self.add(
                    Notification(instance.get_notification(id))
                ),
            ),
            NotificationsService.connect(
                "dismissed",
                lambda _, id: self.set_children(
                    [i for i in self.get_children() if getattr(i, "id") != id]
                ),
            ),
        ),
    ),
)
