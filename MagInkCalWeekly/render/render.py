#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# This script essentially generates a HTML file of the calendar I wish to display. It then fires up a headless Chrome
# instance, sized to the resolution of the eInk display and takes a screenshot. This screenshot will then be processed
# to extract the grayscale and red portions, which are then sent to the eInk display for updating.

# This might sound like a convoluted way to generate the calendar, but I'm doing so mainly because (i) it's easier to
# format the calendar exactly the way I want it using HTML/CSS, and (ii) I can better delink the generation of the
# calendar and refreshing of the eInk display. In the future, I might choose to generate the calendar on a separate
# RPi device, while using a ESP32 or PiZero purely to just retrieve the image from a file host and update the screen.
# """

# from time import sleep
# from datetime import timedelta
# import pathlib
# import logging

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass, fields
import logging
import pathlib

from PIL import Image, ImageDraw, ImageFont

from MagInkCalWeekly.common import InfoBase
from MagInkCalWeekly.config.config_info import ConfigInfo
from MagInkCalWeekly.gcal.calendar_info import CalendarInfo

import datetime as dt


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

sf = 1 #scaling factor
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
@dataclass
class RenderHelper(InfoBase):
    maxEventsPerDay: int
    isDisplayToScreen: bool
    isShutdownOnComplete:bool
    batteryDisplayMode: int
    weekStartDay: int
    dayOfWeekText: list
    screenWidth: int
    screenHeight: int
    rotateAngle: int
    numWeeks: int
    is24h: bool
    calendarImagePath: str
    logger = logging.getLogger('renderer')

    ## Configuration

    # Calendar Margins
    top_margin    = 10*sf
    left_margin   = 10*sf
    bottom_margin = 10*sf
    right_margin  = 10*sf

    # Month spacing
    month_to_day_spacing = 20*sf

    # Event spacing
    day_to_event_spacing = 5*sf
    max_event_width = 17
    event_margins = 5*sf

    # Fonts
    font_bold = pathlib.Path(__file__).parent / "Quattrocento-Bold.ttf"
    font_regular = pathlib.Path(__file__).parent / "Quattrocento-Regular.ttf"

    month_size = 80*sf
    day_size = 35*sf
    event_size = 18*sf

    @classmethod
    def from_config(cls, config: ConfigInfo):
        ret = cls(
            maxEventsPerDay=config.maxEventsPerDay,
            isDisplayToScreen=config.isDisplayToScreen,
            isShutdownOnComplete=config.isShutdownOnComplete,
            batteryDisplayMode=config.batteryDisplayMode,
            weekStartDay=config.weekStartDay,
            dayOfWeekText=config.dayOfWeekText,
            screenWidth=config.screenWidth,
            screenHeight=config.screenHeight,
            rotateAngle=config.rotateAngle,
            is24h=config.is24h,
            calendarImagePath=config.calendarImagePath,
            numWeeks=config.numWeeks,
        )
        return ret
    
    def get_image(self, cal_info: CalendarInfo):
        # Scaling: PIL doesn't support subpixel rendering, so we need to scale up the image, then downsize it before displaying
        self.high_res_width = self.screenWidth * sf
        self.high_res_height = self.screenHeight * sf

        # Create a new image with a white background
        image = Image.new("RGB", (self.high_res_width, self.high_res_height), WHITE)

        draw = ImageDraw.Draw(image)

        # Do the date range
        #month_name = cal_info.currDate.strftime("%B") #Eg. "January"
        date_range = f"{cal_info.startDate.strftime('%b %d')} - {cal_info.endDate.strftime('%b %d')}"
        month_font = ImageFont.truetype(str(self.font_bold), self.month_size)
        draw.text((self.left_margin, self.top_margin), date_range, fill=BLACK, font=month_font)

        # Calculate the day box sizes
        day_width = (self.high_res_width - self.left_margin - self.right_margin) / 7
        day_height = (self.high_res_height - self.top_margin - self.bottom_margin - self.month_to_day_spacing - self.month_size) / self.numWeeks

        topleft_x = self.left_margin
        topleft_y = self.top_margin + self.month_size + self.month_to_day_spacing
        for weekIdx in range(self.numWeeks):
            for dayIdx in range(7):
                x = topleft_x + dayIdx * day_width
                y = topleft_y + weekIdx * day_height
                self.draw_day(draw, x, y, day_width, day_height, cal_info, weekIdx, dayIdx)
    
        #image = image.resize((self.screenWidth, self.screenHeight), Image.LANCZOS)
        return image

    def draw_day(self, draw, x, y, width, height, cal_info, weekIdx, dayIdx):
        # Draw the date
        date = cal_info.startDate + dt.timedelta(days=weekIdx * 7 + dayIdx)
        date_str = date.strftime("%d").lstrip("0")

        # Dates not in the current month should be greyed out
        COLOR = GREY if date.month != cal_info.currDate.month else BLACK

        # Draw the date
        font = ImageFont.truetype(str(self.font_regular), self.day_size)
        if date == cal_info.currDate:
            # Draw a red circle
            circle_radius = self.day_size // 2
            circle_center = (x + self.event_margins + circle_radius, y + self.event_margins + circle_radius)
            draw.ellipse(
                [
                    (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                    (circle_center[0] + circle_radius, circle_center[1] + circle_radius)
                ],
                fill=RED
            )

            # Draw the date in white inside the circle
            draw.text((x + self.event_margins, y + self.event_margins), date_str, fill=WHITE, font=font)
        else:
            # Draw the date normally
            draw.text((x + self.event_margins, y + self.event_margins), date_str, fill=COLOR, font=font)

        # Draw the events
        event_str = ""
        for event_num, event in enumerate(cal_info.get_events_from_date(date)):
            if event_num >= self.maxEventsPerDay:
                event_str += "+" + str(len(cal_info.get_events_from_date(date)) - self.maxEventsPerDay) + " more\n"
                break
            event_str += event.get_cal_str(max_width=self.max_event_width) + "\n"

        font = ImageFont.truetype(str(self.font_regular), self.event_size)
        draw.text((x + self.event_margins, y + self.event_margins + self.day_size + self.day_to_event_spacing), event_str, fill=COLOR, font=font)

    def image_to_file(self):
        ...

    @classmethod
    def from_json(self,  json_str):
        ...

    def log_info(self):
        for field in fields(self):
            value = getattr(self, field.name)
            self.logger.info(f"{field.name}: {value}")

def debug_this():
    config = ConfigInfo.from_file('config.json5')
    cal_info = CalendarInfo.from_file("tests/data/test_cal.json")
    logging.basicConfig(level=logging.INFO)

    renderHelper = RenderHelper.from_config(config)
    image = renderHelper.get_image(cal_info=cal_info)
    image.show()