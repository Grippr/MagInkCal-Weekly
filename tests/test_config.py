# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
import sys
import pytest
import json5 as json
from pathlib import Path
from dataclasses import fields
import logging


sys.path.append(os.path.abspath("."))
from MagInkCalWeekly.config import ConfigInfo

logging.basicConfig(level=logging.DEBUG)

# -----------------------------------------------------------------------------
# Test data
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_calendar_image_filename(tmp_path):
    file_path = tmp_path / "calendar_image.png"
    return file_path
calendar_path = str(mock_calendar_image_filename)

# Sample data 
sample_data = {
  "displayTZ": "EST",
  "thresholdHours": 24,
  "maxEventsPerDay": 3,
  "isDisplayToScreen": False,
  "isShutdownOnComplete": False,
  "batteryDisplayMode": 1,
  "weekStartDay": 6,
  "dayOfWeekText": ["M", "T", "W", "T", "F", "S", "S"],
  "screenWidth": 1304,
  "screenHeight": 984,
  "rotateAngle": 270,
  "is24h": False,
  "privateDirectory": "./private",
  "credentialsFileName": "credentials.json",
  "tokenFileName": "token.pickle",
  "calendars": ["primary"],
  "calendarImagePath": calendar_path,
  "numWeeks": 4
}

sample_json = json.dumps(sample_data)

@pytest.fixture
def mock_json_file(tmp_path):
    file_path = tmp_path / "config.json"
    file_path.write_text(sample_json)
    return file_path


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_from_json():
    # Test the from_json method
    config = ConfigInfo.from_json(sample_json)
    for field in fields(config):
        value = getattr(config, field.name)
        assert value == sample_data[field.name]

def test_from_file(mock_json_file):
    # Test the from_file method
    config = ConfigInfo.from_file(mock_json_file)
    for field in fields(config):
        value = getattr(config, field.name)
        assert value == sample_data[field.name]

def test_to_json():
    # Test the to_json method
    config = ConfigInfo.from_json(sample_json)
    json_output = config.to_json()
    assert json.loads(json_output) == json.loads(sample_json)

def test_log_info(capfd):
    # Test the log_info method
    config = ConfigInfo.from_json(sample_json)
    config.log_info()