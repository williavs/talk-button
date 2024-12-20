import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QMessageBox, QTabWidget, QWidget,
    QPlainTextEdit
)
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    @classmethod
    def get_config_dir(cls):
        home = str(Path.home())
        config_dir = os.path.join(home, '.voice-prompt')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return config_dir

    @classmethod
    def get_api_key(cls):
        try:
            config_file = os.path.join(cls.get_config_dir(), 'config')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            return None
        return None

    @classmethod
    def get_system_prompt(cls):
        """Load the system prompt from config file."""
        try:
            prompt_file = os.path.join(cls.get_config_dir(), 'system_prompt')
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            return None
        return None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedWidth(600)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # API Key tab
        api_key_tab = QWidget()
        api_key_layout = QVBoxLayout()
        
        # API Key input
        api_key_label = QLabel("OpenAI API Key:")
        api_key_layout.addWidget(api_key_label)
        
        self.api_key_input = QLineEdit()
        current_api_key = self.get_api_key()
        if current_api_key:
            self.api_key_input.setText(current_api_key)
        api_key_layout.addWidget(self.api_key_input)
        
        # API Key button container
        api_button_layout = QHBoxLayout()
        
        # Save API button
        save_api_button = QPushButton("Save")
        save_api_button.clicked.connect(self.save_api_key)
        api_button_layout.addWidget(save_api_button)
        
        # Clear API button
        clear_button = QPushButton("Clear API Key")
        clear_button.clicked.connect(self.clear_api_key)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        api_button_layout.addWidget(clear_button)
        
        api_key_layout.addLayout(api_button_layout)
        api_key_layout.addStretch()
        api_key_tab.setLayout(api_key_layout)
        
        # System Prompt tab
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout()
        
        prompt_label = QLabel("System Prompt:")
        prompt_label.setToolTip("This prompt guides how the model processes your transcribed text.")
        prompt_layout.addWidget(prompt_label)
        
        self.prompt_input = QPlainTextEdit()
        self.prompt_input.setPlaceholderText("""Enter your system prompt here. Example:
You are a helpful assistant. Your task is to correct any spelling discrepancies 
in the transcribed text. Add necessary punctuation such as periods, commas, 
and capitalization. Make the text more readable while preserving its original meaning.""")
        
        current_prompt = self.get_system_prompt()
        if current_prompt:
            self.prompt_input.setPlainText(current_prompt)
        else:
            # Set default prompt
            default_prompt = """You are a helpful assistant. Your task is to correct any spelling discrepancies 
in the transcribed text. Add necessary punctuation such as periods, commas, 
and capitalization. Make the text more readable while preserving its original meaning. 
Use only the context provided."""
            self.prompt_input.setPlainText(default_prompt)
        
        prompt_layout.addWidget(self.prompt_input)
        
        # Prompt button container
        prompt_button_layout = QHBoxLayout()
        
        # Save prompt button
        save_prompt_button = QPushButton("Save Prompt")
        save_prompt_button.clicked.connect(self.save_prompt)
        prompt_button_layout.addWidget(save_prompt_button)
        
        # Reset prompt button
        reset_prompt_button = QPushButton("Reset to Default")
        reset_prompt_button.clicked.connect(self.reset_prompt)
        prompt_button_layout.addWidget(reset_prompt_button)
        
        prompt_layout.addLayout(prompt_button_layout)
        prompt_tab.setLayout(prompt_layout)
        
        # Add tabs
        self.tab_widget.addTab(api_key_tab, "API Key")
        self.tab_widget.addTab(prompt_tab, "System Prompt")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def save_api_key(self):
        """Save the API key to config file."""
        api_key = self.api_key_input.text().strip()
        try:
            config_file = os.path.join(self.get_config_dir(), 'config')
            with open(config_file, 'w') as f:
                f.write(api_key)
            self.accept()
        except Exception as e:
            print(f"Error saving API key: {e}")
            self.reject()

    def save_prompt(self):
        """Save the system prompt to config file."""
        prompt = self.prompt_input.toPlainText().strip()
        try:
            prompt_file = os.path.join(self.get_config_dir(), 'system_prompt')
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            # Show success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("System prompt saved successfully")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
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
                    border-radius: 3px;
                    padding: 5px 15px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                    border: 2px solid #666;
                }
            """)
            msg.exec()
            
            # Close the dialog
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save system prompt: {str(e)}")

    def reset_prompt(self):
        """Reset the system prompt to default."""
        default_prompt = """You are a helpful assistant. Your task is to correct any spelling discrepancies 
in the transcribed text. Add necessary punctuation such as periods, commas, 
and capitalization. Make the text more readable while preserving its original meaning. 
Use only the context provided."""
        self.prompt_input.setPlainText(default_prompt)
            
    def clear_api_key(self):
        """Clear the API key from local storage."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Clear API Key")
        msg.setText("Are you sure you want to clear the API key?")
        msg.setInformativeText("This action cannot be undone.")
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
                border-radius: 3px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 2px solid #666;
            }
        """)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            try:
                config_file = os.path.join(self.get_config_dir(), 'config')
                if os.path.exists(config_file):
                    os.remove(config_file)
                    self.api_key_input.clear()
                    QMessageBox.information(self, "Success", "API key cleared successfully")
                    if self.parent():
                        self.parent().transcription_service.clear_api_key()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear API key: {str(e)}") 