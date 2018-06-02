# Dindo Bot
# Copyright (c) 2018 - 2019 AXeL

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CustomComboBox(Gtk.ComboBoxText):

	def __init__(self, data=[], sort=False):
		Gtk.ComboBoxText.__init__(self)
		if sort:
			data = sorted(data)
		for text in data:
			self.append_text(text)

class CustomListBox(Gtk.ListBox):

	perform_scroll = False

	def __init__(self):
		Gtk.ListBox.__init__(self)
		self.set_selection_mode(Gtk.SelectionMode.NONE)
		self.connect('size-allocate', self.on_size_allocate)

	def on_size_allocate(self, widget, event):
		if self.perform_scroll:
			adj = widget.get_adjustment()
			adj.set_value(adj.get_upper() - adj.get_page_size())
			self.perform_scroll = False

	def append_text(self, text):
		# add new row with text & delete button
		row = Gtk.ListBoxRow()
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		row.add(hbox)
		label = Gtk.Label(text, xalign=0)
		label.set_margin_left(5)
		delete_button = Gtk.ModelButton()
		delete_button.set_image(Gtk.Image(stock=Gtk.STOCK_DELETE))
		delete_button.set_tooltip_text('Delete')
		delete_button.connect('clicked', self.on_delete_button_clicked)
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(delete_button, False, True, 0)
		self.add(row)
		self.show_all()
		self.perform_scroll = True

	def get_row_text(self, row):
		label = row.get_children()[0].get_children()[0]
		return label.get_text()

	def on_delete_button_clicked(self, button):
		row = button.get_parent().get_parent()
		self.remove(row)

class CustomScaleButton(Gtk.Button):

	def __init__(self, value=0, min=0, max=100, step=1):
		Gtk.Button.__init__(self, value)
		adjustment = Gtk.Adjustment(value=value, lower=min, upper=max, step_increment=step, page_increment=step, page_size=0)
		self.scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment, digits=0)
		self.scale.set_size_request(100, -1)
		self.scale.connect('value-changed', self.on_value_changed)
		self.popover = Gtk.Popover(relative_to=self, position=Gtk.PositionType.TOP)
		self.popover.add(self.scale)
		self.connect('clicked', self.on_clicked)

	def on_clicked(self, button):
		self.popover.show_all()

	def on_value_changed(self, button):
		value = int(self.scale.get_value())
		self.set_label(str(value))

	def get_value(self):
		return int(self.get_label())

class CustomSpinButton(Gtk.Button):

	def __init__(self, value=0, min=0, max=100, step=1):
		Gtk.Button.__init__(self, value)
		adjustment = Gtk.Adjustment(value=value, lower=min, upper=max, step_increment=step, page_increment=step, page_size=0)
		self.spin_button = Gtk.SpinButton(adjustment=adjustment)
		self.spin_button.connect('value-changed', self.on_value_changed)
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		hbox.set_border_width(5)
		hbox.add(self.spin_button)
		self.popover = Gtk.Popover(relative_to=self, position=Gtk.PositionType.TOP)
		self.popover.add(hbox)
		self.connect('clicked', self.on_clicked)

	def on_clicked(self, button):
		self.popover.show_all()

	def on_value_changed(self, button):
		value = self.spin_button.get_value_as_int()
		self.set_label(str(value))

	def get_value(self):
		return int(self.get_label())