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

#import the classes
from styles import apply_a_css
import testdb

from basicdatagrid import BasicDataGrid

class ExampleUsage(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="BasicDataGrid example usage")
        self.set_default_size(600, 600)

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL  ,spacing=6)
        self.add(vbox)

        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)
        button.set_vexpand(False)
        vbox.pack_start(button, False, False, 0)
        self.box1 = vbox

    def on_click_me_clicked2(self, button):
        #self.create_no_counter()
        #self.create_with_counter()
        #self.create_a_third()
        allrecords = None
        with testdb.SQLite3Memory() as db:
            allrecords = db.get_all_records_in_dict2()
        if allrecords:
            print()
            print(allrecords)
            print(dir(allrecords[0]))
            return
            for arecord in allrecords:
                print(dir(arecord[0]))
            return
            for arecord in allrecords[0]:
                if isinstance(arecord, int):
                    print(arecord, 'is int')
                if isinstance(arecord, str):
                    print(arecord, 'is str')
                if isinstance(arecord, float):
                    print(arecord, 'is float')
            print(names)
        else:
            print('Nothing')
        #disable the button
        button.set_sensitive(False)

    def on_click_me_clicked(self, button):
        #self.create_no_counter()
        #self.create_with_counter()
        #self.create_a_third()

        self.create_fron_db()
        self.create_fron_db(True)

        button.set_sensitive(False)

    def create_fron_db(self, withcounter=False):
        allrecords = None
        columns = []
        with testdb.SQLite3Memory() as db:
            allrecords, names = db.get_all_records()

        if allrecords:
            arow = allrecords[0]
            #print(len(names))
            for i, aname in enumerate(names):
                #print('enumerating')
                rowdict = {}
                rowdict['name']=aname
                if isinstance(arow[i], int):
                    rowdict['type'] = 'long'
                    rowdict['format'] = '%d'
                    rowdict['editable'] = True
                elif isinstance(arow[i], str):
                    rowdict['type'] = 'str'
                    rowdict['format'] = 'left'
                    rowdict['editable'] = True
                elif isinstance(arow[i], float):
                    rowdict['type'] = 'float'
                    rowdict['format'] = '%.2f'
                    rowdict['editable'] = True
                elif isinstance(arow[i], bytearray):
                    rowdict['type'] = 'BLOB'
                    rowdict['format'] = ''
                    rowdict['editable'] = False
                else:
                    rowdict['type'] = 'BLOB'
                    rowdict['format'] = ''
                    rowdict['editable'] = False
                columns.append(rowdict)
                #print('columns ok')
            else:
                #print('Nothing')
                pass

            dummyrecords = [x for x in [x for x in allrecords]]

            #print(dummyrecords)
            #print(columns)
            self.dg = BasicDataGrid(columns=columns,
                parent_box=self.box1,
                counter=withcounter)

            self.dg.fill_with_data(dummyrecords, on_changed=self.onSelectionChangedany)

            #create a label to show something
            self.label_for_selected = Gtk.Label("nothing selected")
            self.box1.add(self.label_for_selected)
            self.label_for_selected.show()

    def create_with_counter(self):
        #create the grid which will be automatically appended
        #to the provided parent_box
        self.dg = BasicDataGrid(columns=[
                    {'name':'col1', 'type':'str', 'format':'left','editable': False},
                    {'name':'supplem', 'type':'str', 'format':'left','editable': False},
                    {'name':'col2', 'type':'long', 'format':'%d','editable': True},
                    {'name':'col2', 'type':'long', 'format':'%d','editable': True},
                    {'name':'col2a', 'type':'float', 'format':'%.2f','editable': False},
                    {'name':'col3', 'type':'checkbox', 'format':'radio','editable': True},
                    {'name':'col4', 'type':'float', 'format':'%.3f','editable': True},
                    {'name':'col5', 'type':'float', 'format':'%.1f','editable': True}
                ],
                parent_box=self.box1,

                counter = True)

        #add dummy records
        dummyrecords = [
                ['dummy1','supp1',1,2,2.4,0,3.1,5.4],
                ['dummy2','supp1',2,2,7.3,0,4.2,5.5],
                ['dummy3','supp1',3,4,4.7,1,5.3,5.6],
                ['dummy4','supp1',15,2,8.6,0,8,5.7],
                ['dummy5','supp1',10202025,7,8.3,0,9,5.8],
                ['dummy6','supp1',30,6,8.4,0,10,5.9],
                ['dummy7','supp1',4,2,8.2,0,11,5.3],
                ['dummy25','supp1',50,2,25.6,1,12,5.2]
            ]
        self.dg.fill_with_data(dummyrecords, on_changed=self.onSelectionChangedany)

        #create a label to show something
        self.label_for_selected = Gtk.Label("nothing selected")
        self.box1.add(self.label_for_selected)
        self.label_for_selected.show()

        #connect the selection to a function
        #select = self.dg.thegrid.get_selection()
        #select.connect("changed", self.onSelectionChanged1)
        apply_a_css()

    def create_no_counter(self):
        #create the grid which will be automatically appended
        #to the provided parent_box
        self.dg2 = BasicDataGrid(columns=[
                    {'name':'col1', 'type':'str', 'format':'left','editable': False},
                    {'name':'col2', 'type':'long', 'format':'{0:n}','editable': True},
                    {'name':'col3', 'type':'checkbox', 'format':'radio','editable': True}
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
                    {'name':'col1', 'type':'str', 'format':'left','editable': False},
                    {'name':'col2', 'type':'long', 'format':'{0:n}','editable': True},
                    {'name':'col3', 'type':'checkbox', 'format':'radio','editable': True}
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

    def onSelectionChangedany(self, tree_selection, *args):
        """The  dg instance is provided here.

        We can print to a specific label
        based on the instance.

        """
        print(tree_selection, args)
        model, pathlist = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            self.label_for_selected.set_label('SELECTED: ' + str(value))

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


apply_a_css()
win = ExampleUsage()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
