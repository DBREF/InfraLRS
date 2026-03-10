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

from qgis.core import QgsProject
from qgis.PyQt.QtGui import QStandardItem

from ..lrs.compat import ITEM_DATA_ROLE_USER
from ..lrs.utils import PROJECT_PLUGIN_NAME, LrsUnits
from .lrscombomanagerbase import LrsComboManagerBase


class LrsUnitComboManager(LrsComboManagerBase):
    def __init__(self, comboOrList, **kwargs):
        kwargs["sort"] = False
        super(LrsUnitComboManager, self).__init__(comboOrList, **kwargs)

        for unit in [LrsUnits.METER, LrsUnits.KILOMETER, LrsUnits.FEET, LrsUnits.MILE]:
            item = QStandardItem(LrsUnits.unitName(unit))
            item.setData(unit, ITEM_DATA_ROLE_USER)
            self.model.appendRow(item)

        self.reset()

    def unit(self):
        idx = self.comboList[0].currentIndex()
        if idx != -1:
            return self.comboList[0].itemData(idx, ITEM_DATA_ROLE_USER)
        return LrsUnits.UNKNOWN

    def writeToProject(self):
        name = LrsUnits.unitName(self.unit())
        QgsProject.instance().writeEntry(PROJECT_PLUGIN_NAME, self.settingsName, name)

    def readFromProject(self):
        name = QgsProject.instance().readEntry(PROJECT_PLUGIN_NAME, self.settingsName)[
            0
        ]

        unit = LrsUnits.unitFromName(name)
        idx = self.comboList[0].findData(unit, ITEM_DATA_ROLE_USER)
        # debug( "readFromProject settingsName = %s name = %s idx = %s" % ( self.settingsName, name, idx) )
        if idx != -1:
            for combo in self.comboList:
                combo.setCurrentIndex(idx)
        else:
            self.reset()
