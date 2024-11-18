from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
import time
from TLPMX import TLPMX
from TLPMX import TLPM_DEFAULT_CHANNEL

"""A class to work with Thorlabs Powermeter
===========================================
Make sure disconnect the device after use by running .disconnect()
"""

class ThorlabsPowerMeter:
    def __init__(self):
        self.tlPM = TLPMX()
        self.resource_name = None

    def find_devices(self):
        device_count = c_uint32()
        self.tlPM.findRsrc(byref(device_count))
        print(f"Number of found devices: {device_count.value}")
        
        devices = []
        resource_name = create_string_buffer(1024)
        for i in range(device_count.value):
            self.tlPM.getRsrcName(c_int(i), resource_name)
            device_name = c_char_p(resource_name.raw).value.decode()
            devices.append(device_name)
            print(f"Resource name of device {i}: {device_name}")
        
        print("")
        return devices

    def connect(self, resource_name=None):
        if resource_name:
            print(1)
            self.resource_name = create_string_buffer(resource_name.encode())
        elif self.resource_name:
            print(2)
            self.resource_name = create_string_buffer(self.resource_name.encode())
        else:
            raise ValueError("No resource name provided or available.")
        print(self.resource_name)
        self.tlPM.open(self.resource_name, c_bool(True), c_bool(True))
        message = create_string_buffer(1024)
        self.tlPM.getCalibrationMsg(message, TLPM_DEFAULT_CHANNEL)
        print("Connected to device.")
        print("Last calibration date:", c_char_p(message.raw).value.decode())
        print("")
    
    def set_wavelength(self, wavelength_nm):
        wavelength = c_double(wavelength_nm)
        self.tlPM.setWavelength(wavelength, TLPM_DEFAULT_CHANNEL)
        print(f"Wavelength set to {wavelength_nm} nm.")

    def enable_auto_range(self, enable=True):
        self.tlPM.setPowerAutoRange(c_int16(1 if enable else 0), TLPM_DEFAULT_CHANNEL)
        print(f"Auto-range {'enabled' if enable else 'disabled'}.")

    def set_power_unit(self, unit="Watt"):
        unit_map = {"Watt": 0, "dBm": 1}
        if unit not in unit_map:
            raise ValueError("Invalid power unit. Choose 'Watt' or 'dBm'.")
        self.tlPM.setPowerUnit(c_int16(unit_map[unit]), TLPM_DEFAULT_CHANNEL)
        print(f"Power unit set to {unit}.")

    def measure_power(self, count=5, interval=1e-3):
        power_measurements = []
        for _ in range(count):
            power = c_double()
            self.tlPM.measPower(byref(power), TLPM_DEFAULT_CHANNEL)
            power_measurements.append(power.value)
            time.sleep(interval)
        return power_measurements

    def disconnect(self):
        self.tlPM.close()
        print("Power meter disconnected.")

# Example Usage
# pm = ThorlabsPowerMeter()
# devices = pm.find_devices()
# if devices:
#     pm.connect(devices[-1])  # Connect to the last found device
#     pm.set_wavelength(671)
#     pm.enable_auto_range(True)
#     pm.set_power_unit("Watt")
#     pm.measure_power(count=5, interval=1)
#     pm.disconnect()