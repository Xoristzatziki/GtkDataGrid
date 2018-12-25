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
    import locale
    from copy import deepcopy

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk
    from gi.repository.GdkPixbuf import Pixbuf

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

column_types = {'str':'gchararray',
        'int':'glong',
        'long':'glong',
        'float':'gfloat',
        'pixbuf':'GdkPixbuf', #TODO: implement the pixbuf
        'checkbox': 'gboolean'
        }
#make_closure = int( str(lambda var: lambda: var))

def make_closure(var):
    newvar = deepcopy(var)
    return newvar
def change(x, newvalue):
    x[0] = newvalue
class BasicDataGrid():
    """ Main class for creating a basic GtkDataGrid. """

    def __init__(self, *args, **kwargs):
        self.parent_box = kwargs['parent_box']
        self.scrollbox = Gtk.ScrolledWindow()

        self.columns = {}
        self.data = None
        self.base_model = None
        self.withcounter = False
        self.row_is_dirty = False
        #self.number_of_columns = 0
        self.pixbuf_save = Gtk.IconTheme.get_default().load_icon('document-save', 64, 0)
        #print(type(self.pixbuf_save))
        if 'columns' in kwargs:
            #self.given_columns = {}# kwargs['columns']
            for i, acolumn in enumerate(kwargs['columns']):
                self.columns[i] = {'name': acolumn['name'],
                        'type' : acolumn['type'],
                        'format': acolumn['format'],
                        'editable': acolumn['editable']}
            if 'counter' in kwargs and kwargs['counter']:
                #self.columns[len(self.columns)]={'name': acolumn['N'],
                        #'type' : 'counter', #dummy type
                        #'format': None}
                self.withcounter = True

            self._create_the_model()
            self._create_the_gridview()
            self.scrollbox.add(self.thegrid)
            self.parent_box.add(self.scrollbox)
            self.scrollbox.set_vexpand(True)
            self.parent_box.show_all()

            #self.fill_with_data()

            numberofcolumns = self.base_model.get_n_columns()

            print('GRID CREATED')

        #save_icon = Gtk.IconTheme.load_icon(i, "gtk-no", 22, Gtk.IconLookupFlags.USE_BUILTIN)

    def fill_with_data(self, data=None,on_changed=None):

        self.base_model.clear()
        self.data = data

        for recordcounter, arecord in enumerate(self.data):
            depth0 = self.base_model.append(None)
            #print('self.base_model.get_n_columns()',self.base_model.get_n_columns())
            for columncounter, afield in enumerate(arecord):
                self.base_model.set_value(depth0, columncounter, afield)
            self.base_model.set_value(depth0, self.base_model.get_n_columns()-2, recordcounter+1)
            self.base_model.set_value(depth0, self.base_model.get_n_columns()-1, "document-save")#"document-save")
        self.thegrid.set_model(self.base_model)
        if on_changed !=None:
            select = self.thegrid.get_selection()
            select.connect("changed", on_changed, (self,))
        print('fill_with_data FINISHED')

    def _create_the_model(self):
        if self.base_model:
            self.base_model.clear()
        #create the model types
        thetuple = tuple()
        for acolumn in sorted(self.columns):
            thetuple = thetuple +  (column_types[self.columns[acolumn]['type']],)

        #add a hidden long that will act as counter or id
        thetuple = thetuple +  ('glong',)
        thetuple = thetuple +  ('gchararray',)
        self.base_model = Gtk.TreeStore(*thetuple)

    def _create_the_gridview(self):
        self.thegrid = Gtk.TreeView(model=self.base_model)
        if self.withcounter:
            renderer = Gtk.CellRendererText()
            renderer.set_alignment(1,0)

            renderer.set_property("background-rgba", Gdk.RGBA(red=0.8, green=0.8, blue=0.8, alpha=1.0))
            #renderer.set_name("blahblah")
            #print(renderer.list_properties())

            column = Gtk.TreeViewColumn('N', renderer, text=len(self.columns))
            #column.add_attribute(renderer, 'name', len(self.columns))

            column.set_sort_column_id(len(self.columns)-1)

            self.thegrid.append_column(column)
        for acolumn in self.columns:
            #print(self.columns[acolumn])
            rendercolumn = None
            if self.columns[acolumn]['type'] == 'str':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(0,0)
                renderer.set_property("editable", self.columns[acolumn]['editable'])
                column = Gtk.TreeViewColumn(self.columns[acolumn]['name'], renderer, text=acolumn)
            elif self.columns[acolumn]['type'] == 'long':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(1,0)
                renderer.set_property("editable", self.columns[acolumn]['editable'])
                renderer.connect("edited", self.long_edited, acolumn)
                #column = Gtk.TreeViewColumn(self.columns[acolumn]['name'], renderer, text=acolumn)
                column = LongTreeViewColumn(self.columns[acolumn]['name'], renderer, text=acolumn, theformat=self.columns[acolumn]['format'])
            elif self.columns[acolumn]['type'] == 'float':
                renderer = Gtk.CellRendererText()
                renderer.set_alignment(1,0)
                renderer.set_property("editable", self.columns[acolumn]['editable'])
                renderer.connect("edited", self.float_edited, acolumn)
                column = FloatTreeViewColumn(self.columns[acolumn]['name'], renderer, text=acolumn, theformat=self.columns[acolumn]['format'])
            elif self.columns[acolumn]['type'] == 'checkbox':
                renderer = Gtk.CellRendererToggle()
                #DataGrid is not supposed to have radio buttons
                #renderer.set_radio(self.columns[acolumn]['format'] == 'radio')
                renderer.connect("toggled", self.on_cell_toggled, acolumn)
                column = Gtk.TreeViewColumn(self.columns[acolumn]['name'], renderer, active=acolumn)
            #set autosizing

            column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            #make resizable
            column.set_resizable(True)
            #use the contents for sorting

            column.set_sort_column_id(acolumn)
            self.thegrid.append_column(column)
        renderer = Gtk.CellRendererPixbuf()
        #renderer = Gtk.CellRenderer()
        #renderer.connect("activate", self.on_save_clicked, len(self.columns))
        column = Gtk.TreeViewColumn("Image", renderer, icon_name=len(self.columns)+1)
        column.set_max_width(30)

        self.thegrid.append_column(column)

    def on_cell_toggled(self, widget, path, *args):
        column = args[0]
        self.base_model[path][column] = not self.base_model[path][column]
        self.row_is_dirty = True

    def long_edited(self, widget, path, text,*args):
        column = args[0]
        self.base_model[path][column] = locale.atoi(text)
        self.row_is_dirty = True

    def float_edited(self, widget, path, text,*args):
        column = args[0]
        self.base_model[path][column] = locale.atof(text)
        self.row_is_dirty = True


    def on_save_clicked(self, event, widget, path, background_area, cell_area, flags):
        print(event, widget, path, background_area, cell_area, flags)


