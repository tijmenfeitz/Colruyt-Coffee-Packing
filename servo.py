import time
from periphery import GPIO

# Define the GPIO pin for the servo
SERVO_PIN = 18  # Change this to the GPIO pin you're using

# Create a GPIO object for the servo pin
servo = GPIO(SERVO_PIN, "out")

def set_angle(angle):
    # Convert angle to duty cycle
    duty_cycle = (angle / 18) + 2
    
    # PWM simulation using software
    cycle_time = 0.02  # 50Hz frequency (20ms period)
    on_time = cycle_time * (duty_cycle / 100)
    off_time = cycle_time - on_time
    
    start_time = time.time()
    while time.time() - start_time < 0.5:  # Run for 0.5 seconds
        servo.write(True)
        time.sleep(on_time)
        servo.write(False)
        time.sleep(off_time)

for _ in range(1):  


    print("Moving to 100 degrees")
    set_angle(100)
    time.sleep(4.0)
    
    print("Moving back to 180 degrees")
    set_angle(180)
    servo.close()
