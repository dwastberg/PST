/*
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
*/

#pragma once

#include <pstalgo/pstalgo.h>

struct SCreateSegmentMapDesc
{
	SCreateSegmentMapDesc() : m_Version(VERSION) {}

	// Version
	static const unsigned int VERSION = 1;
	unsigned int m_Version;

	// Thresholds
	float m_Snap;
	float m_ExtrudeCut;
	float m_MinTail;
	float m_Min3NodeColinearDeviation;

	// Polylines
	double*      m_PolyCoords;
	int*         m_PolySections;
	unsigned int m_PolyCoordCount;
	unsigned int m_PolySectionCount;
	unsigned int m_PolyCount;

	// Unlinks
	double*      m_UnlinkCoords;
	unsigned int m_UnlinkCount;

	// Progress Callback
	FPSTAProgressCallback m_ProgressCallback;
	void*                 m_ProgressCallbackUser;
};

struct SCreateSegmentMapRes
{
	SCreateSegmentMapRes() : m_Version(VERSION) {}

	// Version
	static const unsigned int VERSION = 1;
	unsigned int m_Version;

	// Segments
	double*       m_SegmentCoords;
	unsigned int* m_Segments;  // (P0, P1, Base)
	unsigned int  m_SegmentCount;
};

PSTADllExport IPSTAlgo* PSTACreateSegmentMap(const SCreateSegmentMapDesc* desc, SCreateSegmentMapRes* res);