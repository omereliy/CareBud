import tkinter as tk
from tkinter import ttk
from logic_layer.control_unit.control_unit import ControlUnit
from configs.config_constants import state_to_color


# Define the ControlUnitUI class to accept a ControlUnit instance
class ControlUnitUI:
    def __init__(self, controller: ControlUnit, root):
        self.controller = controller  # Use the provided control unit instance
        self.controller.ui_reference = self
        self.root = root
        self.root.title("Patient Monitoring System")
        self.root.configure(bg="#1c1c1c")  # Darker background for modern look

        # Set dark mode colors and styles
        bg_color = "#1c1c1c"
        fg_color = "#e6e6e6"  # Softer light color for better readability
        button_color = "#3a3a3a"
        button_hover_color = "#555555"
        table_header_bg = "#2a2a2a"
        table_header_fg = "#e6e6e6"
        table_row_bg = "#333333"
        table_row_fg = "#e6e6e6"

        style = ttk.Style(root)
        style.theme_use("clam")  # Modern theme with better aesthetics
        style.configure("Treeview", background=table_row_bg, foreground=table_row_fg, rowheight=28,
                        fieldbackground=table_row_bg, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=table_header_bg, foreground=table_header_fg,
                        font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#464646")])

        # Set up the patient table
        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)  # Increased padding for a cleaner look

        # Updated columns to include "Head Injury"
        columns = ("Patient", "Pulse", "Blood Pressure", "Saturation", "Status", "TBI")
        self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, minwidth=0, width=120, anchor="center")  # Center-align for neatness

        self.table.pack(padx=10, pady=10, fill="both", expand=True)
        self.update_table()

        # Control Buttons with enhanced styling
        button_frame = tk.Frame(root, bg=bg_color)
        button_frame.pack(pady=20)

        for text, command in [("Previous Patient", self.decrement_observed),
                              ("Next Patient", self.increment_observed),
                              ("Show Full Record", self.show_record)]:
            button = tk.Button(button_frame, text=text, command=command, bg=button_color, fg=fg_color,
                               font=("Segoe UI", 10, "bold"), relief="groove", padx=10, pady=8,
                               activebackground=button_hover_color, activeforeground=fg_color)
            button.pack(side="left", padx=10)

        # Labels for observed patient and total patients
        self.current_patient_label = tk.Label(button_frame,
                                              text=f"Observed Patient: {self.controller.obs_bracelet.num + 1}",
                                              font=("Segoe UI", 10, "bold"), bg=bg_color, fg=fg_color)
        self.current_patient_label.pack(side="left", padx=20)  # Added space to the left for separation

        self.total_patients_label = tk.Label(button_frame,
                                             text=f"Total Patients: {len(self.controller.paired_bracelets)}",
                                             font=("Segoe UI", 10, "bold"), bg=bg_color, fg=fg_color)
        self.total_patients_label.pack(side="left", padx=20)  # Added space to the left for separation

        # Head Injury Checkbutton
        self.head_injury_var = tk.BooleanVar()
        self.head_injury_checkbutton = tk.Checkbutton(
            button_frame, text="Head Injury", variable=self.head_injury_var,
            command=self.toggle_head_injury, bg=bg_color, fg=fg_color,
            font=("Segoe UI", 10, "bold"), selectcolor="#464646",
            activebackground=button_hover_color, activeforeground=fg_color
        )
        self.head_injury_checkbutton.pack(side="left", padx=20)

        # Start the UI auto-refresh loop
        self.refresh_ui()

    # Function to display all patient statuses in a table
    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for bracelet in self.controller.paired_bracelets:
            color = state_to_color(bracelet.get_state(), bracelet.is_head_injured)
            head_injury_status = "Yes" if bracelet.is_head_injured else "No"
            self.table.insert("", "end", values=(
                bracelet.num + 1,
                bracelet.pulse,
                bracelet.blood_pressure,
                bracelet.saturation,
                color.name,
                head_injury_status
            ))

    # Periodically refresh the UI to show live updates
    def refresh_ui(self):
        self.update_table()
        self.current_patient_label.config(text=f"Observed Patient: {self.controller.obs_bracelet.num + 1}")
        self.total_patients_label.config(text=f"Total Patients: {len(self.controller.paired_bracelets)}")
        self.head_injury_var.set(self.controller.obs_bracelet.is_head_injured)
        self.root.after(1000, self.refresh_ui)  # Refresh every second

    # Display the full record of the observed bracelet
    def show_record(self):
        observed_bracelet = self.controller.obs_bracelet
        record = self.controller.obs_bracelet.get_record()
        record.columns = record.columns.astype(str)

        # Create a new window for the record display
        record_window = tk.Toplevel(self.root)
        record_window.title(f"Patient {observed_bracelet.num + 1} Full Record")
        record_window.configure(bg="#1c1c1c")

        # Header label
        header = tk.Label(record_window, text=f"Patient {observed_bracelet.num + 1} Record",
                          font=("Segoe UI", 14, "bold"),
                          bg="#1c1c1c", fg="#e6e6e6")
        header.pack(pady=15)

        # Treeview for record, updated to include Head Injury status
        record_columns = list(record.columns) + ["Head Injury"]
        record_tree = ttk.Treeview(record_window, columns=record_columns, show="headings", style="Treeview")

        for col in record_columns:
            record_tree.heading(col, text=col)
            record_tree.column(col, width=150, anchor="center")

        for _, row in record.iterrows():
            # Adding head injury status in each row for the observed patient
            record_tree.insert("",
                               "end",
                               values=(*tuple(row), "Yes" if observed_bracelet.is_head_injured else "No"))

        record_tree.pack(padx=15, pady=15, fill="both", expand=True)

    # Switch observed bracelet
    def increment_observed(self):
        self.controller.increment_bracelet_index()
        self.refresh_ui()

    def decrement_observed(self):
        self.controller.decrement_bracelet_index()
        self.refresh_ui()

    def toggle_head_injury(self):
        self.controller.obs_bracelet.toggle_is_head_injured()
