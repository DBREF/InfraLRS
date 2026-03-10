# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LrsDockWidget
                                 A QGIS plugin
 Linear reference system builder and editor
                             -------------------
        begin                : 2017-5-20
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
    QgsFeature,
    QgsField,
    QgsProject,
    QgsProviderRegistry,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QObject

from .compat import (
    QVARIANT_DOUBLE,
    QVARIANT_INT,
    QVARIANT_LONGLONG,
    QVARIANT_UINT,
    QVARIANT_ULONGLONG,
)
from .utils import crsString


# Write Lrs to memory output layer
class LrsOutput(QObject):
    def __init__(self, iface, lrs, showProgressFunction):
        # debug( "LrsOutput.__init__")
        self.iface = iface
        self.lrs = lrs  # Lrs object
        self.showProgressFunction = showProgressFunction

    def output(self, outputName):
        # geometryType = "MultiLineStringM"
        geometryType = "LineStringM"
        uri = geometryType
        uri += "?crs=%s" % crsString(
            self.iface.mapCanvas().mapSettings().destinationCrs()
        )
        provider = QgsProviderRegistry.instance().createProvider("memory", uri)

        routeField = self.lrs.routeField
        routeFieldName = routeField.name()
        routeFieldType = "string"
        if (
            routeField.type() == QVARIANT_INT
            or routeField.type() == QVARIANT_UINT
            or routeField.type() == QVARIANT_LONGLONG
            or routeField.type() == QVARIANT_ULONGLONG
        ):
            routeFieldType = "int"
        elif routeField.type() == QVARIANT_DOUBLE:
            routeFieldType = "double"

        provider.addAttributes(
            [
                QgsField(routeFieldName, routeField.type(), routeFieldType),
                QgsField("m_from", QVARIANT_DOUBLE, "double"),
                QgsField("m_to", QVARIANT_DOUBLE, "double"),
            ]
        )
        uri = provider.dataSourceUri()
        # debug('uri: %s' % uri)

        outputLayer = QgsVectorLayer(uri, outputName, "memory")
        outputFeatures = []

        total = len(self.lrs.getParts())
        count = 0
        for part in self.lrs.getParts():
            percent = 100 * count / total
            self.showProgressFunction("Exporting features", percent)
            count += 1
            if not part.records:
                continue
            geo = part.getGeometryWithMeasures()
            if not geo:
                continue

            if (
                routeField.type() == QVARIANT_INT
                or routeField.type() == QVARIANT_DOUBLE
            ):
                routeVal = part.routeId
            else:
                routeVal = "%s" % part.routeId

            outputFeature = QgsFeature(
                outputLayer.fields()
            )  # fields must exist during feature life!
            outputFeature.setGeometry(geo)
            outputFeature[routeFieldName] = routeVal
            outputFeature["m_from"] = part.milestoneMeasureFrom()
            outputFeature["m_to"] = part.milestoneMeasureTo()

            outputFeatures.append(outputFeature)

        outputLayer.dataProvider().addFeatures(outputFeatures)

        QgsProject.instance().addMapLayers(
            [
                outputLayer,
            ]
        )
