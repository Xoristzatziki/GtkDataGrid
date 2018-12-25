#!/usr/bin/env python3
#FIXME:
# This is an example class generated using a bare glade file.
#
#FIXME:
"""
    Copyright (C) ilias iliadis, 2018-12-22; ilias iliadis <>

    This file is part of GtkDatagrid.

    GtkDatagrid is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GtkDatagrid is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GtkDatagrid.  If not, see <http://www.gnu.org/licenses/>.
"""
__version__ = '0.0.1'

import locale
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

def apply_a_css():
    css = b"""

GtkTreeView row:nth-child(even) {
    border-style: solid;
    border-width: 0 0 2px 0;
    border-color: #666;
}
GtkTreeView row:nth-child(odd) {
    border-style: solid;
    border-width: 0 0 4px 0;
    border-color: #333;
}
CellRendererText {
    padding: 3px 3px;
    }
#blahblah {
    border-style: solid;
    border-width: 3px 3px 3px 3px;
    border-color: #333;
}
    """
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
