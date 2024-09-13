# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
import sys
import pytest
import json
from pathlib import Path
from dataclasses import fields


sys.path.append(os.path.abspath("."))
from MagInkCalWeekly.config import CalendarConfig

# -----------------------------------------------------------------------------
# Test data
# -----------------------------------------------------------------------------
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
  "imageWidth": 984,
  "imageHeight": 1304,
  "rotateAngle": 270,
  "is24h": False,
  "calendars": [
    "primary"
  ]
}
sample_json = json.dumps(sample_data)

# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
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
    config = CalendarConfig.from_json(sample_json)
    for field in fields(config):
        value = getattr(config, field.name)
        assert value == sample_data[field.name]

def test_from_file(mock_json_file):
    # Test the from_file method
    config = CalendarConfig.from_file(mock_json_file)
    for field in fields(config):
        value = getattr(config, field.name)
        assert value == sample_data[field.name]

def test_to_json():
    # Test the to_json method
    config = CalendarConfig.from_json(sample_json)
    json_output = config.to_json()
    assert json.loads(json_output) == json.loads(sample_json)

def test_print_info(capfd):
    # Test the print_info method
    config = CalendarConfig.from_json(sample_json)
    config.print_info()

    captured = capfd.readouterr()
    for field in fields(config):
        value = getattr(config, field.name)
        assert value == sample_data[field.name]
        assert f"{field.name}: {value}" in captured.out