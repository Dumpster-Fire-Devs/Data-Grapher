import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import statistics

class StatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statistical Analysis and Plotting")
        
        self.data = []
        self.units = "units"
        self.variables = ""
        self.title = ""
        self.current_canvas = None

        self.setup_gui()

    def setup_gui(self):
        # Add scrollbar to the main frame
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.main_frame = ttk.Frame(self.canvas, padding="10")
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Configure root window resizing
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(5, weight=1)

        # Unit selection frame
        self.unit_frame = ttk.LabelFrame(self.main_frame, text="Select Units", padding="10")
        self.unit_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Label(self.unit_frame, text="Units:").grid(row=0, column=0, sticky=tk.W)
        self.unit_var = tk.StringVar()
        self.unit_var.set("units")
        self.unit_options = ttk.Combobox(self.unit_frame, textvariable=self.unit_var, values=[
            "units", "cm", "m", "mm", "km", "in", "ft", "yd", "mile", "mg", "g", "kg", "ton", "oz", "lb", "ml", "l", "gal", "psi", "Pa", "bar", "atm", "C", "F", "K", "s", "min", "h",
            "m/s", "km/h", "mph", "m/s²", "kg/m³", "N", "J", "W", "Hz", "V", "A", "Ω", "F", "T", "H", "Bq", "Gy", "Sv", "lx", "lm", "cd", "mol", "m²", "m³", "L/min", "W/m²", "Pa·s", "m·s", "s²"
        ])
        self.unit_options.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.unit_options.config(state='readonly')

        ttk.Label(self.unit_frame, text="Custom Unit:").grid(row=1, column=0, sticky=tk.W)
        self.custom_unit_entry = ttk.Entry(self.unit_frame, width=20)
        self.custom_unit_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Variable and title input frame
        self.var_title_frame = ttk.LabelFrame(self.main_frame, text="Variables and Title", padding="10")
        self.var_title_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(self.var_title_frame, text="Variable:").grid(row=0, column=0, sticky=tk.W)
        self.var_entry = ttk.Entry(self.var_title_frame, width=20)
        self.var_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.var_title_frame, text="Title:").grid(row=1, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(self.var_title_frame, width=20)
        self.title_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Data input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Add Trial Data", padding="10")
        self.input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(self.input_frame, text="Enter trial value:").grid(row=0, column=0, sticky=tk.W)
        self.value_entry = ttk.Entry(self.input_frame, width=20)
        self.value_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(self.input_frame, text="Add", command=self.add_value).grid(row=0, column=2, padx=5)

        # Statistics frame
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Statistics", padding="10")
        self.stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)

        self.stats_labels = {
            "Mean": ttk.Label(self.stats_frame, text="Mean: -"),
            "Median": ttk.Label(self.stats_frame, text="Median: -"),
            "Mode": ttk.Label(self.stats_frame, text="Mode: -"),
            "Range": ttk.Label(self.stats_frame, text="Range: -"),
        }

        for i, key in enumerate(self.stats_labels.keys()):
            self.stats_labels[key].grid(row=i, column=0, sticky=tk.W)

        # Graphs frame
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Graphs", padding="10")
        self.graph_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(self.graph_frame, text="Select Graph Type:").grid(row=0, column=0, sticky=tk.W)
        self.graph_var = tk.StringVar()
        self.graph_options = ttk.Combobox(self.graph_frame, textvariable=self.graph_var, values=[
            "Line Graph", "Bar Graph", "Histogram", "Scatter Plot", "Pie Chart"
        ])
        self.graph_options.grid(row=0, column=1, padx=5, pady=5)
        self.graph_options.config(state='readonly')

        ttk.Button(self.graph_frame, text="Plot Graph", command=self.plot_selected_graph).grid(row=0, column=2, padx=5)
        ttk.Button(self.graph_frame, text="Save Graph", command=self.save_graph).grid(row=0, column=3, padx=5)

    def add_value(self):
        try:
            value = float(self.value_entry.get())
            self.data.append(value)
            self.value_entry.delete(0, tk.END)
            self.update_statistics()
            if self.current_canvas:
                self.current_canvas.get_tk_widget().destroy()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def update_statistics(self):
        if self.data:
            self.stats_labels["Mean"].config(text=f"Mean: {statistics.mean(self.data):.2f}")
            self.stats_labels["Median"].config(text=f"Median: {statistics.median(self.data):.2f}")
            try:
                mode = statistics.mode(self.data)
            except statistics.StatisticsError:
                mode = "No unique mode"
            self.stats_labels["Mode"].config(text=f"Mode: {mode}")
            self.stats_labels["Range"].config(text=f"Range: {max(self.data) - min(self.data):.2f}")

    def plot_selected_graph(self):
        if not self.data:
            messagebox.showerror("No data", "Please add data to plot.")
            return
        
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
        
        graph_type = self.graph_var.get()
        if graph_type == "Line Graph":
            self.plot_line_graph()
        elif graph_type == "Bar Graph":
            self.plot_bar_graph()
        elif graph_type == "Histogram":
            self.plot_histogram()
        elif graph_type == "Scatter Plot":
            self.plot_scatter_plot()
        elif graph_type == "Pie Chart":
            self.plot_pie_chart()
        else:
            messagebox.showerror("Invalid selection", "Please select a valid graph type.")

    def plot_graph(self, plot_func):
        if not self.data:
            messagebox.showerror("No data", "Please add data to plot.")
            return
        
        fig, ax = plt.subplots()
        plot_func(ax)
        ax.set_title(self.title_entry.get() or "Graph")
        ax.set_xlabel(self.var_entry.get() or "X")
        ax.set_ylabel(f"Values ({self.unit_var.get()})")

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_line_graph(self):
        def plot(ax):
            ax.plot(self.data, marker='o', linestyle='-')
        self.plot_graph(plot)

    def plot_bar_graph(self):
        def plot(ax):
            ax.bar(range(len(self.data)), self.data)
        self.plot_graph(plot)

    def plot_histogram(self):
        def plot(ax):
            ax.hist(self.data, bins='auto', alpha=0.7, rwidth=0.85)
        self.plot_graph(plot)

    def plot_scatter_plot(self):
        def plot(ax):
            ax.scatter(range(len(self.data)), self.data)
        self.plot_graph(plot)

    def plot_pie_chart(self):
        def plot(ax):
            ax.pie(self.data, labels=[f"{i+1}" for i in range(len(self.data))], autopct='%1.1f%%')
        self.plot_graph(plot)

    def save_graph(self):
        if not self.current_canvas:
            messagebox.showerror("No graph", "Please plot a graph to save.")
            return

        filetypes = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ]
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
        if filepath:
            self.current_canvas.figure.savefig(filepath)

    def edit_value(self, idx):
        def save_edited_value():
            try:
                new_value = float(entry.get())
                self.data[idx] = new_value
                self.update_statistics()
                if self.current_canvas:
                    self.plot_selected_graph()
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter a valid number.")
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Value")
        
        tk.Label(edit_window, text=f"Current Value: {self.data[idx]}").pack(padx=10, pady=10)
        entry = tk.Entry(edit_window)
        entry.pack(padx=10, pady=10)
        
        tk.Button(edit_window, text="Save", command=save_edited_value).pack(pady=10)

    def create_edit_buttons(self):
        for i, _ in enumerate(self.data):
            button = ttk.Button(self.main_frame, text=f"Edit Value {i+1}", command=lambda idx=i: self.edit_value(idx))
            button.grid(row=5+i, column=0, sticky=(tk.W, tk.E), pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = StatsApp(root)
    root.mainloop()
