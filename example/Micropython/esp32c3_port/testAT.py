# SPDX-FileCopyrightText: 2022 Mark Perino
#
# SPDX-License-Identifier: MIT

"""


====================================================
Examples using mperino's (my) version of esp_at_port for the LillyGO T-PicoC3 under Micropython.

Each function should have an example called in the code.
You will also likley need a secrets.py file.  Edit it and put it on the board together with this file and esp_at_port.py

As alwasy, AT interfaces are slow, and depricated by both espressif and Micropython, but it mostly works.
Command set:
https://www.espressif.com/sites/default/files/documentation/4a-esp8266_at_instruction_set_en.pdf
Examples:
https://www.espressif.com/sites/default/files/documentation/4b-esp8266_at_command_examples_en.pdf
* Author(s):  ExperiMentor, mperino
Implementation Notes
--------------------
**Hardware:**
* LilyGO T-PicoC3
**Software and Dependencies:**
* Lillygo Supplied Micropython: e7dfbcd 
  https://github.com/Xinyuan-LilyGO/T-PicoC3/tree/main/example/Micropython/firmware
"""
from esp_at_port import esp_uart
import time

esp = esp_uart(1)
time.sleep_ms(500)
# Reset the ESP
print("Reset ESP:",esp.soft_reset())
print("Scan WIFI:",esp.scan_APs())


try:
    while True:
        command = input("Command: ")
        response = esp.sendAT(command)
        # print(response, "\n") # if want to see all the \r\n
        print(response) # otherwise display with codes applied

except KeyboardInterrupt:
    pass