# move_servo.py
import serial
import time

# Initialize serial communication with ESP32-CAM
ser = serial.Serial('COM6', 115200)  # Replace 'COM6' with the correct port
time.sleep(2)  # Wait for the serial connection to initialize

# Servo control parameters
pan_angle = 90  # Initial pan angle (X-axis)
tilt_angle = 90  # Initial tilt angle (Y-axis)
servo_speed = 2  # Speed of servo movement (adjust as needed)
servo_delay = 0.02  # Delay between servo movements (in seconds)

# Define tilt servo limits (adjust these values as needed)
TILT_MIN_ANGLE = 60  # Minimum angle for tilt (down)
TILT_MAX_ANGLE = 100  # Maximum angle for tilt (up)

# Function to constrain servo angles to valid range
def constrain_angle(angle, min_angle, max_angle):
    return max(min_angle, min(max_angle, angle))

# Function to move servos via serial communication
def move_servo(x, y, frame_width, frame_height):
    global pan_angle, tilt_angle

    # Calculate the error between the object center and the frame center
    center_x = frame_width // 2
    center_y = frame_height // 2
    error_x = x - center_x
    error_y = y - center_y

    # Pan servo (left/right)
    if error_x > 30:  # Object is to the right
        pan_angle += servo_speed  # Move right
    elif error_x < -30:  # Object is to the left
        pan_angle -= servo_speed  # Move left

    # Tilt servo (up/down)
    if error_y > 30:  # Object is below
        tilt_angle += servo_speed  # Move down
    elif error_y < -30:  # Object is above
        tilt_angle -= servo_speed  # Move up

    # Constrain servo angles to valid range
    pan_angle = constrain_angle(pan_angle, 0, 180)  # Pan servo range (0 to 180)
    tilt_angle = constrain_angle(tilt_angle, TILT_MIN_ANGLE, TILT_MAX_ANGLE)  # Tilt servo range

    # Send target positions to ESP32-CAM via serial communication
    command = f"{pan_angle},{tilt_angle}\n"
    ser.write(command.encode())
    print(f"Sent to ESP32-CAM: {command.strip()}")  # Debug print

    # Add delay for smoother movement
    time.sleep(servo_delay)