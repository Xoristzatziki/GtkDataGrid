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


import sqlite3

class SQLite3Memory():
    """Encapsulate all comunication with the DB.

    Using SQLite3.
    """
    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        if self.memconn != None:
            self.memconn.close()
        return True

    def __repr__(self):
        return "<"+self.__module__+'.'+self.__class__.__name__+" "+repr(output)+">"

    def __init__(self):
        self.memconn = sqlite3.connect(":memory:")
        self.create_start_DB()
        self.add_dummy_records()

    def create_start_DB(self):
        try:
            mycursor = self.memconn.cursor()
            mycursor.execute('''CREATE TABLE maintbl
                         (col1 text PRIMARY KEY,
                         col2 INTEGER, col3 INTEGER, col4 REAL, col5 REAL) WITHOUT ROWID;''')
            return True
        except Exception as e:
            print('createDb error:',e)
        return False

    def add_dummy_records(self):
        try:
            mycursor = self.memconn.cursor()
            mycursor.execute("insert into maintbl values (?, ?, ?, ?, ?);", ('rec1text', 15, 5, 0.2, 11.2))
            mycursor.execute("insert into maintbl values (?, ?, ?, ?, ?);", ('rec2text', 16, 4, 0.4, 11.6))
            mycursor.execute("insert into maintbl values (?, ?, ?, ?, ?);", ('rec3text', 17, 3, 0.3, 12.2))
            mycursor.execute("insert into maintbl values (?, ?, ?, ?, ?);", ('rec4text', 25, 2, 0.5, 12.5))
            mycursor.execute("insert into maintbl values (?, ?, ?, ?, ?);", ('rec5text', 26, 1, 0.2, 14.7))
            return True
        except Exception as e:
            print('add_dummy_records error:',e)
        return False

    def get_all_records(self):

        try:
            mycursor = self.memconn.cursor()
            mycursor.execute('''SELECT * FROM maintbl;''')
            names = list(map(lambda x: x[0], mycursor.description))
            manyrows = mycursor.fetchall()

            return manyrows, names
            #titles = [x[0] for x in manyrows]
            #if len(titles):
                #print('len(titles)',len(titles))
                #return titles
            #else:
                #print('len(titles)',len(titles))
                #return []
        except sqlite3.IntegrityError:
            return 'DB IntegrityError ERROR',[]
        except Exception as e:
            #myprint('Exception in:', inspect.stack()[0][3],e.args)
            raise

    def get_all_records_in_dict(self):
        try:

            self.memconn.row_factory = sqlite3.Row
            mycursor = self.memconn.cursor()
            mycursor.execute('''SELECT * FROM maintbl;''')
            result = [dict(row) for row in mycursor.fetchall()]

            return result
            #titles = [x[0] for x in manyrows]
            #if len(titles):
                #print('len(titles)',len(titles))
                #return titles
            #else:
                #print('len(titles)',len(titles))
                #return []
        except sqlite3.IntegrityError:
            return 'DB IntegrityError ERROR'
        except Exception as e:
            #myprint('Exception in:', inspect.stack()[0][3],e.args)
            raise

    def get_all_records_in_dict2(self):
        try:

            #self.memconn.row_factory = sqlite3.Row
            self.memconn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
            mycursor = self.memconn.cursor()
            mycursor.execute('''SELECT * FROM maintbl;''')
            result = mycursor.fetchall()
            #db.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
            print(result)
            return result
            #titles = [x[0] for x in manyrows]
            #if len(titles):
                #print('len(titles)',len(titles))
                #return titles
            #else:
                #print('len(titles)',len(titles))
                #return []
        except sqlite3.IntegrityError:
            return 'DB IntegrityError ERROR'
        except Exception as e:
            #myprint('Exception in:', inspect.stack()[0][3],e.args)
            raise
