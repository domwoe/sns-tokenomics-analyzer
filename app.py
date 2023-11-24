#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 11:38:18 2023

@author: bjoernassmann
"""

from dash import Dash
import callbacks
import layout
from scenario_computation import get_scenarios
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys


class YamlFileChangeHandler(FileSystemEventHandler):
    """Handles the YAML file change event."""
    def __init__(self, filename, start_script):
        self.filename = filename
        self.start_script = start_script

    def on_modified(self, event):
        if event.src_path == self.filename:
            print(f"{self.filename} has been modified. Restarting the server...")
            os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == '__main__':
    # Define the path to your YAML file and your Dash app script
    yaml_file_path = 'sns_init.yaml'
    app_script = 'app.py'

    # Set up file observer
    event_handler = YamlFileChangeHandler(yaml_file_path, app_script)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(yaml_file_path), recursive=False)
    observer.start()

    try:
        app = Dash(__name__)
        scenarios = get_scenarios()
        app.layout = layout.create_layout(scenarios)
        callbacks.register_callbacks(app, scenarios)
        app.run_server(debug=True, port=8051)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
