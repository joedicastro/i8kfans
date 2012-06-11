#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    i8kfans.py: Adjust the fans speed in Dell Inspiron laptops (with a nvidia
    graphics card) to maintain the right temperatures. This affect both fans,
    the cpu and the gpu fan.

    Based on a 2006 bash script by Wheelspin. This old script served faithfully
    me for many years, but my ears couldn't stand much longer its random and
    common slow downs/speed ups. Over the years, fans have become more and more
    loud. This new script runs in a more smooth way, with less sudden changes.
    It's cheaper than replace booth fans, don't you think?

"""


#==============================================================================
#    Copyright 2012 joe di castro <joe@joedicastro.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "11/06/2012"
__version__ = "0.1"


try:
    from os import linesep
    from subprocess import check_output, Popen, PIPE
    from sys import exit, exc_info
    from time import sleep
except ImportError:
    # Checks the installation of the necessary python modules
    print((linesep * 2).join(["An error found importing one module:",
    str(exc_info()[1]), "You need to install it", "Stopping..."]))
    exit(-2)


def check_execs(*progs):
    """Check if the programs are installed, if not exit and report."""
    for prog in progs:
        try:
            Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
        except OSError:
            msg = 'The {0} program is necessary to run this script'.format(prog)
            exit(msg)
    return


def get_right_fan_speed(current_temperature, current_fan_speed, temp_triggers):
    """Get the right fan speed to use with i8kfan command.

    :current_temperature: current temperature value for the fan implied
    :current_fan_speed: current fan speed
    :temp_triggers: the threshold temp_triggers to trigger the fan speed change
    :returns: right fan speed or "-" (means change nothing to i8kfan)

    """
    right_fan_speed = None  # the right fan speed for the current temp
    if current_temperature >= temp_triggers[0]:
        if current_temperature >= temp_triggers[1]:
            right_fan_speed = 2
        else:
            right_fan_speed = 1
    else:
        right_fan_speed = 0
    return right_fan_speed if right_fan_speed != current_fan_speed else "-"


def main():
    """Main section"""
    # time between temperature checks
    interval = 1
    # the temp thresholds to jump to a faster fan speed. Values greater than
    # [g|c]pu[0] set the fan speed to 1 and the ones greater than [g|c]pu[1]
    # set the speed to 2. Obviously, values minor than [g|c]pu[0] stop the fan
    gpu_temps = [45, 53]
    cpu_temps = [40, 50]

    # check if the i8k kernel module is already loaded
    if  "i8k" not in check_output("ls /proc/".split()):
        exit("The i8k kernel module is not loaded")

    while True:
        try:
            # get current values
            cpu_temp = int(check_output("i8kctl temp".split()))
            gpu_out = check_output("nvidia-smi -q -d TEMPERATURE".split())
            gpu_temp = int([s for s in gpu_out.split() if s.isdigit()][-1])
            cpu_fan, gpu_fan = [int(f) for f in check_output("i8kfan").split()]

            # get the right speed values for each fan
            cpu_rfs = get_right_fan_speed(cpu_temp, cpu_fan, cpu_temps)
            gpu_rfs = get_right_fan_speed(gpu_temp, gpu_fan, gpu_temps)

            # if any of the fans needs to change their speed, change it!
            if cpu_rfs != "-" or gpu_rfs != "-":
                Popen("i8kfan {0} {1}".format(cpu_rfs, gpu_rfs).split(),
                      stdout=PIPE)

            # wait a moment. We want a cooler laptop, aren't we?
            sleep(interval)
        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    check_execs("i8kctl", "i8kfan", "nvidia-smi")
    main()

###############################################################################
#                                  Changelog                                  #
###############################################################################
#
# 0.1:
#
# * First attempt
#
