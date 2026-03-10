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

from ..compat import QVARIANT_STRING


class LrsErrorFields(QgsFields):
    def __init__(self):
        super(LrsErrorFields, self).__init__()

        fields = [
            QgsField(
                "error", QVARIANT_STRING, "string"
            ),  # error type, avoid 'type' which could be keyword
            QgsField("route", QVARIANT_STRING, "string"),
            QgsField("measure", QVARIANT_STRING, "string"),
        ]

        for field in fields:
            self.append(field)


LRS_ERROR_FIELDS = LrsErrorFields()
