import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from tkinter.constants import DISABLED
from tkinter.font import NORMAL
from tkinter import font
import pygame

# Global variables to track countdown state and alarm
update_task_id = None
count_val = 0  # To track the countdown value
alarm_playing = False  # Flag to track if alarm is currently playing
placeholder = "Duration in Seconds"  # Placeholder for input text box
pygame.mixer.init()  # Initialize the pygame mixer for audio playback


def set_timer(time_input_box, set_button, counter_val_label, start_button, placeholder_text, counter_val_label2):
    """
    Function to set or reset the countdown timer based on user input.
    If the 'Set' button is clicked, the timer is initialized to the input value.
    If the 'Reset' button is clicked, the timer is reset to 0.
    """
    global count_val, placeholder, alarm_playing
    time_val = time_input_box.get()  # Get the time input from the user
    button_label = set_button.cget("text")  # Get the current label of the set button
    placeholder = placeholder_text

    if time_val != "":
        try:
            if button_label == "Set":
                # Convert input to integer and set the countdown timer
                count_val = int(time_val)
                if count_val <= 0:
                    messagebox.showerror("Entry Error", "Value must be positive")
                else:
                    # Update the label with the countdown value
                    counter_val_label.config(text=f"{count_val}")
                    set_button.config(text="Reset")  # Change button label to 'Reset'
                    time_input_box.config(state=DISABLED)  # Disable time input box after setting timer

            elif button_label == "Reset":
                # Reset the countdown value to 0
                count_val = 0
                counter_val_label.config(text="0")  # Reset the displayed countdown label
                counter_val_label2.config(text="")  # Clear the additional label
                set_button.config(text="Set")  # Change button label back to 'Set'
                time_input_box.config(state=NORMAL)  # Re-enable time input box
                time_input_box.delete(0, tk.END)  # Clear the input box
                start_button.config(text="Start")
                time_input_box.config(text=placeholder_text)  # Reset placeholder text
                if alarm_playing:
                    pygame.mixer.music.stop()  # Stop the alarm sound
                    alarm_playing = False  # Reset the alarm status

        except ValueError:
            messagebox.showerror("Entry Error", "Value must be a number")
    else:
        messagebox.showerror("Entry Error", "No value has been provided yet")


def update_countdown(window, time_input_box, counter_val_label, set_button, start_button, counter_val_label2):
    """
    Function that updates the countdown every second.
    Decreases the countdown value by 1 second and updates the displayed time.
    When time reaches 0, the countdown stops and triggers the alarm sound.
    """
    global count_val, update_task_id, alarm_playing

    if count_val > 0:
        count_val -= 1  # Decrease the countdown value by 1 second

        # Convert total seconds to hours, minutes, and seconds for display
        hours = count_val // 3600
        minutes = (count_val % 3600) // 60
        seconds = count_val % 60
        counter_val_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")  # Update label
        counter_val_label2.config(text="Hours : Minutes : Seconds")  # Update label

        # Continue the countdown by calling update_countdown every 1000 ms (1 second)
        update_task_id = window.after(1000, update_countdown, window, time_input_box, counter_val_label, set_button,
                                      start_button, counter_val_label2)
    else:
        # When the countdown reaches 0
        start_button.config(text="Start")  # Change start button text to "Start"
        counter_val_label.config(text="Time up!")  # Display "Time up!" message
        counter_val_label2.config(text="")  # Clear the second label
        time_input_box.config(state=NORMAL)  # Enable input box to set a new time
        set_button.config(state=NORMAL)  # Enable the 'Set' button
        start_button.config(state=NORMAL)  # Enable the 'Start' button

        # Play alarm sound if it's not already playing
        if not alarm_playing:
            pygame.mixer.music.load("alarm.wav")  # Load alarm sound
            loops = 3  # Number of times to loop the alarm
            pygame.mixer.music.play(loops=loops, start=0.0)  # Play the alarm sound
            alarm_playing = True  # Set alarm_playing to True to prevent restarting the alarm


def start_timer(time_input_box, set_button, start_button, counter_val_label, window, counter_val_label2):
    """
    Function to start, pause, or resume the countdown timer.
    If the countdown is paused, the timer will resume.
    If the countdown is not set, an error is shown.
    """
    global update_task_id, count_val, alarm_playing

    if start_button.cget("text") == "Start":
        # If the countdown hasn't started yet, start it
        if count_val == 0:
            messagebox.showerror("Error", "Please set a valid duration first")
        else:
            # Disable input box and Set button during countdown to prevent modification
            time_input_box.config(state=DISABLED)
            set_button.config(state=DISABLED)
            start_button.config(text="Pause")  # Change button text to "Pause"
            start_button.config(state=NORMAL)  # Ensure the button is enabled for pausing
            update_countdown(window, time_input_box, counter_val_label, set_button, start_button,
                             counter_val_label2)  # Start updating the countdown

    elif start_button.cget("text") == "Pause":
        # If the countdown is running, pause it
        start_button.config(text="Resume")  # Change button text to "Resume"
        # Cancel the countdown task to pause it
        if update_task_id:
            window.after_cancel(update_task_id)
            update_task_id = None  # Reset the task ID to indicate it's paused

        # Allow users to reset or modify the countdown duration
        time_input_box.config(state=DISABLED)
        set_button.config(state=NORMAL)
        start_button.config(state=NORMAL)  # Re-enable the start button for resuming

    elif start_button.cget("text") == "Resume":
        # If the countdown is paused, resume it
        start_button.config(text="Pause")  # Change button text to "Pause"
        # Continue the countdown by calling update_countdown again
        update_countdown(window, time_input_box, counter_val_label, set_button, start_button,
                         counter_val_label2)  # Continue the countdown


