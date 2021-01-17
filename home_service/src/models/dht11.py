from dht11 import DHT11 as DHT


class DHT11(DHT):
    def __init__(self, bcm_pin, name, phrase):
        super(DHT11, self).__init__(bcm_pin)
        self.pin = bcm_pin
        self.name = name
        self.phrase = phrase

    def status(self):
        result = self.read()
        if result.is_valid():
            return result.temperature, result.humidity
        else:
            return -1, -1