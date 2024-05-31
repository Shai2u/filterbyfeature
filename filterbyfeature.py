"""
****************************************************************
 Filter by feature
                              -------------------
        begin                : 2024-05-31
        copyright            : Shai Sussman
        email                : shai.sussman@gmail.com
****************************************************************
"""

from __future__ import absolute_import
import os.path
from qgis.PyQt.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .filter_by_feature_dialog import FilterByFeatureDialog


class filterByFeature:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.actions = []
        self.menu = self.tr(u'&FilterByFeature')

        self.toolbar = self.iface.addToolBar(u'FilterByFeature')
        self.toolbar.setObjectName(u'FilterByFeature')
        
        self.pluginIsActive = False
        self.dockwidget = None

    def tr(self, message):
        """
        Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FilterByFeature', message)

    # noinspection PyPep8Naming
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        """Add a toolbar icon to the toolbar."""
        icon = QIcon(self.icon_path)
        self.panelAction = QAction(icon, self.tr(u'FilterByFeature'), self.iface.mainWindow())
        self.panelAction.triggered.connect(self.run)
        self.panelAction.setCheckable(True)
        self.panelAction.setEnabled(True)

        self.toolbar.addAction(self.panelAction)
        self.iface.addPluginToMenu(self.menu, self.panelAction)
        self.actions.append(self.panelAction)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&FilterByFeature'), action)
            self.iface.removeToolBarIcon(action)

    def widgetVisibilityChanged(self, visible: bool) -> None:
        self.panelAction.setChecked(visible)

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        self.pluginIsActive = False

    def run(self, checked: bool):
        if not self.pluginIsActive:
            self.pluginIsActive = True
            if self.dockwidget is None:
                self.dockwidget = FilterByFeatureDialog(self.iface)
            self.dockwidget.visibilityChanged.connect(self.widgetVisibilityChanged)

            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            self.iface.addDockWidget(
                area=Qt.LeftDockWidgetArea,
                dockwidget=self.dockwidget,
            )
            
        # The triggered signal includes a bool 
        # that indicates whether the button was checked or unchecked
        self.dockwidget.setVisible(checked)
