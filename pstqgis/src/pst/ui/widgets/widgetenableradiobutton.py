"""
Copyright 2019 Meta Berghauser Pont

This file is part of PST.

PST is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. The GNU General Public License
is intended to guarantee your freedom to share and change all versions
of a program--to make sure it remains free software for all its users.

PST is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PST. If not, see <http://www.gnu.org/licenses/>.
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QRadioButton

class WidgetEnableRadioButton(QRadioButton):
	def __init__(self, text, widgets=[], parent=None):
		QRadioButton.__init__(self, text, parent)
		self._widgets = []
		for w in widgets:
			self.addWidget(w)
		self.toggled.connect(self.onToggled)

	def addWidget(self, w):
		self._widgets.append(w)
		w.setEnabled(Qt.Checked == self.isChecked())

	def onToggled(self, checked):
		for w in self._widgets:
			w.setEnabled(checked)