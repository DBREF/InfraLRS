# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LrsSelectionDialog
                                 A QGIS plugin
 Linear reference system builder and editor
                             -------------------
        begin                : 2013-10-02
        copyright            : (C) 2013 by Radim Blažek
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

from qgis.core import NULL
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QTableWidgetSelectionRange,
)

from ..lrs.compat import ITEM_DATA_ROLE_USER, SELECTION_MODE_EXTENDED
from .ui_selectiondialog import Ui_LrsSelectionDialog


class LrsSelectionDialog(QDialog, Ui_LrsSelectionDialog):
    def __init__(self, parent=None):
        # debug( "LrsDockWidget.__init__")

        super(LrsSelectionDialog, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)

        # self.model =

        # self.proxy = QSortFilterProxyModel()
        # self.proxy.setFilterKeyColumn(0)
        # self.proxy.setFilterCaseSensitivity( Qt.CaseInsensitive )
        # self.proxy.setSourceModel( self.model )

        self.tableWidget.insertColumn(0)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Route"))
        self.tableWidget.setSelectionMode(SELECTION_MODE_EXTENDED)

    # select is list of values to be selected
    def load(self, layer, fieldName, select):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        if not layer or not fieldName:
            return

        field = layer.fields().field(fieldName)
        if not field:
            return

        values = set()
        for feature in layer.getFeatures():
            value = feature[fieldName]
            values.add(value)

        if field.type() == QVariant.String:
            values = sorted(values, key=lambda s: s.lower() if s != NULL else "")
        else:
            values = sorted(values)

        for i in range(len(values)):
            strValue = "%s" % values[i]
            item = QTableWidgetItem(strValue)
            item.setData(ITEM_DATA_ROLE_USER, values[i])
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, item)
            if strValue in select:
                self.tableWidget.setRangeSelected(
                    QTableWidgetSelectionRange(i, 0, i, 0), True
                )

    def selected(self):
        selected = []
        for item in self.tableWidget.selectedItems():
            selected.append(item.data(ITEM_DATA_ROLE_USER))
        return selected
