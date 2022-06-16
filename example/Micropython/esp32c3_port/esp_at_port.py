# SPDX-FileCopyrightText: 2022 Mark Perino
#
# SPDX-License-Identifier: MIT

"""
This is a Derivitive work based on:
`adafruit_espatcontrol.adafruit_espatcontrol` 2018 ladyada for Adafruit Industries
and
'T-PicoC3/example/Micropython/esp32c3_port/esp_at_port.py' 2022 Micky Micky513673326

====================================================
An attempt to implement the AT interfaces in adafruit_espatcontrol for the LillyGO T-PicoC3 under Micropython.
The changes are both for the hardware specific to T-Pico, and Micropython vs CircuitPython.
Wherever possible I have kept the same functions as the 

As alwasy, AT interfaces are slow, and depricated by both espressif and Micropython, but it mostly works.
Command set:
https://www.espressif.com/sites/default/files/documentation/4a-esp8266_at_instruction_set_en.pdf
Examples:
https://www.espressif.com/sites/default/files/documentation/4b-esp8266_at_command_examples_en.pdf
* Author(s): ladyada, Micky, mperino
Implementation Notes
--------------------
**Hardware:**
* LilyGO T-PicoC3
**Software and Dependencies:**
* Lillygo Supplied Micropython: e7dfbcd 
  https://github.com/Xinyuan-LilyGO/T-PicoC3/tree/main/example/Micropython/firmware
"""



from machine import UART, Pin
import time

#
# settings
#
retries = 3



class esp_uart:
    def __init__(self,bus_num):
        self.uart = UART(bus_num, baudrate=115200, tx=Pin(8), rx=Pin(9), cts=Pin(10), rts=Pin(11))
        self.uart.write('ATE0\r\n') #turn off echo
        self.sendAT('')

    def begin(self):
        for _ in range(self.retries):
            try:
#                if not self.sync() and not self.soft_reset():
#                    self.hard_reset()
#                    self.soft_reset()
                self.echo(False)
                self.get_version()
                if self.cipmux != 0:
                    self.cipmux = 0
                try:
                    self.sendAT('CIPSSLSIZE=4096')
                except:
                    self.sendAT('CIPSSLCCONF?')
                self.initialized = True
                return
            except:
                pass
            
    def sync(self):
        try:
            self.sendAT('')
            return True
        except:
            return False

    def soft_reset(self):
        self.sync()
        try:
            if "OK\r\n" in self.sendAT('RST'):
                print("T")
                time.sleep_ms(50)
                return True
        except:
            print("Soft Reset Failed")
            return False


    def sendAT(self,cmd):
        self.uart.write('AT+'+cmd+'\r\n')
        while self.uart.any()==0:
            time.sleep_ms(1)
        time.sleep_ms(50) #Prevent data loss caused by excessive data
        return self.uart.read()

    def reset(self):
        try:
            message = self.sendAT('RST')
            time.sleep_ms(50)
        except:
            print("Failed to Reset.  Try a Power Cycle of the board")
        return message
    
    def scan_APs(self):
        try:
            self.scan = self.sendAT('CWLAP').split(b"\r\n")
    
        except:
            print("Failed to scan for AP.  Make sure the ESP is in the correct mode")
            
        routers = []
        for line in self.scan:
            if line.startswith(b"+CWLAP:("):
                router = line[8:-1].split(b",")
                for i, val in enumerate(router):
                    router[i] = str(val, "utf-8")
                    try:
                        router[i] = int(router[i])
                    except ValueError:
                        router[i] = router[i].strip('"')  # its a string!
                routers.append(router)
            return routers
     

    def mode(self, mode: int) -> None:
        if not self._initialized:
            self.begin()
        if not mode in (1, 2, 3):
            raise RuntimeError("Invalid Mode")
        self.at_response("AT+CWMODE=%d" % mode, timeout=3)
        
    MODE_STATION = 1
    MODE_SOFTAP = 2
    MODE_SOFTAPSTATION = 3
    TYPE_TCP = "TCP"
    TCP_MODE = "TCP"
    TYPE_UDP = "UDP"
    TYPE_SSL = "SSL"
    TLS_MODE = "SSL"
    STATUS_APCONNECTED = 2
    STATUS_SOCKETOPEN = 3
    STATUS_SOCKETCLOSED = 4
    STATUS_NOTCONNECTED = 5
    USER_AGENT = "esp-idf/1.0 esp32"
    
        