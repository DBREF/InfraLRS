# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LrsPlugin
                                 A QGIS plugin
 Linear reference system builder and editor
                              -------------------
        begin                : 2017-5-29
        copyright            : (C) 2017 by Radim Blažek
        email                : radim.blazek@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import (
    QgsCoordinateTransform,
    QgsGeometry,
    QgsProject,
    QgsRectangle,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.gui import QgsHighlight
from qgis.PyQt.QtCore import Qt

from ..utils import crsString, getProjectCrs, isProjectCrsEnabled


# Highlight, zoom errors
class LrsErrorVisualizer(object):
    def __init__(self, mapCanvas):
        self.errorHighlight = None
        self.mapCanvas = mapCanvas

    def __del__(self):
        if self.errorHighlight:
            del self.errorHighlight

    def clearHighlight(self):
        if self.errorHighlight:
            del self.errorHighlight
            self.errorHighlight = None

    def highlight(self, error, crs):
        self.clearHighlight()
        if not error:
            return

        # QgsHighlight does reprojection from layer CRS
        layer = QgsVectorLayer(
            "Point?crs=" + crsString(crs), "LRS error highlight", "memory"
        )
        self.errorHighlight = QgsHighlight(self.mapCanvas, error.geo, layer)
        # highlight point size is hardcoded in QgsHighlight
        self.errorHighlight.setWidth(2)
        self.errorHighlight.setColor(Qt.yellow)
        self.errorHighlight.show()

    def zoom(self, error, crs):
        if not error:
            return
        geo = error.geo
        if isProjectCrsEnabled() and getProjectCrs() != crs:
            geo = QgsGeometry(error.geo)
            transform = QgsCoordinateTransform(
                crs, QgsProject().instance().crs(), QgsProject.instance()
            )
            geo.transform(transform)

        if geo.type() == QgsWkbTypes.PointGeometry:
            p = geo.asPoint()
            bufferCrs = getProjectCrs() if isProjectCrsEnabled() else crs
            b = 2000 if not bufferCrs.isGeographic() else 2000 / 100000  # buffer
            extent = QgsRectangle(p.x() - b, p.y() - b, p.x() + b, p.y() + b)
        else:  # line
            extent = geo.boundingBox()
            extent.scale(2)
        self.mapCanvas.setExtent(extent)
        self.mapCanvas.refresh()
