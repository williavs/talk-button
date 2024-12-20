from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QGraphicsDropShadowEffect, QFrame, QApplication,
    QMessageBox, QDialog
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, 
    pyqtSlot, QTimer, QSize, QPoint, QObject, pyqtProperty
)
from PyQt6.QtGui import QPalette, QColor, QIcon, QPainter, QPainterPath, QFont, QKeySequence, QShortcut
import sys
import os
import pyperclip
from pathlib import Path
import threading

from .components.circle_button import CircleButton
from .components.system_tray import SystemTray
from .components.settings_dialog import SettingsDialog
from ..core.audio_recorder import AudioRecorder
from ..core.transcription import TranscriptionService

class PulseEffect(QObject):
    def __init__(self, target):
        super().__init__()
        self._target = target
        self._radius = 30
        
        self.animation = QPropertyAnimation(self, b"radius")
        self.animation.setDuration(1000)
        self.animation.setStartValue(30)
        self.animation.setEndValue(50)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setLoopCount(-1)
        
    @pyqtProperty(int)
    def radius(self):
        return self._radius
        
    @radius.setter
    def radius(self, value):
        self._radius = value
        if self._target.graphicsEffect():
            self._target.graphicsEffect().setBlurRadius(value)

class FloatingText(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        # Create text edit
        self.text_edit = QLabel(self)
        self.text_edit.setWordWrap(True)
        self.text_edit.setMinimumWidth(250)
        self.text_edit.setMaximumWidth(400)
        self.text_edit.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse | 
            Qt.TextInteractionFlag.TextEditable
        )
        
        # Create confirmation label
        self.confirmation = QLabel(self)
        self.confirmation.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 12px;
                padding: 4px;
                background: transparent;
            }
        """)
        self.confirmation.hide()
        
        # Modern font setup
        font = QFont('Inter', 13)
        font.setWeight(QFont.Weight.Normal)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.5)
        self.text_edit.setFont(font)
        
        self.text_edit.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
                padding: 8px;
                line-height: 145%;
                min-height: 50px;
            }
        """)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.confirmation)
        
        # Style the frame
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 0.92);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Enhanced drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.hide()
        
    def showText(self, text: str):
        self.text_edit.setText(text)
        self.confirmation.setText("✓ Copied to clipboard")
        self.confirmation.show()
        self.adjustSize()
        
        # Position above the button
        parent_rect = self.parent().rect()
        button_pos = self.parent().record_button.pos()
        
        # Calculate position ensuring text is visible
        x_pos = button_pos.x() + (self.parent().record_button.width() - self.width()) // 2
        y_pos = max(20, button_pos.y() - self.height() - 20)
        
        self.move(x_pos, y_pos)
        self.show()
        # Hide after 10 seconds
        QTimer.singleShot(10000, self.hide)

