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

from __future__ import absolute_import
from builtins import object
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import *
from qgis.core import Qgis
from .analyses import SplitPolylinesAnalysis, CreateSegmentMapAnalysis, CreateJunctionsAnalysis, ReachAnalysis, NetworkIntegrationAnalysis, AngularIntegrationAnalysis, NetworkBetweennessAnalysis, AngularChoiceAnalysis, AttractionDistanceAnalysis, AttractionReachAnalysis, AttractionBetweennessAnalysis
from .model import QGISModel, Settings
from .ui import wizards
from . import APP_TITLE

MENU_TITLE = APP_TITLE

ENABLE_EXPERIMENTAL_ANALYSES = True

QGIS_ERROR_LEVEL_FROM_PSTA_LEVEL = [Qgis.Info, Qgis.Info, Qgis.Warning, Qgis.Critical]

class PSTPlugin(object):

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		self._actions = []
		self._pstalgo = None
		self._settings = Settings()
		self._settings.load()
		self._model = QGISModel()
		self._logHandle = None

	def initGui(self):
		self._actions = self.createActions()
		# Create menu
		for a in self._actions:
			self.iface.addPluginToVectorMenu(MENU_TITLE, a)

	def unload(self):
		# Remove menu
		for a in self._actions:
			self.iface.removePluginVectorMenu(MENU_TITLE, a)

	def createActions(self):
		ACTIONS = [
			('Split Polylines',        lambda : self.onAnalysis(wizards.SplitPolylinesWiz,        SplitPolylinesAnalysis), None),
			('Create Segment Map',     lambda : self.onAnalysis(wizards.CreateSegmentMapWiz,      CreateSegmentMapAnalysis), None),
			('Create Junctions',       lambda : self.onAnalysis(wizards.CreateJunctionsWiz,       CreateJunctionsAnalysis), None),
			None,
			('Reach',                  lambda : self.onAnalysis(wizards.ReachWiz,                 ReachAnalysis), None),
			('Network Integration',    lambda : self.onAnalysis(wizards.NetworkIntegrationWiz,    NetworkIntegrationAnalysis), None),
			('Angular Integration',    lambda : self.onAnalysis(wizards.AngularIntegrationWiz,    AngularIntegrationAnalysis), None),
			('Network Betweenness',    lambda : self.onAnalysis(wizards.NetworkBetweennessWiz,    NetworkBetweennessAnalysis), None),
			('Angular Choice',         lambda : self.onAnalysis(wizards.AngularChoiceWiz,         AngularChoiceAnalysis), None),
			('Attraction Distance',    lambda : self.onAnalysis(wizards.AttractionDistanceWiz,    AttractionDistanceAnalysis), None),
			('Attraction Reach',       lambda : self.onAnalysis(wizards.AttractionReachWiz,       AttractionReachAnalysis), None),
			('Attraction Betweenness', lambda : self.onAnalysis(wizards.AttractionBetweennessWiz, AttractionBetweennessAnalysis), None)
		]

		if ENABLE_EXPERIMENTAL_ANALYSES:
			from .analyses import SegmentGroupingAnalysis, SegmentGroupIntegrationAnalysis
			ACTIONS += [
				None,
				('Segment Grouping',          lambda : self.onAnalysis(wizards.SegmentGroupingWiz,         SegmentGroupingAnalysis),         None),
				('Segment Group Integration', lambda : self.onAnalysis(wizards.SegmentGroupIntegrationWiz, SegmentGroupIntegrationAnalysis), None),
			]

		actions = []
		for a in ACTIONS:
			act = None
			if a is None:
				act = QAction(self.iface.mainWindow())
				act.setSeparator(True)
			else:
				icon = QIcon(a[2]) if a[2] else None
				act = QAction(a[0], self.iface.mainWindow()) if icon is None else QAction(icon, a[0], self.iface.mainWindow())
				act.triggered.connect(a[1])
			actions.append(act)
		return actions

	@staticmethod
	def PSTALogCallback(level, domain, msg):
		title = APP_TITLE
		log_msg = msg
		if domain is not None:
			title += ' (%s)' % domain
			log_msg = "(%s) %s" % (domain, msg)
		QgsMessageLog.logMessage(log_msg, 'PST', QGIS_ERROR_LEVEL_FROM_PSTA_LEVEL[level])
		# Show popup
		if 3 == level:
			QMessageBox.critical(None, title, msg)
		elif 2 == level:
			QMessageBox.warning(None, title, msg)
		else:
			QMessageBox.information(None, title, msg)

	def initLog(self):
		if self._logHandle is None:
			import pstalgo
			self._logHandle = pstalgo.RegisterLogCallback(self.PSTALogCallback)

	def onAnalysis(self, wizard, analysis):
		def TaskFactory(props):
			self.initLog()
			return analysis(self._model, props)
		wiz = wizard(self.iface.mainWindow(), self._settings, self._model, TaskFactory)
		wiz.exec_()