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

from qgis.core import QgsField, QgsFields

from ..compat import QVARIANT_DOUBLE, QVARIANT_STRING


class LrsQualityFields(QgsFields):
    def __init__(self):
        super(LrsQualityFields, self).__init__()

        fields = [
            QgsField("route", QVARIANT_STRING, "string"),
            QgsField("m_from", QVARIANT_DOUBLE, "double"),
            QgsField("m_to", QVARIANT_DOUBLE, "double"),
            QgsField("m_len", QVARIANT_DOUBLE, "double"),
            QgsField("len", QVARIANT_DOUBLE, "double"),
            QgsField("err_abs", QVARIANT_DOUBLE, "double"),
            QgsField("err_rel", QVARIANT_DOUBLE, "double"),
            QgsField("err_perc", QVARIANT_DOUBLE, "double"),  # relative in percents
        ]
        for field in fields:
            self.append(field)


LRS_QUALITY_FIELDS = LrsQualityFields()
