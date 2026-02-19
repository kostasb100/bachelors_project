"""
Calibration module for the HX711-based load cell measurement system

This program:
- Determines the reference unit required to convert raw HX711 ADC readings into mass values (grams).

Purpose:
- Establish accurate raw-to-mass conversion
- Improve measurement stability by reducing noise influence
- Ensure repeatable mass measurements during experimental cycles

Date: 2025-10
"""

import time
import RPi.GPIO as GPIO
from hx711 import HX711

# Setup HX711
hx = HX711(17, 27) # (DAT,CLK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()

# Collect this number of samples to calibrate
num_samples = 50

print(f"Place known weight on scale and enter it's weight in grams:",end="")
known_weight = int(input())

# Collect samples
print("Collecting samples...")
samples = []
for i in range(num_samples):
    reading = hx.get_weight(1)
    samples.append(reading)
    print(f"{i+1}: {reading}")
    time.sleep(0.2)

# Remove outliers to avoid changes due to errors
samples.sort()
clean_samples = samples[3:-3]  # Remove 3 highest and 3 lowest

# Calculate reference unit
average = sum(clean_samples) / len(clean_samples)
reference_unit = average / known_weight

print(f"\nAverage reading: {average:.1f}")
print(f"Reference unit: {reference_unit:.2f}")
print(f"\nAdd this to your script:")
print(f"hx.set_reference_unit({reference_unit:.2f})")

GPIO.cleanup()