def floatCellDataFunc(treeViewColumn, cellRenderer, model, iter, args):
    val = model.get(iter, args[0])
    val = val[0]
    #the only way to respect locale
    newval = locale.format(args[1], val)
    return cellRenderer.set_property("text", newval)

def longCellDataFunc(treeViewColumn, cellRenderer, model, iter, args):
    val = model.get(iter, args[0])
    val = val[0]
    #the only way to respect locale
    newval = locale.format(args[1], val, grouping=True)
    return cellRenderer.set_property("text", newval)

def numberCellDataFunc(treeViewColumn, cellRenderer, model, iter, args):
    val = model.get(iter, args[0])
    val = val[0]
    #the only way to respect locale
    newval = locale.format_string(args[1], val)
    return cellRenderer.set_property("text", newval)

class FloatTreeViewColumn(Gtk.TreeViewColumn):
    def __init__(self, title, cell_renderer, text=0, theformat="%.2f"):
        super().__init__(title, cell_renderer, text=text)
        argstopass = (text, theformat)
        self.set_cell_data_func(cell_renderer, floatCellDataFunc, argstopass)

class LongTreeViewColumn(Gtk.TreeViewColumn):
    def __init__(self, title, cell_renderer, text=0, theformat="%n"):
        super().__init__(title, cell_renderer, text=text)
        argstopass = (text, theformat)
        self.set_cell_data_func(cell_renderer, longCellDataFunc, argstopass)

class NumberTreeViewColumn(Gtk.TreeViewColumn):
    def __init__(self, title, cell_renderer, text=0, theformat="%n"):
        super().__init__(title, cell_renderer, text=text)
        argstopass = (text, theformat)
        self.set_cell_data_func(cell_renderer, numberCellDataFunc, argstopass)
