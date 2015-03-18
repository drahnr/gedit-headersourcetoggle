#!/usr/bin/env python

"""Header Source Toggle plugin for Gedit3
https://github.com/drahnr/gedit3-headersourcetoggle

(C) 2015 Bernhard Schuster <hej@ahoi.io>
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
		self.app.add_accelerator("<Control>r", "win.headersourcetoggle", None)

	def do_deactivate(self):
		print ("APP do remove called")
		self.app.remove_accelerator("win.headersourcetoggle")




class HeaderSourceToggleWindow(GObject.Object, Gedit.WindowActivatable):
	window = GObject.property(type=Gedit.Window)

	action = None

	def __init__(self):
		GObject.Object.__init__(self)

	def do_header_source_toggle(self, action, data=None):
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
		if ext.lower() in (".h", ".hpp"):
			complement_extensions = [".c", ".cpp"]
		elif ext.lower() in (".c", ".cpp"):
			complement_extensions = [".h", ".hpp"]
		else:
			return

		complement = None
		for ext in complement_extensions:
			for case in [ext.lower(), ext.upper()]:
				if os.path.isfile(root + case):
					complement = root + case
					break
		if complement:
			for doc in self.window.get_documents():
				loc = doc.get_location()
				if not loc:
					continue
				path = loc.get_path()
				if path == complement:
					tab = Gedit.Tab.get_from_document(doc)
					if tab:
						self.window.set_active_tab(tab)
						return
			self.window.create_tab_from_location(Gio.file_new_for_path(complement), None, 0, 0, False, True)


	def do_activate(self):
		print ("WIN do activate called")
		self.action = Gio.SimpleAction(name="headersourcetoggle")
		self.action.connect('activate', lambda a, p: self.do_header_source_toggle(self.action))
		self.window.add_action(self.action)

#		button = Gtk.Button.new()
#		button.set_label("Toggle Header/Source")
#		button.set_action_name("headersourcetoggle")
#		self.window.add(button)
#		button.show()

	def do_update_state(self):
		print ("WIN updating UI")
		self.window.lookup_action("headersourcetoggle").set_enabled(self.window.get_active_document() is not None)

	def do_deactivate(self):
		print ("WIN do remove called")
		self.window.remove_action("headersourcetoggle")
		
