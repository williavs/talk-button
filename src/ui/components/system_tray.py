from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt, QSize, QPoint
import os
import sys
import subprocess
from .settings_dialog import SettingsDialog
from .about_dialog import AboutDialog

class SystemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window_visible = True  # Track window visibility state
        self.setup_icon()
        self.setup_menu()
        self.activated.connect(self.on_tray_activated)
        self.show()

    def setup_icon(self):
        """Create a simple circle icon."""
        size = 32
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw a blue circle
        painter.setBrush(Qt.GlobalColor.blue)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(2, 2, size-4, size-4)
        painter.end()
        
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setToolTip('Voice Prompt')

    def setup_menu(self):
        """Setup the system tray menu."""
        self.menu = QMenu()
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3f3f3f;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3f3f3f;
            }
            QMenu::item:checked {
                background-color: #1e88e5;
            }
            QMenu::separator {
                height: 1px;
                background: #3f3f3f;
                margin: 5px 0px;
            }
        """)
        
        # Show/Hide action
        self.toggle_action = self.menu.addAction("Hide")
        self.toggle_action.triggered.connect(self.toggle_window)
        
        self.menu.addSeparator()
        
        # Always on top action
        self.always_on_top_action = self.menu.addAction("Always on Top")
        self.always_on_top_action.setCheckable(True)
        self.always_on_top_action.setChecked(True)  # Default to on
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        
        self.menu.addSeparator()
        
        # Record action
        record_action = self.menu.addAction("Record")
        record_action.triggered.connect(lambda: self.parent().toggle_recording())
        
        self.menu.addSeparator()
        
        # Settings action
        settings_action = self.menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings)
        
        self.menu.addSeparator()
        
        # About action
        about_action = self.menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
        self.menu.addSeparator()
        
        # Restart action
        restart_action = self.menu.addAction("Restart")
        restart_action.triggered.connect(self.restart_application)
        
        self.menu.addSeparator()
        
        # Quit action
        quit_action = self.menu.addAction("Quit")
        quit_action.triggered.connect(self.parent().close)
        
        self.setContextMenu(self.menu)
        
        # Connect menu signals
        self.menu.aboutToShow.connect(self.on_menu_about_to_show)
        self.menu.aboutToHide.connect(self.on_menu_about_to_hide)
        
    def on_menu_about_to_show(self):
        """Ensure window is visible when menu is shown."""
        # Store the current visibility state
        self.was_visible = self.parent().isVisible()
        # Show window while menu is open
        self.parent().show()
        self.parent().activateWindow()
        
    def on_menu_about_to_hide(self):
        """Restore window visibility state after menu is closed."""
        # Only hide if it wasn't visible before and isn't meant to be visible
        if not self.was_visible and not self.window_visible:
            self.parent().hide()

    def show_settings(self):
        """Show the settings dialog."""
        # Store current visibility state
        was_visible = self.parent().isVisible()
        
        # Ensure window is visible while settings dialog is open
        self.parent().show()
        self.parent().activateWindow()
        
        # Show settings dialog
        dialog = SettingsDialog(self.parent())
        result = dialog.exec()
        
        if result == dialog.DialogCode.Accepted:  # If user clicked Save or applied changes
            # Reload API key and system prompt
            self.parent().transcription_service._load_api_key()
            # Update window state
            self.parent().set_state(self.parent().STATE_IDLE)
        else:
            # Restore window visibility state if dialog was cancelled
            if not was_visible and not self.window_visible:
                self.parent().hide()

    def show_about(self):
        """Show the about dialog."""
        # Store current visibility state
        was_visible = self.parent().isVisible()
        
        # Ensure window is visible while about dialog is open
        self.parent().show()
        self.parent().activateWindow()
        
        # Show about dialog
        dialog = AboutDialog(self.parent())
        dialog.exec()
        
        # Restore window visibility state
        if not was_visible and not self.window_visible:
            self.parent().hide()

    def toggle_window(self):
        """Toggle the main window visibility."""
        self.window_visible = not self.window_visible
        
        if self.window_visible:
            self.parent().show()
            self.parent().activateWindow()
            self.toggle_action.setText("Hide")
        else:
            self.parent().hide()
            self.toggle_action.setText("Show")

    def restart_application(self):
        """Restart the application."""
        try:
            # Get the paths
            python = sys.executable
            main_script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'main.py')
            
            # Start new instance
            subprocess.Popen([python, main_script])
            
            # Close current instance
            self.parent().close()
            
        except Exception as e:
            print(f"Error restarting application: {e}")

    def on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_window()
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # Show menu slightly above tray icon
            menu_pos = self.geometry().topLeft()
            menu_pos.setY(menu_pos.y() - self.menu.sizeHint().height())
            self.menu.popup(menu_pos)

    def toggle_always_on_top(self, checked: bool):
        """Toggle the always-on-top state of the main window."""
        window = self.parent()
        flags = window.windowFlags()
        
        if checked:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
            
        # Re-apply window flags
        window.setWindowFlags(flags)
        
        # Show window if it was visible
        if window.isVisible():
            window.show()
            window.activateWindow()