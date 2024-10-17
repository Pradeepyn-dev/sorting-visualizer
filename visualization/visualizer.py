import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

class SortingVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Sorting Algorithm Visualizer")

        # Get the width and height of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Set the window size to fit the screen
        self.master.geometry(f"{screen_width}x{screen_height}")

        # Set dark theme colors
        self.master.configure(bg='#2E2E2E')  # Dark background for the window

        self.algorithm = tk.StringVar()
        self.algorithm.set("bubblesort")
        self.data = None
        self.sorting_steps = None
        self.is_sorting = False
        self.sort_thread = None
        
        # New variables for time complexity
        self.time_complexity = tk.StringVar()
        self.sorting_time = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        frame = ttk.Frame(self.master, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Set background color for the frame
        frame.configure(style='TFrame')

        # Define a style for the frame
        style = ttk.Style()
        style.configure('TFrame', background='#2E2E2E')
        style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF')
        style.configure('TButton', background='#4B4B4B', foreground='#2E2E2E', borderwidth=0)
        style.configure('TRadiobutton', background='#2E2E2E', foreground='#FFFFFF', font=('Helvetica', 14))  # Increased font size for radio buttons

        # New style for time complexity label with larger font
        style.configure('TimeComplexity.TLabel', background='#2E2E2E', foreground='#FFFFFF', font=('Helvetica', 18))

        algorithms = [
            ("Bubble Sort", "bubblesort"),
            ("Selection Sort", "selectionsort"),
            ("Insertion Sort", "insertionsort"),
            ("Quick Sort", "quicksort"),
            ("Merge Sort", "mergesort"),
            ("Counting Sort", "countingsort"),
            ("Radix Sort", "radixsort"),
            ("Comb Sort", "combsort")
        ]

        for text, value in algorithms:
            ttk.Radiobutton(frame, text=text, variable=self.algorithm, value=value, command=self.algorithm_changed).pack(anchor=tk.W, padx=10, pady=5)

        self.visualize_button = ttk.Button(frame, text="Visualize", command=self.start_visualization)
        self.visualize_button.pack(pady=10)

        self.reset_button = ttk.Button(frame, text="Reset", command=self.reset_visualization)
        self.reset_button.pack(pady=10)

        # Add the new Compare button
        self.compare_button = ttk.Button(frame, text="Compare", command=self.open_compare_window)
        self.compare_button.pack(pady=10)

        # Add labels for time complexity and sorting time
        self.complexity_label = ttk.Label(frame, textvariable=self.time_complexity, style='TimeComplexity.TLabel')
        self.complexity_label.pack(pady=10)

        self.time_label = ttk.Label(frame, textvariable=self.sorting_time, style='TLabel')
        self.time_label.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        # Change the background of the plot area
        self.ax.set_facecolor('#2E2E2E')

    def choose_file(self):
        filename = filedialog.askopenfilename(
            title=f"Select {self.algorithm.get().replace('_', ' ').title()} Output File",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            try:
                self.sorting_steps = self.load_data(filename)
                self.data = self.sorting_steps[0]
                self.update_plot(self.data)
                messagebox.showinfo("File Loaded", f"Data loaded from {filename}")
                self.update_time_complexity()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def load_data(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        return [[int(x) for x in line.split()] for line in lines if line.strip()]

    def update_plot(self, data, highlights=None):
        self.ax.clear()

        # Set default color for all bars
        bars = self.ax.bar(range(len(data)), data, color='cyan', edgecolor='black', linewidth=0.5)

        if highlights:
            for i, color in highlights:
                bars[i].set_color(color)  # Change specific bar colors based on highlights
                bars[i].set_edgecolor('black')  # Ensure the edge color remains black for highlighted bars

        algorithm_name = self.algorithm.get().replace('_', ' ').title()
        font_size = 32 if len(algorithm_name) < 10 else 28
        self.ax.set_title(algorithm_name, fontsize=font_size)
        self.ax.set_ylim(0, max(data) * 1.1 if data else 1)
        self.canvas.draw()
        self.master.update()

    def start_visualization(self):
        if self.sorting_steps is None:
            messagebox.showwarning("No Data", "Please choose a file first.")
            return

        self.is_sorting = True
        self.visualize_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

        self.sort_thread = threading.Thread(target=self.visualize_sorting)
        self.sort_thread.start()

    def visualize_sorting(self):
        if not self.sorting_steps:
            return

        n = len(self.sorting_steps[0])
        previous_data = self.sorting_steps[0].copy()
        sorted_indices = set()

        start_time = time.time()

        for step, current_data in enumerate(self.sorting_steps):
            if not self.is_sorting:
                break

            highlights = [(i, 'cyan') for i in range(n)]  # Start with all bars cyan

            # Identify elements that have changed in this step
            changed_indices = [i for i in range(n) if current_data[i] != previous_data[i]]

            # Color changed elements red (currently being sorted)
            for i in changed_indices:
                highlights[i] = (i, 'red')
                sorted_indices.add(i)

            # Color previously sorted elements blue
            for i in sorted_indices - set(changed_indices):
                highlights[i] = (i, 'blue')

            self.master.after(0, self.update_plot, current_data, highlights)
            time.sleep(0.1)  # Simulate processing time

            previous_data = current_data.copy()

        # Ensure all elements are green at the end
        final_highlights = [(i, 'lime') for i in range(n)]
        self.master.after(0, self.update_plot, current_data, final_highlights)

        end_time = time.time()
        sorting_time = end_time - start_time
        self.sorting_time.set(f"Sorting Time: {sorting_time:.2f} seconds")

        self.is_sorting = False
        self.master.after(0, self.reset_buttons)

    def reset_buttons(self):
        self.visualize_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def algorithm_changed(self):
        if self.is_sorting:
            self.is_sorting = False
            self.master.after(0, self.stop_visualization_and_choose_file)
        else:
            self.choose_file()
        self.update_time_complexity()

    def stop_visualization_and_choose_file(self):
        self.is_sorting = False
        self.master.after(100, self.clean_up_and_choose_file)

    def clean_up_and_choose_file(self):
        if self.sort_thread and self.sort_thread.is_alive():
            self.master.after(100, self.clean_up_and_choose_file)
        else:
            # Clear existing data and update the plot
            self.sorting_steps = None
            self.data = None
            self.update_plot([])  # Reset the plot
            self.reset_buttons()

            # Reset time complexity and sorting time
            self.update_time_complexity()
            self.sorting_time.set("")

            # Prompt for a new file
            self.choose_file()

    def reset_visualization(self):
        self.is_sorting = False
        self.reset_button.config(state=tk.DISABLED)
        self.visualize_button.config(state=tk.DISABLED)
        self.master.after(0, self.perform_reset)

    def perform_reset(self):
        if self.sort_thread and self.sort_thread.is_alive():
            self.master.after(100, self.perform_reset)
        else:
            # Clear existing data and update the plot
            self.sorting_steps = None
            self.data = None
            self.update_plot([])  # Reset the plot
            self.reset_buttons()

            # Reset time complexity and sorting time
            self.update_time_complexity()
            self.sorting_time.set("")

            # Enable all algorithm radio buttons
            for child in self.master.winfo_children():
                if isinstance(child, ttk.Radiobutton):
                    child.config(state=tk.NORMAL)

            messagebox.showinfo("Reset", "Visualization has been reset. You can now select a new algorithm and file.")

    def open_compare_window(self):
        # Import the compare functionality from compare.py
        from compare import open_compare_dialog
        open_compare_dialog(self.master)

    def update_time_complexity(self):
        complexities = {
            "bubblesort": "O(n²)",
            "selectionsort": "O(n²)",
            "insertionsort": "O(n²)",
            "quicksort": "O(n log n)",
            "mergesort": "O(n log n)",
            "countingsort": "O(n + k)",
            "radixsort": "O(d(n + k))",
            "combsort": "O(n²)"
        }
        current_algorithm = self.algorithm.get()
        self.time_complexity.set(f"Time Complexity: {complexities.get(current_algorithm, 'Unknown')}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()