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
    QgsGraduatedSymbolRenderer,
    QgsProviderRegistry,
    QgsRendererRange,
    QgsSymbol,
    QgsVectorLayer,
)
from qgis.PyQt.QtGui import QColor

from ..compat import COLOR_BLUE, COLOR_GREEN, COLOR_RED, GEO_LINE
from ..utils import crsString
from .lrsqualityfields import LRS_QUALITY_FIELDS


class LrsQualityLayer(QgsVectorLayer):
    def __init__(self, crs):
        uri = "LineString?crs=%s" % crsString(crs)
        provider = QgsProviderRegistry.instance().createProvider("memory", uri)
        provider.addAttributes(LRS_QUALITY_FIELDS.toList())
        uri = provider.dataSourceUri()
        super(LrsQualityLayer, self).__init__(uri, "LRS quality", "memory")

        # min, max, color, label
        styles = [
            [0, 10, QColor(COLOR_GREEN), "0 - 10 % error"],
            [10, 30, QColor(COLOR_BLUE), "10 - 30 % error"],
            [30, 1000000, QColor(COLOR_RED), "> 30 % error"],
        ]
        ranges = []
        for style in styles:
            symbol = QgsSymbol.defaultSymbol(GEO_LINE)
            symbol.setColor(style[2])
            range = QgsRendererRange(style[0], style[1], symbol, style[3])
            ranges.append(range)

        renderer = QgsGraduatedSymbolRenderer("err_perc", ranges)
        self.setRenderer(renderer)
