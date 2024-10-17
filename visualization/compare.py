import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class ComparisonVisualizer:
    def __init__(self, master, algorithm1, algorithm2):
        self.master = master
        self.master.title(f"Comparing {algorithm1} vs {algorithm2}")
        self.master.configure(bg='#2E2E2E')  # Set background color

        self.algorithm1 = algorithm1
        self.algorithm2 = algorithm2
        
        self.data1 = None
        self.data2 = None
        self.sorting_steps1 = None
        self.sorting_steps2 = None
        self.is_sorting = False
        self.visualization_step = 0

        self.create_widgets()
        self.time_complexities = {
            "bubblesort": "O(n^2)",
            "selectionsort": "O(n^2)",
            "insertionsort": "O(n^2)",
            "quicksort": "O(n log n)",
            "mergesort": "O(n log n)",
            "countingsort": "O(n + k)",
            "radixsort": "O(nk)",
            "combsort": "O(n^2 / log n)"
        }

    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        # Create two separate frames for each algorithm
        frame1 = ttk.Frame(self.master, padding="10", style='TFrame')
        frame1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        frame2 = ttk.Frame(self.master, padding="10", style='TFrame')
        frame2.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set the style for the frames
        style = ttk.Style()
        style.configure('TFrame', background='#2E2E2E')
        style.configure('TLabel', background='#2E2E2E', foreground='white')

        # Create labels for algorithm names
        self.algorithm_label1 = ttk.Label(frame1, text=self.algorithm1, font=("Helvetica", 28, "bold"))
        self.algorithm_label1.pack(pady=5)  # Add some padding for better spacing

        self.algorithm_label2 = ttk.Label(frame2, text=self.algorithm2, font=("Helvetica", 28, "bold"))
        self.algorithm_label2.pack(pady=5)  # Add some padding for better spacing

        # Create plots for each algorithm
        self.fig1, self.ax1 = plt.subplots(figsize=(6, 4))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=frame1)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.pack(fill=tk.BOTH, expand=True)

        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=frame2)
        self.canvas_widget2 = self.canvas2.get_tk_widget()
        self.canvas_widget2.pack(fill=tk.BOTH, expand=True)

        # Set titles for each plot
        self.ax1.set_title(self.algorithm1)
        self.ax2.set_title(self.algorithm2)

        # Set background color for plots
        self.ax1.set_facecolor('#2E2E2E')
        self.ax2.set_facecolor('#2E2E2E')

        # Create labels for time complexity
        self.time_label1 = ttk.Label(frame1, text="Time complexity: ", font=("Helvetica", 18))
        self.time_label1.pack()

        self.time_label2 = ttk.Label(frame2, text="Time complexity: ", font=("Helvetica", 18))
        self.time_label2.pack()

        # Create a frame for buttons
        button_frame = ttk.Frame(self.master, style='TFrame')
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Create a button to start visualization
        self.visualize_button = ttk.Button(button_frame, text="Visualize", command=self.start_visualization)
        self.visualize_button.pack(side=tk.LEFT, padx=5)

        # Create a button to reset visualization
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_visualization, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        return [[int(x) for x in line.split()] for line in lines if line.strip()]

    def update_plot(self, ax, canvas, data, highlights=None):
        ax.clear()
        bars = ax.bar(range(len(data)), data, color='cyan', edgecolor='black', linewidth=0.5)

        if highlights:
            for i, color in highlights:
                bars[i].set_color(color)
                bars[i].set_edgecolor('black')  # Set the edge color to black

        ax.set_ylim(0, max(data) * 1.1 if data else 1)
        canvas.draw()

    def set_all_bars_color(self, ax, canvas, color):
        for bar in ax.patches:
            bar.set_color(color)
            bar.set_edgecolor('black')  # Set the edge color to black
        canvas.draw()

    def start_visualization(self):
        if self.sorting_steps1 is None or self.sorting_steps2 is None:
            messagebox.showwarning("No Data", "Please choose files for both algorithms first.")
            return

        self.is_sorting = True
        self.visualize_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.visualization_step = 0
        
        # Start visualizing both algorithms
        self.visualize_algorithm(self.algorithm1, self.sorting_steps1, self.ax1, self.canvas1, self.time_label1)
        self.visualize_algorithm(self.algorithm2, self.sorting_steps2, self.ax2, self.canvas2, self.time_label2)

    def visualize_algorithm(self, algorithm, sorting_steps, ax, canvas, time_label):
        start_time = time.time()
        n = len(sorting_steps[0])
        previous_data = sorting_steps[0].copy()
        sorted_indices = set()

        def step_visualization(step):
            if step < len(sorting_steps):
                current_data = sorting_steps[step]

                highlights = [(i, 'cyan') for i in range(n)]

                changed_indices = [i for i in range(n) if current_data[i] != previous_data[i]]

                for i in changed_indices:
                    highlights[i] = (i, 'red')
                    sorted_indices.add(i)

                for i in sorted_indices - set(changed_indices):
                    highlights[i] = (i, 'blue')

                self.update_plot(ax, canvas, current_data, highlights)
                self.master.update_idletasks()  # Allow GUI to update
                self.master.after(50, step_visualization, step + 1)

                previous_data[:] = current_data
            else:
                time_taken = time.time() - start_time
                time_label.config(text=f"Time complexity: {self.time_complexities[algorithm]} - {time_taken:.2f} seconds", font=("Helvetica", 18))
                self.set_all_bars_color(ax, canvas, 'lime')
                self.is_sorting = False
                self.reset_button.config(state=tk.NORMAL)

        self.master.after(0, step_visualization, 0)

    def reset_visualization(self):
        # Clear plots
        self.ax1.clear()
        self.ax2.clear()
        self.canvas1.draw()
        self.canvas2.draw()

        # Reset labels
        self.time_label1.config(text="Time complexity: ")
        self.time_label2.config(text="Time complexity: ")

        # Enable visualize button and disable reset button
        self.visualize_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

