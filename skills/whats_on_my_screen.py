"""
This skill will show whats on my screen
it will take a screenshot and describe its content
"""
import pyautogui
import os
from image_interpreter import send_image_to_interpreter

def take_screenshot_and_describe():
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a temporary file
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)

    # Use the image_interpreter to find the contents of the image
    response = send_image_to_interpreter(screenshot_path)

    # Delete the screenshot after use
    os.remove(screenshot_path)

    # Return the response
    return response

# Example usage
if __name__ == "__main__":
    description = take_screenshot_and_describe()
    print(description)
