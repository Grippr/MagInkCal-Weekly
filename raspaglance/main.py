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
# import datetime as dt
# import sys

# from pytz import timezone
# from gcal.gcal import GcalHelper
# from render.render import RenderHelper
# from power.power import PowerHelper
# import json
# import logging

import os
import sys
import logging

sys.path.append(os.path.abspath("."))
from raspaglance.config import ConfigInfo
from raspaglance.gcal.calendar_info import CalendarInfo
from raspaglance.render.render import RenderHelper

logging.basicConfig(level=logging.DEBUG)

def main():
    # Create and configure logger
    logging.basicConfig(filename="logfile.log", format='%(asctime)s %(levelname)s - %(message)s', filemode='a')
    logger = logging.getLogger('raspaglance')
    logger.addHandler(logging.StreamHandler(sys.stdout))  # print logger to stdout
    logger.setLevel(logging.INFO)
    logger.info("Starting daily calendar update")

    # Read the config
    logger.info("Reading config")
    config = ConfigInfo.from_file("config.json5")

    # Read the calendar
    logger.info("Reading calendar")
    cal_info = CalendarInfo.from_config(config=config)

    # Render an Image
    logger.info("Rendering image")
    renderHelper = RenderHelper.from_config(config=config)
    image = renderHelper.get_image(cal_info)

    # try:
    #     # Establish current date and time information
    #     # Note: For Python datetime.weekday() - Monday = 0, Sunday = 6
    #     # For this implementation, each week starts on a Sunday and the calendar begins on the nearest elapsed Sunday
    #     # The calendar will also display 5 weeks of events to cover the upcoming month, ending on a Saturday
    #     powerService = PowerHelper()
    #     powerService.sync_time()
    #     currBatteryLevel = powerService.get_battery()
    #     logger.info('Battery level at start: {:.3f}'.format(currBatteryLevel))

    #     calDict = {'events': eventList, 'calStartDate': calStartDate, 'today': currDate, 'lastRefresh': currDatetime,
    #                'batteryLevel': currBatteryLevel, 'batteryDisplayMode': batteryDisplayMode,
    #                'dayOfWeekText': dayOfWeekText, 'weekStartDay': weekStartDay, 'maxEventsPerDay': maxEventsPerDay,
    #                'is24hour': is24hour}

    #     if isDisplayToScreen:
    #         from display.display import DisplayHelper
    #         displayService = DisplayHelper(screenWidth, screenHeight)
    #         if currDate.weekday() == weekStartDay:
    #             # calibrate display once a week to prevent ghosting
    #             displayService.calibrate(cycles=0)  # to calibrate in production
    #         displayService.update(calBlackImage, calRedImage)
    #         displayService.sleep()

    #     currBatteryLevel = powerService.get_battery()
    #     logger.info('Battery level at end: {:.3f}'.format(currBatteryLevel))

    # except Exception as e:
    #     logger.error(e)

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