def open_compare_dialog(parent):
    dialog = tk.Toplevel(parent)
    dialog.title("Choose Algorithms to Compare")
    dialog.geometry("200x200")
    dialog.configure(bg='#2E2E2E')  # Set background color
    algorithms = ["bubblesort", "selectionsort", "insertionsort", "quicksort", "mergesort", "countingsort", "radixsort", "combsort"]

    algorithm1 = tk.StringVar(value=algorithms[0])
    algorithm2 = tk.StringVar(value=algorithms[1])

    ttk.Label(dialog, text="Choose first algorithm:", background='#2E2E2E', foreground='white').pack(pady=5)
    ttk.Combobox(dialog, textvariable=algorithm1, values=algorithms).pack(pady=5)

    ttk.Label(dialog, text="Choose second algorithm:", background='#2E2E2E', foreground='white').pack(pady=5)
    ttk.Combobox(dialog, textvariable=algorithm2, values=algorithms).pack(pady=5)

    def choose_files():
        if algorithm1.get() == algorithm2.get():
            messagebox.showerror("Error", "Please choose two different algorithms.")
            return

        file1 = filedialog.askopenfilename(title=f"Select file for {algorithm1.get()}", filetypes=[("Text files", "*.txt")])
        file2 = filedialog.askopenfilename(title=f"Select file for {algorithm2.get()}", filetypes=[("Text files", "*.txt")])

        if file1 and file2:
            dialog.destroy()
            comparison_window = tk.Toplevel(parent)
            app = ComparisonVisualizer(comparison_window, algorithm1.get(), algorithm2.get())

            try:
                app.sorting_steps1 = app.load_data(file1)
                app.sorting_steps2 = app.load_data(file2)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load data: {e}")

    ttk.Button(dialog, text="Compare", command=choose_files).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x600")
    root.configure(bg='#2E2E2E')  # Set background color
    ttk.Button(root, text="Start Comparison", command=lambda: open_compare_dialog(root)).pack(pady=20)
    root.mainloop()