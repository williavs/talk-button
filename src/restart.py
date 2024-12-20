#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import signal

def restart_app():
    """
    Restart the application by starting a new instance and terminating the current one.
    """
    # Get the path to the main script
    main_script = os.path.join(os.path.dirname(__file__), 'main.py')
    
    # Start the new instance
    subprocess.Popen([sys.executable, main_script])
    
    # Signal the parent process to terminate
    os.kill(os.getppid(), signal.SIGTERM)

if __name__ == '__main__':
    restart_app() 