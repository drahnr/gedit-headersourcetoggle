#!/usr/bin/env python

"""Header Source Toggle plugin for Gedit3

Copyright (C) 2015 Bernhard Schuster

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

__author__ = "Bernhard Schuster"
__email__ = "hej@ahoi.io"


import os
from gi.repository import GObject, Gio, Gtk, Gedit, Gio


class HeaderSourceToggleApp(GObject.Object, Gedit.AppActivatable):
	app = GObject.property(type=Gedit.App)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.app.add_accelerator("F3", "win.headersourcetoggle", None)

	def do_deactivate(self):
		self.app.remove_accelerator("win.headersourcetoggle")




class HeaderSourceToggleWindow(GObject.Object, Gedit.WindowActivatable):
	window = GObject.property(type=Gedit.Window)

	action = None

	def __init__(self):
		GObject.Object.__init__(self)


	def tab_magic(self, complement):
		if not complement:
			return
		for doc in self.window.get_documents():
			loc = doc.get_location()
			if loc and loc.get_path() == complement:
				tab = Gedit.Tab.get_from_document(doc)
				if tab:
					self.window.set_active_tab(tab)
					return
		self.window.create_tab_from_location(Gio.file_new_for_path(complement), None, 0, 0, False, True)

	def toggle_header_source(self, action, data=None):
		doc = self.window.get_active_document()
		if not doc:
			return

		loc = doc.get_location()
		if not loc:
			return

		path = loc.get_path()
		if not path:
			return

		#TODO: some projects have them in src/*.c and inc/*.h
		root, ext = os.path.splitext(path)
		ext = ext.lower()
		if ext in (".h", ".hpp"):
			complement_extensions = [".c", ".cpp", ".cxx"]
		elif ext in (".c", ".cpp"):
			complement_extensions = [".h", ".hpp", ".hxx"]
		else:
			return

		complement = None
		for ext in complement_extensions:
			for case in [ext.lower(), ext.upper()]:
				if os.path.isfile(root + case):
					complement = root + case
					break

		self.tab_magic(complement)

	def do_activate(self):
		self.action = Gio.SimpleAction(name="headersourcetoggle")
		self.action.connect('activate', lambda sender, data: self.toggle_header_source(self.action))
		self.window.add_action(self.action)

#		button = Gtk.Button.new()
#		button.set_label("Toggle Header/Source")
#		button.set_action_name("headersourcetoggle")
#		self.window.add(button)
#		button.show()

	def do_update_state(self):
		if self.action:
			self.action.set_enabled(self.window.get_active_document() is not None)

	def do_deactivate(self):
		self.window.remove_action("headersourcetoggle")
		
