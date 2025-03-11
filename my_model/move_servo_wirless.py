# move_servo.py
import socket
import time

# TCP Server Configuration for ESP32-CAM
ESP32_IP = "192.168.3.14"  # Replace with your ESP32-CAM IP address
ESP32_PORT = 82  # Use the same port as in the ESP32-CAM code

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

# Function to move servos via TCP communication
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

    # Send target positions to ESP32-CAM via TCP
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ESP32_IP, ESP32_PORT))

        # Send the servo angles (format: "pan_angle,tilt_angle\n")
        command = f"{pan_angle},{tilt_angle}\n"
        sock.send(command.encode())
        print(f"Sent to ESP32-CAM: {command.strip()}")  # Debug print

        # Close the socket
        sock.close()
    except Exception as e:
        print(f"Error sending servo angles: {e}")

    # Add delay for smoother movement
    time.sleep(servo_delay)