#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    i8kfans.py: Adjust the fans speed in various Dell laptops (with a nvidia
    graphics card) to maintain the right temperatures. This affect both fans,
    the cpu and the gpu fan. Originally i8k was created to run in a Dell
    Inspiron 8000 laptop, but this Dell fan control via SMM BIOS is available
    in others laptops of various series (Inspiron, XPS, Latitude, etcetera),
    but not all of them are supported. Mine is an Inspiron 9400 but I tested
    this successfully in a XPS m1330 too.

    Based on a 2006 bash script by Wheelspin, `i8kapplet`. This old script
    served faithfully me for many years, but my ears couldn't stand much longer
    its random and common slow downs/speed ups. Over the years, fans have
    become more and more loud. This new script runs in a more smooth way, with
    less sudden changes.  It's cheaper than replace booth fans, don't you
    think?

    This script needs the `i8kutils` linux package installed and the `i8k`
    kernel module loaded to work.
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
__date__ = "16/06/2012"
__version__ = "0.4"


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
            msg = 'The {0} program is necessary to run this.'.format(prog)
            exit(msg)
    return


def set_right_fan_speed(fan):
    """Set the right fan speed for current temp. to use with i8kfan command.

    :fan: dictionary with fan values

    """
    if fan['temp'] >= fan['low']:
        if fan['temp'] >= fan['high']:
            fan['rfs'] = 2
        else:
            fan['rfs'] = 1
    else:
        fan['rfs'] = 0


def check_airflow(cpu, gpu):
    """Guarantee a minimal internal airflow when a side is cold and the other
    hot.

    :cpu: dictionary with cpu fan values
    :gpu: dictionary with gpu fan values

    """
    speed_difference = gpu['rfs'] - cpu['rfs']
    if abs(speed_difference) == 2:
        if speed_difference > 1:
            cpu['rfs'] += 1
        else:
            gpu['rfs'] += 1


def main():
    """Main section"""
    # time between temperature checks
    interval = 1
    # set the temp thresholds to jump to a faster fan speed. Values greater
    # than 'low' set the fan speed to 1 and the ones greater than 'high' set
    # the speed to 2. Obviously, values minor than 'low' stop the fan
    gpu = {'low': 45, 'high': 53}
    cpu = {'low': 45, 'high': 50}

    # check if the i8k kernel module is already loaded
    if  "i8k" not in check_output("ls /proc/".split()):
        exit("The i8k kernel module is not loaded")

    while True:
        try:
            # get current values
            cpu['temp'] = int(check_output("i8kctl temp".split()))
            gpu_out = check_output("nvidia-smi -q -d TEMPERATURE".split())
            gpu['temp'] = int([s for s in gpu_out.split() if s.isdigit()][-1])
            cpu['speed'], gpu['speed'] = [int(f) for f in
                                          check_output("i8kfan").split()]

            # get the right speed values for each fan
            set_right_fan_speed(cpu)
            set_right_fan_speed(gpu)
            # guarantee a minimal internal airflow when is needed
            check_airflow(cpu, gpu)
            # if any of the fans needs to change their speed, change it!
            if cpu['rfs'] != cpu['speed'] or gpu['rfs'] != gpu['speed']:
                Popen("i8kfan {0} {1}".format(cpu['rfs'], gpu['rfs']).split(),
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
# 0.4:
#
# * Guarantee a minimal internal airflow when a side is cold and the other hot
# * Change temperature thresholds for cpu
# * Refactorization
#
# 0.3:
#
# * Better documentation
#
# 0.2:
#
# * Fix an error in a function docstring due to refactorization
# * Give appropriate credit to original idea' script
#
# 0.1:
#
# * First attempt
#