def stop_counter(window, set_button, start_button, counter_val_label, time_input_box, count_val_parameter):
    """
    Function to stop the countdown and reset the state.
    Cancels the ongoing countdown and stops the alarm if it's playing.
    """
    global update_task_id, alarm_playing, count_val
    count_val = count_val_parameter  # Reset the count value to its initial state

    if update_task_id is not None:
        # Cancel the countdown task
        window.after_cancel(update_task_id)
        update_task_id = None  # Reset task ID

        # Reset button labels and clear counter
        start_button.config(text="Start")
        set_button.config(text="Set")  # Reset the set button text
        counter_val_label.config(text="0")  # Clear the counter label

        # Enable the time input box and buttons
        time_input_box.config(state=NORMAL)
        set_button.config(state=NORMAL)
        start_button.config(state=NORMAL)

    if alarm_playing:
        # Stop the alarm sound
        pygame.mixer.music.stop()
        alarm_playing = False  # Reset the alarm status


def on_focus_in(event, time_input_box, placeholder):
    """
    Handles the focus-in event for the entry widget.
    Clears the placeholder text when the input field is clicked.
    """
    if time_input_box.get() == placeholder:
        time_input_box.config(fg='black')
        time_input_box.delete(0, tk.END)  # Clear the placeholder text


def on_focus_out(event, time_input_box, placeholder):
    """
    Handles the focus-out event for the entry widget.
    Re-inserts the placeholder text if the input field is empty.
    """
    if time_input_box.get() == '':
        time_input_box.insert(0, placeholder)  # Reinsert the placeholder text
        time_input_box.config(fg='grey')  # Change text color to grey


def main():
    # Initialize Tkinter window
    window = tk.Tk()

    # Set default font for the window
    default_font = font.nametofont("TkDefaultFont")
    default_font.config(family="Helvetica", size=12)
    window.option_add("*font", default_font)

    window.title("Counter Down Timer")
    window.geometry("300x250")
    window.resizable(False, False)

    alarm_icon = PhotoImage(file="alarm-icon.png")
    window.iconphoto(True, alarm_icon)

    # Frames for layout
    frame_top = tk.Frame(window)
    frame_top.pack(pady=(20, 0))

    frame_middle = tk.Frame(window, borderwidth=2, background="#e9f2f2")
    frame_middle.pack(padx=20, pady=10)

    frame_bottom = tk.Frame(window)
    frame_bottom.pack(padx=5, pady=(10, 0))

    placeholder = "Time in Seconds"

    # Time input section
    time_input_label = tk.Label(frame_top, text="Enter Duration")
    time_input_label.pack(pady=(5, 10))
    time_input_box = tk.Entry(frame_top, font=("Helvetica", 12, "bold"), fg='grey', justify="center")
    time_input_box.insert(0, placeholder)  # Initial empty string in the input box
    time_input_box.bind("<FocusIn>", lambda event: on_focus_in(event, time_input_box, placeholder))  # Focus in event
    time_input_box.bind("<FocusOut>", lambda event: on_focus_out(event, time_input_box, placeholder))  # Focus out event
    time_input_box.pack(padx=10)

    # Counter value label
    counter_val_label = tk.Label(frame_middle, text="0", font=("Helvetica", 40))
    counter_val_label.pack()
    counter_val_label2 = tk.Label(frame_middle, text="", font=("Helvetica", 12))
    counter_val_label2.pack()

    # Buttons section
    start_button = tk.Button(frame_bottom, text="Start", width=7,
                             command=lambda: start_timer(time_input_box, set_button, start_button, counter_val_label,
                                                         window, counter_val_label2))
    start_button.grid(row=0, column=0, padx=(0, 5))

    stop_button = tk.Button(frame_bottom, text="Stop", width=7,
                            command=lambda: stop_counter(window, set_button, start_button, counter_val_label,
                                                         time_input_box, count_val))
    stop_button.grid(row=0, column=1, padx=5)

    set_button = tk.Button(frame_bottom, text="Set", width=7,
                           command=lambda: set_timer(time_input_box, set_button, counter_val_label, start_button,
                                                     placeholder, counter_val_label2))
    set_button.grid(row=0, column=2, padx=(5, 0))

    window.mainloop()


if __name__ == "__main__":
    main()
