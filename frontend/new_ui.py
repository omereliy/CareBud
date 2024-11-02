import tkinter as tk
from tkinter import ttk, messagebox
from logic_layer.control_unit.control_unit import ControlUnit
from configs.config_constants import state_to_color


def open_threshold_page(patient_id):
    messagebox.showinfo("Thresholds", f"Thresholds page for Patient {patient_id + 1}.")


class ControlUnitUI:
    def __init__(self, controller: ControlUnit, root):
        self.controller = controller
        self.controller.ui_reference = self
        self.root = root
        self.root.title("Patient Monitoring System")
        self.root.configure(bg="#1c1c1c")

        # Create a canvas to hold the scrollable frame
        self.canvas = tk.Canvas(self.root, bg="#1c1c1c")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1c1c1c")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enable scrolling with the mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.patient_frames = []  # Track patient frames and labels for selective updates
        self.patient_labels = []  # Store labels for pulse, saturation, and bp
        self.tbi_labels = []  # Store TBI labels for selective updates
        self.tbi_buttons = []  # Store TBI toggle buttons for update states

        # Dynamically adjust window size based on number of patient frames
        self.adjust_window_size()
        self.create_patient_frames()
        self.root.bind("<Configure>", self.on_window_resize)

    def _on_mousewheel(self, event):
        """Enable scrolling with the mouse wheel."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def adjust_window_size(self):
        num_patients = len(self.controller.paired_bracelets)
        height = (num_patients // 3 + 1) * 250  # Calculate height based on patient rows
        self.root.geometry(f"600x{min(height, 600)}")  # Set a max initial height

    def on_window_resize(self, event):
        """Rearrange the patient frames when the window is resized."""
        frame_width = 200  # Width of each patient frame including padding
        min_spacing = 20  # Adjust spacing as needed
        scrollbar_width = self.scrollbar.winfo_width() if self.scrollbar.winfo_ismapped() else 0
        available_width = self.root.winfo_width() - scrollbar_width  # Adjust to account for any side padding

        columns = max(1, available_width // (frame_width + min_spacing))

        for i, patient_frame in enumerate(self.patient_frames):
            row = i // columns
            column = i % columns
            patient_frame.grid_configure(row=row, column=column)

        # Ensure the canvas scroll region is updated to reflect the new arrangement
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_patient_frames(self):
        for i, bracelet in enumerate(self.controller.paired_bracelets):
            frame = self.create_patient_frame(i, bracelet)
            self.patient_frames.append(frame)

    def create_patient_frame(self, index, bracelet):
        color = state_to_color(bracelet.get_state(), bracelet.is_head_injured)
        frame_border_color = "#AB3838" if color.name == "RED" else "#273D51"

        patient_frame = tk.Frame(
            self.scrollable_frame, bg="#1A2937", highlightthickness=2,
            highlightbackground=frame_border_color, width=300, height=150
        )
        patient_frame.grid(row=index // 3, column=index % 3, padx=10, pady=10, sticky="nsew")

        # Display patient information
        patient_label = tk.Label(
            patient_frame, text=f"Patient {bracelet.num + 1}",
            font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#1A2937", anchor="w"
        )
        patient_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        if bracelet.is_head_injured:
            tbi_label = tk.Label(
                patient_frame, text="TBI", font=("Segoe UI", 10, "bold"), fg="#AB3838", bg="#1A2937"
            )
            tbi_label.grid(row=0, column=1, padx=5, sticky="e")
            self.tbi_labels.append(tbi_label)
        else:
            self.tbi_labels.append(None)

        pulse_label = tk.Label(
            patient_frame, text=f"Pulse: {bracelet.pulse}", font=("Segoe UI", 12), fg="#FFFFFF",
            bg="#1A2937", anchor="w"
        )
        pulse_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        saturation_label = tk.Label(
            patient_frame, text=f"Saturation: {bracelet.saturation}%", font=("Segoe UI", 12), fg="#FFFFFF",
            bg="#1A2937", anchor="w"
        )
        saturation_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        bp_label = tk.Label(
            patient_frame, text=f"BP: {bracelet.blood_pressure}", font=("Segoe UI", 12), fg="#FFFFFF",
            bg="#1A2937", anchor="w"
        )
        bp_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.patient_labels.append((pulse_label, saturation_label, bp_label))

        # Add buttons for thresholds and records
        threshold_button = tk.Button(
            patient_frame, text="Thresholds", font=("Segoe UI", 9, "bold"),
            command=lambda pid=bracelet.num: open_threshold_page(pid), bg="#34495E", fg="#FFFFFF",
            relief="flat", activebackground="#5D6D7E"
        )
        threshold_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        record_button = tk.Button(
            patient_frame, text="Record", font=("Segoe UI", 9, "bold"),
            command=lambda pid=bracelet.num: self.show_record(pid), bg="#34495E", fg="#FFFFFF",
            relief="flat", activebackground="#5D6D7E"
        )
        record_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Add a toggle button to update head injury state with better design
        tbi_var = tk.BooleanVar(value=bracelet.is_head_injured)
        tbi_switch_button = tk.Checkbutton(
            patient_frame, text="TBI", font=("Segoe UI", 9, "bold"), variable=tbi_var,
            command=lambda pid=bracelet.num: self.toggle_tbi(pid, tbi_var),
            bg="#2C3E50", fg="#FFFFFF", selectcolor="#AB3838",
            indicatoron=False, relief="flat", activebackground="#5D6D7E"
        )
        tbi_switch_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.tbi_buttons.append(tbi_switch_button)

        patient_frame.grid_columnconfigure(0, weight=1)
        patient_frame.grid_columnconfigure(1, weight=1)

        return patient_frame

    def on_data_change(self, changed_index):
        """Update only the labels, TBI warning, and frame border color of the changed patient frame."""
        bracelet = self.controller.paired_bracelets[changed_index]
        pulse_label, saturation_label, bp_label = self.patient_labels[changed_index]

        # Update the text of the labels
        pulse_label.config(text=f"Pulse: {bracelet.pulse}")
        saturation_label.config(text=f"Saturation: {bracelet.saturation}%")
        bp_label.config(text=f"BP: {bracelet.blood_pressure}")

        # Update the TBI label
        if bracelet.is_head_injured and not self.tbi_labels[changed_index]:
            tbi_label = tk.Label(
                self.patient_frames[changed_index], text="TBI", font=("Segoe UI", 10, "bold"),
                fg="#AB3838", bg="#1A2937"
            )
            tbi_label.grid(row=0, column=1, padx=5, sticky="e")
            self.tbi_labels[changed_index] = tbi_label
        elif not bracelet.is_head_injured and self.tbi_labels[changed_index]:
            self.tbi_labels[changed_index].destroy()
            self.tbi_labels[changed_index] = None

        # Update the frame border color based on the patient's status
        color = state_to_color(bracelet.get_state(), bracelet.is_head_injured)
        frame_border_color = "#AB3838" if color.name == "RED" else "#273D51"
        self.patient_frames[changed_index].config(highlightbackground=frame_border_color)

    def toggle_tbi(self, patient_id, tbi_var):
        """Toggle the TBI status of the patient and notify the ControlUnit."""
        bracelet = self.controller.paired_bracelets[patient_id]
        bracelet.is_head_injured = tbi_var.get()
        self.on_data_change(patient_id)  # Notify ControlUnit of the change

    def show_record(self, patient_id):
        observed_bracelet = self.controller.paired_bracelets[patient_id]
        record = observed_bracelet.get_record()
        record.columns = record.columns.astype(str)

        record_window = tk.Toplevel(self.root)
        record_window.title(f"Patient {patient_id + 1} Full Record")
        record_window.configure(bg="#1c1c1c")

        header = tk.Label(record_window, text=f"Patient {patient_id + 1} Record",
                          font=("Segoe UI", 14, "bold"), bg="#1c1c1c", fg="#e6e6e6")
        header.pack(pady=15)

        record_columns = list(record.columns)
        record_tree = ttk.Treeview(record_window, columns=record_columns, show="headings", style="Treeview")

        for col in record_columns:
            record_tree.heading(col, text=col)
            record_tree.column(col, width=150, anchor="center")

        for _, row in record.iterrows():
            record_tree.insert("", "end", values=tuple(row))

        record_tree.pack(padx=15, pady=15, fill="both", expand=True)
