# -*- coding: utf-8 -*-
"""
Compatibility shims for QGIS 3.x / 4.0 and Qt 5.15 / Qt 6.

Import version-independent constants from this module instead of
accessing QGIS or Qt enum values directly, which differ between
QGIS 3.x (Qt 5, PyQt5) and QGIS 4.0 (Qt 6, PyQt6).
"""

from qgis.core import Qgis, QgsWkbTypes
from qgis.PyQt.QtCore import QT_VERSION_STR, Qt
from qgis.PyQt.QtWidgets import QAbstractItemView, QDialogButtonBox

IS_QT6 = int(QT_VERSION_STR.split(".")[0]) >= 6

# ── Geometry type (QgsWkbTypes.PointGeometry → Qgis.GeometryType.Point) ──────
try:
    # QGIS 4.0+
    GEO_POINT = Qgis.GeometryType.Point
    GEO_LINE = Qgis.GeometryType.Line
    GEO_POLYGON = Qgis.GeometryType.Polygon
except AttributeError:
    # QGIS 3.x
    GEO_POINT = QgsWkbTypes.PointGeometry
    GEO_LINE = QgsWkbTypes.LineGeometry
    GEO_POLYGON = QgsWkbTypes.PolygonGeometry

# ── Layer type (QgsMapLayer.VectorLayer → Qgis.LayerType.Vector) ─────────────
try:
    # QGIS 4.0+
    LAYER_VECTOR = Qgis.LayerType.Vector
except AttributeError:
    # QGIS 3.x
    from qgis.core import QgsMapLayer

    LAYER_VECTOR = QgsMapLayer.VectorLayer

# ── Distance units (QgsUnitTypes.DistanceMeters → Qgis.DistanceUnit.Meters) ──
try:
    # QGIS 4.0+
    DIST_METERS = Qgis.DistanceUnit.Meters
    DIST_FEET = Qgis.DistanceUnit.Feet
    DIST_DEGREES = Qgis.DistanceUnit.Degrees
except AttributeError:
    # QGIS 3.x
    from qgis.core import QgsUnitTypes

    DIST_METERS = QgsUnitTypes.DistanceMeters
    DIST_FEET = QgsUnitTypes.DistanceFeet
    DIST_DEGREES = QgsUnitTypes.DistanceDegrees


def encodeDistanceUnit(unit):
    """Return a short string identifier for a distance unit.

    Wraps QgsUnitTypes.encodeUnit() with a fallback for QGIS 4.0
    in case the function signature changed.
    """
    from qgis.core import QgsUnitTypes

    try:
        return QgsUnitTypes.encodeUnit(unit)
    except Exception:
        return str(unit)


# ── Qt enum compatibility (Qt 5 flat enums → Qt 6 scoped enums) ───────────────
try:
    # Qt 6 / PyQt6 — enums are scoped
    ITEM_DATA_ROLE_USER = Qt.ItemDataRole.UserRole
    ITEM_DATA_ROLE_DISPLAY = Qt.ItemDataRole.DisplayRole
    CASE_INSENSITIVE = Qt.CaseSensitivity.CaseInsensitive
    ORIENTATION_HORIZONTAL = Qt.Orientation.Horizontal
    MATCH_FIXED_STRING = Qt.MatchFlag.MatchFixedString
    COLOR_YELLOW = Qt.GlobalColor.yellow
    COLOR_RED = Qt.GlobalColor.red
    COLOR_GREEN = Qt.GlobalColor.green
    COLOR_BLUE = Qt.GlobalColor.blue
    DOCK_RIGHT = Qt.DockWidgetArea.RightDockWidgetArea
    SELECTION_BEHAVIOR_ROWS = QAbstractItemView.SelectionBehavior.SelectRows
    SELECTION_MODE_SINGLE = QAbstractItemView.SelectionMode.SingleSelection
    SELECTION_MODE_EXTENDED = QAbstractItemView.SelectionMode.ExtendedSelection
    DIALOG_OK = QDialogButtonBox.StandardButton.Ok
    DIALOG_RESET = QDialogButtonBox.StandardButton.Reset
    DIALOG_HELP = QDialogButtonBox.StandardButton.Help
except AttributeError:
    # Qt 5 / PyQt5 — flat enums
    ITEM_DATA_ROLE_USER = Qt.UserRole
    ITEM_DATA_ROLE_DISPLAY = Qt.DisplayRole
    CASE_INSENSITIVE = Qt.CaseInsensitive
    ORIENTATION_HORIZONTAL = Qt.Horizontal
    MATCH_FIXED_STRING = Qt.MatchFixedString
    COLOR_YELLOW = Qt.yellow
    COLOR_RED = Qt.red
    COLOR_GREEN = Qt.green
    COLOR_BLUE = Qt.blue
    DOCK_RIGHT = Qt.RightDockWidgetArea
    SELECTION_BEHAVIOR_ROWS = QAbstractItemView.SelectRows
    SELECTION_MODE_SINGLE = QAbstractItemView.SingleSelection
    SELECTION_MODE_EXTENDED = QAbstractItemView.ExtendedSelection
    DIALOG_OK = QDialogButtonBox.Ok
    DIALOG_RESET = QDialogButtonBox.Reset
    DIALOG_HELP = QDialogButtonBox.Help

# ── QVariant.Type → QMetaType.Type (Qt 6 / PyQt6) ────────────────────────────
# In Qt 6, QVariant::Type was removed in favour of QMetaType::Type.
# PyQt6 exposes these as QMetaType.Type.<name>; PyQt5 exposes them as
# QVariant.<name>.  The integer values are identical, but the attribute names
# on the Python objects differ.
try:
    # PyQt6 / Qt 6
    from qgis.PyQt.QtCore import QMetaType

    QVARIANT_INT = QMetaType.Type.Int
    QVARIANT_UINT = QMetaType.Type.UInt
    QVARIANT_LONGLONG = QMetaType.Type.LongLong
    QVARIANT_ULONGLONG = QMetaType.Type.ULongLong
    QVARIANT_DOUBLE = QMetaType.Type.Double
    QVARIANT_STRING = QMetaType.Type.QString
    QVARIANT_BOOL = QMetaType.Type.Bool
except (ImportError, AttributeError):
    # PyQt5 / Qt 5 — QVariant.Type values
    from qgis.PyQt.QtCore import QVariant as _QVariant

    QVARIANT_INT = _QVariant.Int
    QVARIANT_UINT = _QVariant.UInt
    QVARIANT_LONGLONG = _QVariant.LongLong
    QVARIANT_ULONGLONG = _QVariant.ULongLong
    QVARIANT_DOUBLE = _QVariant.Double
    QVARIANT_STRING = _QVariant.String
    QVARIANT_BOOL = _QVariant.Bool

# Convenience list of numeric field types (replaces QVARIANT_NUMBER_TYPE_LIST)
QVARIANT_NUMBER_TYPES = {
    QVARIANT_INT,
    QVARIANT_UINT,
    QVARIANT_LONGLONG,
    QVARIANT_ULONGLONG,
    QVARIANT_DOUBLE,
}
