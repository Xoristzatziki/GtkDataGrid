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

try:
    import os
    import sys

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

column_types = {'str':'gchararray',
        'number':'gchararray',
        'pixbuf':'GdkPixbuf', #TODO: implement the pixbuf
        'checkbox': 'gboolean'
        }

class BasicDataGrid():
    """ Main class for creating a basic GtkDataGrid. """

    def __init__(self, *args, **kwargs):
        self.parent_box = kwargs['parent_box']
        self.scrollbox = Gtk.ScrolledWindow()

        self.columns = {}
        self.data = None
        self.base_model = None
        self.withcounter = False
        #self.number_of_columns = 0
        if 'columns' in kwargs:
            #self.given_columns = {}# kwargs['columns']
            for i, acolumn in enumerate(kwargs['columns']):
                self.columns[i] = {'name': acolumn['name'],
                        'type' : acolumn['type'],
                        'format': acolumn['format'] if 'format' in acolumn else None}
            if 'counter' in kwargs and kwargs['counter']:
                #self.columns[len(self.columns)]={'name': acolumn['N'],
                        #'type' : 'counter', #dummy type
                        #'format': None}
                self.withcounter = True
            self._create_the_model()
            self._create_the_gridview()
            self.scrollbox.add(self.thegrid)
            self.parent_box.add(self.scrollbox)
            self.parent_box.show_all()

            #self.fill_with_data()

            numberofcolumns = self.base_model.get_n_columns()
            print('CREATED',numberofcolumns)

    def fill_with_data(self, data=None):

        self.base_model.clear()
        self.data = data

        for recordcounter, arecord in enumerate(self.data):
            depth0 = self.base_model.append(None)
            for columncounter, afield in enumerate(arecord):
                theformat = self.columns[columncounter]['format']
                #print(columncounter, self.columns[columncounter]['type'])
                if self.columns[columncounter]['type'] == 'str':
                    self.base_model.set_value(depth0, columncounter, afield)
                elif self.columns[columncounter]['type'] == 'number':
                    self.base_model.set_value(depth0, columncounter, theformat.format(afield,))
                elif self.columns[columncounter]['type'] == 'checkbox':
                    self.base_model.set_value(depth0, columncounter, afield)
            self.base_model.set_value(depth0, self.base_model.get_n_columns()-1, recordcounter)
        self.thegrid.set_model(self.base_model)

    def _create_the_model(self):
        if self.base_model:
            self.base_model.clear()
        #create the model types
        thetuple = tuple()
        for acolumn in sorted(self.columns):
            thetuple = thetuple +  (column_types[self.columns[acolumn]['type']],)

        #add a hidden long that will act as counter or id
        thetuple = thetuple +  ('glong',)
        self.base_model = Gtk.TreeStore(*thetuple)

    def _create_the_gridview(self):
        self.thegrid = Gtk.TreeView(model=self.base_model)
        if self.withcounter:
            renderer = Gtk.CellRendererText()
            renderer.set_alignment(1,0)
            column = Gtk.TreeViewColumn('N', renderer, text=len(self.columns))
            column.set_sort_column_id(len(self.columns))
            self.thegrid.append_column(column)
        for acolumn in self.columns:
            if self.columns[acolumn]['type'] == 'str':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(0,0)
                column = Gtk.TreeViewColumn(self.columns[acolumn]['name'], renderer, text=acolumn)
            elif self.columns[acolumn]['type'] == 'number':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(1,0)
                column = Gtk.TreeViewColumn(self.columns[acolumn]['name'], renderer, text=acolumn)
            elif self.columns[acolumn]['type'] == 'checkbox':
                renderer = Gtk.CellRendererToggle()
                renderer.set_radio(self.columns[acolumn]['format'] == 'radio')
                column = Gtk.TreeViewColumn(self.columns[acolumn]['name'], renderer, active=acolumn)
            #set autosizing
            column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            #make resizable
            column.set_resizable(True)
            #use the contents for sorting
            #Warning! Handles numbers as strings!!!
            column.set_sort_column_id(acolumn)
            self.thegrid.append_column(column)
