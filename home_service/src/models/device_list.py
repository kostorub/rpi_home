class DeviceList:
    def __init__(self, devices=[]):
        self.devices = devices
    
    def __getitem__(self, value):
        for device in self.devices:
            if isinstance(value, str):
                if device.name == value:
                    return device
            if isinstance(value, int):
                if device.pin.number == value:
                    return device
        else:
            raise Exception(f"No device found on this pin: {value}")
    
    def __iter__(self):
        return iter(self.devices)

    def append(self, value):
        self.devices.append(value)

    def find_similar_phrase(self, text):
        phrases = text.split()
        for device in self.devices:
            if all(phrase in device.phrase_on for phrase in phrases):
                return device, True
            if all(phrase in device.phrase_off for phrase in phrases):
                return device, False
        return None, False

if __name__ == "__main__":
    devices = DeviceList()
    print(devices[1])