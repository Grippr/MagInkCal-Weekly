#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This project is designed for the WaveShare 12.48" eInk display. Modifications will be needed for other displays,
especially the display drivers and how the image is being rendered on the display. Also, this is the first project that
I posted on GitHub so please go easy on me. There are still many parts of the code (especially with timezone
conversions) that are not tested comprehensively, since my calendar/events are largely based on the timezone I'm in.
There will also be work needed to adjust the calendar rendering for different screen sizes, such as modifying of the
CSS stylesheets in the "render" folder.
"""
from argparse import ArgumentParser
import datetime as dt
import os
import sys
import logging


sys.path.append(os.path.abspath("."))
from MagInkCalPy.config import ConfigInfo
from MagInkCalPy.gcal.calendar_info import CalendarInfo
from MagInkCalPy.render.render import RenderHelper
from MagInkCalPy.power import PowerHelper

logging.basicConfig(level=logging.DEBUG)

maginkcal_stages = (
    "get_calendar",
    "render_image",
    "output_to_display",
)

def add_main_arguments(parser: ArgumentParser):
    parser.add_argument(
        "-f", "--first-stage",
        type = str,
        choices=maginkcal_stages,
        help="The stage to start at",
        default="read_config",
    )

    parser.add_argument(
        "-l", "--last-stage",
        type = str,
        choices=maginkcal_stages,
        help="The stage to end at",
        default="output_to_display",
    )

def main():
    # Setup the argument parser
    parser = ArgumentParser(description="MagInkCalPy: A Calendar for eInk Displays")

    # Add the arguments
    add_main_arguments(parser)
    ConfigInfo.add_arguments(parser)

    # Parse the arguments
    args = parser.parse_args()
    print(main)
    print(args)

    # # Create and configure logger
    # logging.basicConfig(filename="logfile.log", format='%(asctime)s %(levelname)s - %(message)s', filemode='a')
    # logger = logging.getLogger('MagInkCalPy:main')
    # logger.addHandler(logging.StreamHandler(sys.stdout))  # print logger to stdout
    # logger.setLevel(logging.INFO)
    # logger.info("Starting daily calendar update")

    # # Get the start time
    # startTime = dt.datetime.now()

    # # Read the config
    # logger.info("Reading config")
    # config = ConfigInfo.from_file("config.json5")

    # # # Read the calendar
    # logger.info("Reading calendar")
    # cal_info = CalendarInfo.from_config(config=config)

    # # Establish current date and time information
    # # Note: For Python datetime.weekday() - Monday = 0, Sunday = 6
    # # For this implementation, each week starts on a Sunday and the calendar begins on the nearest elapsed Sunday
    # # The calendar will also display 5 weeks of events to cover the upcoming month, ending on a Saturday
    # try: 
    #     powerService = PowerHelper()
    #     powerService.sync_time()
    #     currBatteryLevel = powerService.get_battery()
    #     logger.info('Battery level at start: {:.3f}'.format(currBatteryLevel))

    # except FileNotFoundError as e:
    #     logger.warning("Ensure that the PiSugar service is running. Continuing without battery level check.")
    #     currBatteryLevel = None

    # # Render an Image
    # logger.info("Rendering image")
    # renderHelper = RenderHelper.from_config(config=config)

    # if config.calendarImagePath is not None:
    #     bw_image, red_image, combined_image = renderHelper.get_image(
    #         cal_info, 
    #         currBatteryLevel=currBatteryLevel, 
    #         include_combined_image=True
    #     )
    #     combined_image.save(config.calendarImagePath)
    # else: # config.calendarImagePath is None:
    #     bw_image, red_image = renderHelper.get_image(
    #         cal_info, 
    #         currBatteryLevel=currBatteryLevel
    #     )

    # if config.isDisplayToScreen:
    #     from display.display import DisplayHelper

    #     displayService = DisplayHelper(config.screenWidth, config.screenHeight)
    #     # Cycle once a week to prevent ghosting 
    #     displayService.calibrate(cycles=0) 

    #     displayService.update(bw_image, red_image)
    #     displayService.sleep()

    # try: 
    #     currBatteryLevel = powerService.get_battery()
    #     logger.info('Battery level at end: {:.3f}'.format(currBatteryLevel))
    # except FileNotFoundError as e:
    #     pass
    # logger.info("Completed daily calendar update")


    # logger.info("Checking if configured to shutdown safely - Current hour: {}".format(currDatetime.hour))
    # if isShutdownOnComplete:
    #     # implementing a failsafe so that we don't shutdown when debugging
    #     # checking if it's 6am in the morning, which is the time I've set PiSugar to wake and refresh the calendar
    #     # if it is 6am, shutdown the RPi. if not 6am, assume I'm debugging the code, so do not shutdown
    #     if currDatetime.hour == 6:
    #         logger.info("Shutting down safely.")
    #         import os
    #         os.system("sudo shutdown -h now")


if __name__ == "__main__":
    main()
