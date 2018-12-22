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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

#import the class
from basicdatagrid import BasicDataGrid

class ExampleUsage(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="BasicDataGrid example usage")
        self.set_default_size(300, 200)

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL  ,spacing=6)
        self.add(vbox)

        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)
        button.set_vexpand(False)
        vbox.pack_start(button, False, False, 0)
        self.box1 = vbox

    def on_click_me_clicked(self, button):
        self.create_no_counter()
        self.create_with_counter()
        self.create_a_third()
        #disable the button
        button.set_sensitive(False)

    def create_with_counter(self):
        #create the grid which will be automatically appended
        #to the provided parent_box
        self.dg = BasicDataGrid(columns=[
                    {'name':'col1', 'type':'str', 'format':'left'},
                    {'name':'col2', 'type':'number', 'format':'{0:9.3f}'},
                    {'name':'col3', 'type':'checkbox', 'format':'radio'}
                ],
                parent_box=self.box1,
                counter = True)
        #the scrollbox is its parent widget
        #use it to expand the gridview
        self.dg.scrollbox.set_vexpand(True)

        #add dummy records
        dummyrecords = [
                ['dummy1',2,0],
                ['dummy2',7,0],
                ['dummy3',4,1],
                ['dummy4',8,0],
                ['dummy5',8,0],
                ['dummy6',8,0],
                ['dummy7',8,0],
                ['dummy25',25,1]
            ]
        self.dg.fill_with_data(dummyrecords)

        #create a label to show something
        self.label_for_selected = Gtk.Label("nothing selected")
        self.box1.add(self.label_for_selected)
        self.label_for_selected.show()

        #connect the selection to a function
        select = self.dg.thegrid.get_selection()
        select.connect("changed", self.onSelectionChanged1)

    def create_no_counter(self):
        #create the grid which will be automatically appended
        #to the provided parent_box
        self.dg2 = BasicDataGrid(columns=[
                    {'name':'col1', 'type':'str', 'format':'left'},
                    {'name':'col2', 'type':'number', 'format':'{0:9.3f}'},
                    {'name':'col3', 'type':'checkbox', 'format':'radio'}
                ],
                parent_box=self.box1,
                counter = False)
        #the scrollbox is its parent widget
        #use it to expand the gridview
        self.dg2.scrollbox.set_vexpand(True)

        #add dummy records
        dummyrecords = [
                ['dummyA1',9,0],
                ['dummyA2',1,0],
                ['dummyA3',5,1],
                ['dummyA4',32,0],
                ['dummyA25',25,1]
            ]
        self.dg2.fill_with_data(dummyrecords)

        #create a label to show something
        self.label_for_selected2 = Gtk.Label("nothing selected")
        self.box1.add(self.label_for_selected2)
        self.label_for_selected2.show()

        #connect the selection to a function
        select = self.dg2.thegrid.get_selection()
        select.connect("changed", self.onSelectionChanged2)

    def create_a_third(self):
        #create the grid which will be automatically appended
        #to the provided parent_box
        self.dg4 = BasicDataGrid(columns=[
                    {'name':'col1', 'type':'str', 'format':'left'},
                    {'name':'col2', 'type':'number', 'format':'{0:9.3f}'},
                    {'name':'col3', 'type':'checkbox', 'format':'radio'}
                ],
                parent_box=self.box1,
                counter = False)
        #the scrollbox is its parent widget
        #use it to expand the gridview
        self.dg4.scrollbox.set_vexpand(True)

        #add dummy records
        dummyrecords = [
                ['dummyA1',9,0],
                ['dummyA2',1,0],
                ['dummyA3',5,1],
                ['dummyA4',32,0],
                ['dummyA25',25,1]
            ]
        self.dg4.fill_with_data(dummyrecords)

        #create a label to show something
        self.label_for_selected4 = Gtk.Label("nothing selected")
        self.box1.add(self.label_for_selected4)
        self.label_for_selected4.show()

        #connect the selection to a function
        select = self.dg4.thegrid.get_selection()
        select.connect("changed", self.onSelectionChanged4)

    def onSelectionChanged1(self, tree_selection):
        model, pathlist = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            self.label_for_selected.set_label('SELECTED: ' + str(value))

    def onSelectionChanged2(self, tree_selection):
        model, pathlist = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            self.label_for_selected2.set_label('SELECTED: ' + str(value))

    def onSelectionChanged4(self, tree_selection):
        model, pathlist = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            self.label_for_selected4.set_label('SELECTED: ' + str(value))

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
CellRendererText{
    padding: 3px 3px;
    }
    """
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
apply_a_css()
win = ExampleUsage()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
