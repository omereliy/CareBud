import tkinter as tk
from tkinter import ttk
from control_unit import ControlUnit
from config_constants import state_to_color


# Define the ControlUnitUI class to accept a ControlUnit instance
class ControlUnitUI:
    def __init__(self, control_unit: ControlUnit, root):
        self.control_unit = control_unit  # Use the provided control unit instance
        self.root = root
        self.root.title("Patient Monitoring System")
        self.root.configure(bg="#2e2e2e")  # Dark background

        # Set dark mode colors and styles
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        button_color = "#4a4a4a"
        table_header_bg = "#3a3a3a"
        table_header_fg = "#ffffff"
        table_row_bg = "#404040"
        table_row_fg = "#ffffff"

        style = ttk.Style(root)
        style.theme_use("default")
        style.configure("Treeview", background=table_row_bg, foreground=table_row_fg, rowheight=25,
                        fieldbackground=table_row_bg)
        style.configure("Treeview.Heading", background=table_header_bg, foreground=table_header_fg,
                        font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#565656")])

        # Set up the patient table
        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(pady=10)

        columns = ("Patient", "Pulse", "Blood Pressure", "Saturation", "Status")
        self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, minwidth=0, width=120)

        self.table.pack(padx=10, pady=10)
        self.update_table()

        # Control Buttons with styling
        button_frame = tk.Frame(root, bg=bg_color)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Previous Patient", command=self.decrement_observed, bg=button_color, fg=fg_color,
                  font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(button_frame, text="Next Patient", command=self.increment_observed, bg=button_color, fg=fg_color,
                  font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(button_frame, text="Show Full Record", command=self.show_record, bg=button_color, fg=fg_color,
                  font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5).pack(side="left", padx=5)

        # Start the UI auto-refresh loop
        self.refresh_ui()

    # Function to display all patient statuses in a table
    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for bracelet in self.control_unit.paired_bracelets:
            color = state_to_color(bracelet.get_state())
            self.table.insert("", "end", values=(
                bracelet.num + 1,
                bracelet.pulse,
                bracelet.blood_pressure,
                bracelet.saturation,
                color.name
            ))

    # Periodically refresh the UI to show live updates
    def refresh_ui(self):
        self.update_table()
        self.root.after(1000, self.refresh_ui)  # Refresh every second

    # Display the full record of the observed bracelet
    def show_record(self):
        observed_bracelet = self.control_unit.obs_bracelet
        record = observed_bracelet.get_record()
        record.columns = record.columns.astype(str)

        # Create a new window for the record display
        record_window = tk.Toplevel(self.root)
        record_window.title(f"Patient {observed_bracelet.num + 1} Full Record")
        record_window.configure(bg="#2e2e2e")

        # Header label
        header = tk.Label(record_window, text=f"Patient {observed_bracelet.num + 1} Record", font=("Arial", 14, "bold"),
                          bg="#2e2e2e", fg="#ffffff")
        header.pack(pady=10)

        # Treeview for record
        record_tree = ttk.Treeview(record_window, columns=list(record.columns), show="headings", style="Treeview")

        for col in record.columns:
            record_tree.heading(col, text=col)
            record_tree.column(col, width=120)

        for _, row in record.iterrows():
            record_tree.insert("", "end", values=tuple(row))

        record_tree.pack(padx=10, pady=10)

    # Switch observed bracelet
    def increment_observed(self):
        self.control_unit.increment_bracelet_index()
        self.update_table()

    def decrement_observed(self):
        self.control_unit.decrement_bracelet_index()
        self.update_table()
