import tkinter as tk
import subprocess
import threading

# Function to capture and display the live output of another script
def capture_output():
    try:
        # Replace 'your_script.py' with the path to your script
        process = subprocess.Popen(
            ['python', 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1  # Line-buffered
        )

        while True:
            line = process.stdout.readline()
            if not line:
                break
            # Get the current content of the text widget
            current_text = output_text.get("1.0", "end-1c")
            # Append the new output to the same line
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, current_text + line)
            output_text.see(tk.END)  # Scroll to the end
            output_text.update_idletasks()  # Update the tkinter GUI

        process.stdout.close()
        process.wait()
    except Exception as e:
        # Handle any exceptions here
        print(f"Error: {e}")

# Create a tkinter window
window = tk.Tk()
window.title("Live Output Viewer")

# Create a text widget for displaying live output
output_text = tk.Text(window)
output_text.pack(fill=tk.BOTH, expand=True)

# Create a button to start capturing and displaying output
capture_button = tk.Button(window, text="Capture Output", command=lambda: threading.Thread(target=capture_output).start())
capture_button.pack()

# Start the tkinter main loop
window.mainloop()
