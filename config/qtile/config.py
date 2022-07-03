# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

colors = ['#8f2100', '#000000', '#979aaa']

mod = "mod4"
terminal = 'kitty'

def tasklist_parser(text):
    return text
    # for string in [" - Chromium", " - Mozilla Firefox", " - Code - OSS"]:
    #     text = text.replace(string, "")
    # return text

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.run_extension(extension.DmenuRun(
        font='Ubuntu Bold',
        fontsize='10',
        dmenu_command='dmenu_run',
        dmenu_prompt='⟿ ',
        dmenu_height=25,
        dmenu_lines=0,
        background=colors[2],
        foreground=colors[0],
        selected_foreground=colors[1],
        selected_background=colors[2],
    )))
]

groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_width=0, margin=4),
    layout.Max(),
    # layout.Floating(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 10,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def right_arrow(bg_color, fg_color):
    return widget.TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=26,
        background=bg_color,
        foreground=fg_color)

def left_arrow(bg_color, fg_color):
    return widget.TextBox(
        text='\uE0B2',
        padding=0,
        fontsize=26,
        background=bg_color,
        foreground=fg_color)

screens = [
    Screen(
        wallpaper='~/.config/qtile/wallpaper.jpg',
        top=bar.Bar([
            widget.GroupBox(
                highlight_method='text',
                this_screen_border=colors[2],
                this_current_screen_border=colors[2],
                other_current_screen_border=colors[1],
                other_screen_border=colors[1],
                background=colors[0]
            ),
            right_arrow(colors[2], colors[0]),
            widget.TaskList(
                background=colors[2],
                highlight_method='border',
                foreground=colors[0],
                unfocused_border=colors[1],
                borderwidth=0,
                padding=5,
                parse_text=tasklist_parser
            ),
            left_arrow(colors[2], colors[0]),
            widget.Battery(
                foreground=colors[2],
                background=colors[0],
                format='{char} {percent:2.0%}',
                padding=5
            ),
            left_arrow(colors[0], colors[2]),
            widget.Volume(
                foreground = colors[0],
                background = colors[2],
                fmt = 'Vol: {}',
                padding = 5
                ),
            left_arrow(colors[2], colors[0]),
            widget.Clock(
                foreground=colors[2],
                background=colors[0],
                format='%d/%m/%y %H:%M',
                padding=5
            ),
            ], 25, opacity=1),
        ),
        Screen(
        wallpaper='~/.config/qtile/wallpaper.jpg',
        top=bar.Bar([
            widget.GroupBox(
                highlight_method='text',
                this_screen_border=colors[2],
                this_current_screen_border=colors[2],
                other_current_screen_border=colors[1],
                other_screen_border=colors[1],
                background=colors[0]
            ),
            right_arrow(colors[2], colors[0]),
            widget.TaskList(
                background=colors[2],
                highlight_method='border',
                foreground=colors[0],
                unfocused_border=colors[1],
                borderwidth=0,
                padding=5,
                parse_text=tasklist_parser,
            ),
            left_arrow(colors[2], colors[0]),
            widget.Battery(
                foreground=colors[2],
                background=colors[0],
                format='{char} {percent:2.0%}',
                padding=5
            ),
            left_arrow(colors[0], colors[2]),
            widget.Volume(
                foreground = colors[0],
                background = colors[2],
                fmt = 'Vol: {}',
                padding = 5
                ),
            left_arrow(colors[2], colors[0]),
            widget.Clock(
                foreground=colors[2],
                background=colors[0],
                format='%d/%m/%y %H:%M',
                padding=5
            ),
            ], 25, opacity=1),
        ),
    ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button0", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button2", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    Key([mod,"shift"],  "Right",  lazy.function(window_to_next_screen)),    
    Key([mod,"shift"],  "Left", lazy.function(window_to_previous_screen)),
    Key([mod,"control"],"Right",  lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"control"],"Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])