class MainWindow(QMainWindow):
    STATE_IDLE = "idle"
    STATE_RECORDING = "recording"
    STATE_PROCESSING = "processing"
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Prompt")
        self.audio_recorder = AudioRecorder()
        self.transcription_service = TranscriptionService()
        self.current_state = self.STATE_IDLE
        self.last_click_pos = None
        self.is_dragging = False
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_system_tray()
        
        # Check for API key on startup
        if not self.transcription_service.api_key:
            QTimer.singleShot(500, self.show_api_key_warning)
        
        self.setMinimumSize(300, 500)
        self.resize(300, 500)
        self.center()
        
        # Remove window frame, set transparency, and make window stay on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 100, 20, 20)
        
        # Main circle button
        self.record_button = CircleButton(200, self)
        self.record_button.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Floating text display
        self.floating_text = FloatingText(self)
        
        # Add glow effect
        self.update_glow(self.STATE_IDLE)
        
    def setup_shortcuts(self):
        quit_shortcut = QShortcut(QKeySequence('Esc'), self)
        quit_shortcut.activated.connect(self.close)
        
        record_shortcut = QShortcut(QKeySequence('Space'), self)
        record_shortcut.activated.connect(self.toggle_recording)
        
        hide_shortcut = QShortcut(QKeySequence('Alt+H'), self)
        hide_shortcut.activated.connect(self.toggle_visibility)
        
    def setup_system_tray(self):
        self.system_tray = SystemTray(self)
        
    def show_api_key_warning(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("API Key Required")
        msg.setText("OpenAI API Key is missing")
        msg.setInformativeText("Would you like to set it up now?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: white;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 2px solid #666;
            }
        """)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            dialog = SettingsDialog(self)
            result = dialog.exec()
            
            # Update state after settings dialog closes
            if result == QDialog.DialogCode.Accepted:
                # Reload API key and system prompt
                self.transcription_service._load_api_key()
                self.set_state(self.STATE_IDLE)
            
    def set_state(self, state: str, message: str = ""):
        self.current_state = state
        self.record_button.setEnabled(state != self.STATE_PROCESSING)
        self.update_glow(state)
        
        # Update button state text
        if state == self.STATE_IDLE:
            api_key = self.transcription_service.load_api_key()
            if not api_key:
                self.record_button.update_state("api_missing")
                self.record_button.setEnabled(False)
            else:
                self.record_button.update_state("ready")
        elif state == self.STATE_RECORDING:
            self.record_button.update_state("recording")
        elif state == self.STATE_PROCESSING:
            self.record_button.update_state("processing")
            
    def toggle_recording(self):
        if not self.transcription_service.api_key:
            dialog = SettingsDialog(self)
            dialog.exec()
            self.set_state(self.STATE_IDLE)
            return
            
        if self.current_state == self.STATE_IDLE:
            self.start_recording()
        elif self.current_state == self.STATE_RECORDING:
            self.stop_recording()
    
    def start_recording(self):
        self.audio_recorder.start_recording()
        self.set_state(self.STATE_RECORDING)
        
    def stop_recording(self):
        self.set_state(self.STATE_PROCESSING)
        audio_path = self.audio_recorder.stop_recording()
        
        if audio_path:
            QTimer.singleShot(100, lambda: self.process_recording(audio_path))
    
    def process_recording(self, audio_path: Path):
        try:
            transcript = self.transcription_service.transcribe_audio(audio_path)
            
            if transcript:
                self.floating_text.showText(transcript)
                pyperclip.copy(transcript)
            
            audio_path.unlink()
            
        except Exception as e:
            self.floating_text.showText(f"Error: {str(e)}")
            
        finally:
            self.set_state(self.STATE_IDLE)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            self.window_pos = self.pos()
            self.is_dragging = True
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if (event.globalPosition().toPoint() - self.drag_position).manhattanLength() < 3:
                self.toggle_recording()
            self.is_dragging = False
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.window_pos + delta)
            event.accept()

    def changeEvent(self, event):
        if event.type() == 105:  # WindowStateChange event type
            if self.windowState() & Qt.WindowState.WindowMinimized:
                event.ignore()
                self.hide()
                self.system_tray.toggle_action.setText("Show")
        super().changeEvent(event)
    
    def closeEvent(self, event):
        self.system_tray.hide()
        event.accept()
    
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def toggle_visibility(self):
        """Toggle the window visibility."""
        if self.isVisible():
            self.hide()
            if hasattr(self, 'system_tray'):
                self.system_tray.toggle_action.setText("Show")
        else:
            self.show()
            if hasattr(self, 'system_tray'):
                self.system_tray.toggle_action.setText("Hide")
    
    def update_glow(self, state: str):
        """Update the glow effect based on the current state."""
        if not hasattr(self, 'record_button'):
            return
            
        glow = QGraphicsDropShadowEffect(self)
        
        if state == self.STATE_IDLE:
            color = QColor(0, 122, 255)  # Blue
        elif state == self.STATE_RECORDING:
            color = QColor(255, 59, 48)  # Red
        else:  # Processing
            color = QColor(255, 204, 0)  # Yellow
            
        glow.setColor(color)
        glow.setBlurRadius(30)
        glow.setOffset(0)
        
        self.record_button.setGraphicsEffect(glow)
        
        # Start pulsing animation for recording state
        if hasattr(self, 'pulse_effect'):
            self.pulse_effect.animation.stop()
            
        if state == self.STATE_RECORDING:
            self.pulse_effect = PulseEffect(self.record_button)
            self.pulse_effect.animation.start()
    