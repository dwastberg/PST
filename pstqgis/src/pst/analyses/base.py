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


# Delegate interface, dummy class
from builtins import object
class AnalysisDelegate(object):
	def setProgress(self, progress):
		pass
	def setStatus(self, text):
		pass
	def getCancel(self):
		return False


class BaseAnalysis(object):
	def __init__(self):
		self._want_cancel = False
		self._error = None

	def run(self, delegate):
		pass


class AnalysisException(Exception):
	def __init__(self, text):
		Exception.__init__(self, text)