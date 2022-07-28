import board
import busio
from time import sleep
from analogio import AnalogIn
from adafruit_dac4725 import adafruit_mcp4725
#
from drivers_wish_maps import maps




#dac setup:
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

#read sensor value:
analog_in = AnalogIn(board.A4)


#smoothing sensor readings w/ running average:
num_of_reads = 20
readings = [0] * num_of_reads
start_read = 0
total_reads = 0
average = 0

    
def _get_voltage(pin):
    return (pin.value * 3.3) / 65536


#mapping a drivers wish map with the sensor output
def _map(x, in_min, in_max, out_min, out_max):
    return (((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min) * 10)


#main function normalized
def main():
    global total_reads, start_read
    
    total_reads = total_reads - readings[start_read]
    readings[start_read] = _get_voltage(analog_in)
    total_reads = total_reads + readings[start_read]
    start_read = start_read + 1

    if start_read >= num_of_reads:
        start_read = 0
    
    
    average = total_reads / num_of_reads
    if average > 0.75 and average < 1.5:
        mapped_val = _map(average, 0.0, 2.5, float(maps["map_75"][0]), float(maps["map_112"][-1]))
        dac.normalized_value = mapped_val / 10
        sleep(0.01)
    elif average > 1.5 and average < 2.0:
        mapped_val = _map(average, 0.0, 2.5, float(maps["map_90"][-1]), float(maps["map_25"][0]))
        dac.normalized_value = mapped_val / 10
        sleep(0.01)
    else:
        dac.normalized_value = 1.0
        sleep(0.01)


if __name__ == "__main__":
    main()
