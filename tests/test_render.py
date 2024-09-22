import pytest
from unittest.mock import MagicMock
import os
import sys

sys.path.append(os.path.abspath("."))
from raspaglance.render.render import RenderHelper
from raspaglance.config.config_info import ConfigInfo
from raspaglance.gcal.calendar_info import CalendarInfo
from PIL import Image
import datetime as dt

@pytest.fixture
def config():
    return ConfigInfo(
        maxEventsPerDay=5,
        isDisplayToScreen=True,
        isShutdownOnComplete=False,
        batteryDisplayMode=1,
        weekStartDay=0,
        dayOfWeekText=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        screenWidth=800,
        screenHeight=600,
        rotateAngle=0,
        numWeeks=4,
        is24h=True,
        calendarImagePath="path/to/image",
        displayTZ="US/Eastern",
        thresholdHours=24,
        calendars=["primary"],
        privateDirectory="path/to/private",
        credentialsFileName="credentials.json",
        tokenFileName="token.json",
    )

@pytest.fixture
def cal_info():
    ret = CalendarInfo()
    ret.currDate=dt.date(2023, 10, 1)
    ret.startDate=dt.date(2023, 10, 1)
    ret.endDate=dt.date(2023, 10, 28)
    return ret

@pytest.fixture
def render_helper(config):
    return RenderHelper.from_config(config)

def test_from_config(config):
    render_helper = RenderHelper.from_config(config)
    assert render_helper.maxEventsPerDay == config.maxEventsPerDay
    assert render_helper.isDisplayToScreen == config.isDisplayToScreen
    assert render_helper.isShutdownOnComplete == config.isShutdownOnComplete
    assert render_helper.batteryDisplayMode == config.batteryDisplayMode
    assert render_helper.weekStartDay == config.weekStartDay
    assert render_helper.dayOfWeekText == config.dayOfWeekText
    assert render_helper.screenWidth == config.screenWidth
    assert render_helper.screenHeight == config.screenHeight
    assert render_helper.rotateAngle == config.rotateAngle
    assert render_helper.numWeeks == config.numWeeks
    assert render_helper.is24h == config.is24h
    assert render_helper.calendarImagePath == config.calendarImagePath

def test_get_image(render_helper, cal_info):
    image = render_helper.get_image(cal_info)
    assert isinstance(image, Image.Image)
    assert image.size == (render_helper.high_res_width, render_helper.high_res_height)

def test_draw_day(render_helper, cal_info):
    draw = MagicMock()
    x, y, width, height = 0, 0, 100, 100
    weekIdx, dayIdx = 0, 0
    render_helper.draw_day(draw, x, y, width, height, cal_info, weekIdx, dayIdx)
    draw.text.assert_called()

def test_log_info(render_helper):
    render_helper.logger = MagicMock()
    render_helper.log_info()
    assert render_helper.logger.info.called

def test_image_to_file(render_helper):
    render_helper.image_to_file = MagicMock()
    render_helper.image_to_file()
    render_helper.image_to_file.assert_called()