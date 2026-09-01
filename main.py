import customtkinter as ctk
from tkinter import filedialog, messagebox
from automation import organize_folder
import json
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BusinessFileAutomation(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Business File Automation")
        self.geometry("1100x700")
        self.minsize(950, 600)

        self.history_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "history.json"
        )

        self.selected_folder = ""

        self.last_stats = {
            "Documents": 0,
            "Images": 0,
            "Videos": 0,
            "Audio": 0,
            "Archives": 0,
            "Code": 0,
            "Others": 0
        }

        self.last_results = []

        self.load_history()
        self.create_interface()

        if self.selected_folder:
            self.folder_entry.insert(0, self.selected_folder)

    # ========================================================
    # HISTORIAL
    # ========================================================

    def save_history(self):
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "folder": self.selected_folder,
            "stats": self.last_stats,
            "total": sum(self.last_stats.values())
        }

        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as file:
                    history = json.load(file)
            else:
                history = []

            if not isinstance(history, list):
                history = []

            history.append(record)

            with open(self.history_file, "w", encoding="utf-8") as file:
                json.dump(history, file, indent=4, ensure_ascii=False)

        except Exception as error:
            print(f"History save error: {error}")

    def load_history(self):
        try:
            if not os.path.exists(self.history_file):
                return

            with open(self.history_file, "r", encoding="utf-8") as file:
                history = json.load(file)

            if not isinstance(history, list) or not history:
                return

            last_record = history[-1]

            self.selected_folder = last_record.get("folder", "")

            saved_stats = last_record.get("stats", {})

            if isinstance(saved_stats, dict):
                for category in self.last_stats:
                    self.last_stats[category] = int(
                        saved_stats.get(category, 0)
                    )

        except Exception as error:
            print(f"History load error: {error}")

    # ========================================================
    # INTERFAZ
    # ========================================================

    def create_interface(self):

        self.sidebar = ctk.CTkFrame(
            self, width=230, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Business\nAutomation",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo.pack(pady=(45, 50))

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            height=45,
            anchor="w",
            command=self.show_dashboard
        )
        self.dashboard_button.pack(padx=20, pady=8, fill="x")

        self.organizer_button = ctk.CTkButton(
            self.sidebar,
            text="File Organizer",
            height=45,
            anchor="w",
            command=self.show_organizer
        )
        self.organizer_button.pack(padx=20, pady=8, fill="x")

        self.reports_button = ctk.CTkButton(
            self.sidebar,
            text="Reports",
            height=45,
            anchor="w",
            command=self.show_reports
        )
        self.reports_button.pack(padx=20, pady=8, fill="x")

        self.separator = ctk.CTkFrame(self.sidebar, height=2)
        self.separator.pack(fill="x", padx=20, pady=30)

        self.info_label = ctk.CTkLabel(
            self.sidebar,
            text="Automation Suite\nVersion 1.0",
            text_color="gray",
            justify="left"
        )
        self.info_label.pack(padx=20, anchor="w")

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.content,
            text="Business File Automation",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        self.title_label.pack(anchor="w", padx=45, pady=(35, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.content,
            text="Automate repetitive file organization tasks.",
            font=ctk.CTkFont(size=15),
            text_color="gray"
        )
        self.subtitle_label.pack(anchor="w", padx=45)

        self.create_organizer_view()
        self.create_dashboard_view()

        self.update_dashboard()

    def create_organizer_view(self):

        self.organizer_view = ctk.CTkFrame(
            self.content, fg_color="transparent"
        )
        self.organizer_view.pack(fill="both", expand=True)

        self.main_card = ctk.CTkFrame(
            self.organizer_view, corner_radius=15
        )
        self.main_card.pack(fill="x", padx=45, pady=30)

        self.card_title = ctk.CTkLabel(
            self.main_card,
            text="File Organization",
            font=ctk.CTkFont(size=21, weight="bold")
        )
        self.card_title.pack(anchor="w", padx=30, pady=(25, 5))

        self.card_description = ctk.CTkLabel(
            self.main_card,
            text="Select a folder and let the application organize your files automatically.",
            text_color="gray"
        )
        self.card_description.pack(anchor="w", padx=30, pady=(0, 20))

        self.folder_frame = ctk.CTkFrame(
            self.main_card, fg_color="transparent"
        )
        self.folder_frame.pack(fill="x", padx=30, pady=10)

        self.folder_entry = ctk.CTkEntry(
            self.folder_frame,
            height=45,
            placeholder_text="No folder selected"
        )
        self.folder_entry.pack(
            side="left", fill="x", expand=True, padx=(0, 10)
        )

        self.browse_button = ctk.CTkButton(
            self.folder_frame,
            text="Browse",
            width=120,
            height=45,
            command=self.select_folder
        )
        self.browse_button.pack(side="right")

        self.organize_button = ctk.CTkButton(
            self.main_card,
            text="Organize Files",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.organize_files
        )
        self.organize_button.pack(
            fill="x", padx=30, pady=(20, 30)
        )

        self.status_label = ctk.CTkLabel(
            self.organizer_view,
            text="Ready to automate.",
            font=ctk.CTkFont(size=15)
        )
        self.status_label.pack(anchor="w", padx=45)

        self.progress = ctk.CTkProgressBar(
            self.organizer_view, height=12
        )
        self.progress.pack(
            fill="x", padx=45, pady=(15, 20)
        )
        self.progress.set(0)

        self.results_card = ctk.CTkFrame(
            self.organizer_view, corner_radius=15
        )
        self.results_card.pack(
            fill="both", expand=True, padx=45, pady=(0, 25)
        )

        self.results_title = ctk.CTkLabel(
            self.results_card,
            text="Automation Results",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.results_title.pack(
            anchor="w", padx=25, pady=(15, 10)
        )

        self.results_text = ctk.CTkTextbox(
            self.results_card, height=120
        )
        self.results_text.pack(
            fill="both", expand=True, padx=25, pady=(0, 15)
        )
        self.results_text.insert(
            "1.0", "No automation has been executed yet."
        )
        self.results_text.configure(state="disabled")

    def create_dashboard_view(self):

        self.dashboard_view = ctk.CTkFrame(
            self.content, fg_color="transparent"
        )

        self.dashboard_header = ctk.CTkLabel(
            self.dashboard_view,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.dashboard_header.pack(
            anchor="w", padx=45, pady=(25, 15)
        )

        self.total_card = ctk.CTkFrame(
            self.dashboard_view, corner_radius=15
        )
        self.total_card.pack(
            fill="x", padx=45, pady=(0, 15)
        )

        self.total_title = ctk.CTkLabel(
            self.total_card,
            text="TOTAL FILES ORGANIZED",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        self.total_title.pack(anchor="w", padx=25, pady=(18, 0))

        self.total_value = ctk.CTkLabel(
            self.total_card,
            text="0",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.total_value.pack(anchor="w", padx=25, pady=(0, 18))

        self.stats_grid = ctk.CTkFrame(
            self.dashboard_view, fg_color="transparent"
        )
        self.stats_grid.pack(fill="x", padx=45)

        self.stat_cards = {}

        categories = [
            ("Documents", ""),
            ("Images", ""),
            ("Videos", ""),
            ("Audio", ""),
            ("Archives", ""),
            ("Code", ""),
            ("Others", "")
        ]

        for index, (category, icon) in enumerate(categories):

            row = index // 4
            column = index % 4

            card = ctk.CTkFrame(
                self.stats_grid, corner_radius=12
            )
            card.grid(
                row=row, column=column,
                padx=6, pady=6, sticky="nsew"
            )

            self.stats_grid.grid_columnconfigure(
                column, weight=1
            )

            icon_label = ctk.CTkLabel(
                card, text=icon,
                font=ctk.CTkFont(size=22)
            )
            icon_label.pack(anchor="w", padx=15, pady=(12, 0))

            name_label = ctk.CTkLabel(
                card, text=category,
                text_color="gray",
                font=ctk.CTkFont(size=12)
            )
            name_label.pack(anchor="w", padx=15)

            value_label = ctk.CTkLabel(
                card, text="0",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            value_label.pack(
                anchor="w", padx=15, pady=(0, 12)
            )

            self.stat_cards[category] = value_label

        self.chart_card = ctk.CTkFrame(
            self.dashboard_view, corner_radius=15
        )
        self.chart_card.pack(
            fill="x", padx=45, pady=(20, 0)
        )

        self.chart_title = ctk.CTkLabel(
            self.chart_card,
            text="File Distribution",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.chart_title.pack(
            anchor="w", padx=25, pady=(18, 12)
        )

        self.chart_frame = ctk.CTkFrame(
            self.chart_card, fg_color="transparent"
        )
        self.chart_frame.pack(
            fill="x", padx=25, pady=(0, 20)
        )

        self.chart_bars = {}

        for category in self.last_stats.keys():

            row = ctk.CTkFrame(
                self.chart_frame, fg_color="transparent"
            )
            row.pack(fill="x", pady=4)

            label = ctk.CTkLabel(
                row, text=category, width=90, anchor="w"
            )
            label.pack(side="left")

            bar = ctk.CTkProgressBar(
                row, height=12
            )
            bar.pack(
                side="left", fill="x", expand=True, padx=10
            )
            bar.set(0)

            value = ctk.CTkLabel(
                row, text="0", width=40
            )
            value.pack(side="right")

            self.chart_bars[category] = (bar, value)

        self.dashboard_info = ctk.CTkFrame(
            self.dashboard_view, corner_radius=15
        )
        self.dashboard_info.pack(
            fill="both", expand=True, padx=45, pady=20
        )

        self.dashboard_folder_label = ctk.CTkLabel(
            self.dashboard_info,
            text="Last selected folder:\nNone",
            font=ctk.CTkFont(size=13),
            text_color="gray",
            justify="left"
        )
        self.dashboard_folder_label.pack(
            anchor="w", padx=25, pady=(20, 10)
        )

        self.dashboard_status_label = ctk.CTkLabel(
            self.dashboard_info,
            text="System status: WAITING",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.dashboard_status_label.pack(
            anchor="w", padx=25
        )

        self.dashboard_message_label = ctk.CTkLabel(
            self.dashboard_info,
            text="Select a folder to begin.",
            text_color="gray"
        )
        self.dashboard_message_label.pack(
            anchor="w", padx=25, pady=(0, 20)
        )

    # ========================================================
    # FUNCIONES
    # ========================================================

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.selected_folder = folder

            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

            self.status_label.configure(
                text="Folder selected. Ready to organize."
            )

    def organize_files(self):

        if not self.selected_folder:
            messagebox.showwarning(
                "Folder Required",
                "Please select a folder first."
            )
            return

        self.status_label.configure(
            text="Organizing files..."
        )
        self.progress.set(0.3)

        try:

            results, stats = organize_folder(
                self.selected_folder
            )

            self.last_stats = stats
            self.last_results = results

            self.save_history()

            self.progress.set(0.8)

            self.results_text.configure(
                state="normal"
            )
            self.results_text.delete(
                "1.0", "end"
            )

            self.results_text.insert(
                "end",
                "AUTOMATION SUMMARY\n"
            )
            self.results_text.insert(
                "end",
                "========================\n\n"
            )

            total_files = sum(stats.values())

            self.results_text.insert(
                "end",
                f"Total files organized: {total_files}\n\n"
            )

            for category, count in stats.items():
                self.results_text.insert(
                    "end",
                    f"{category}: {count}\n"
                )

            self.results_text.insert(
                "end",
                "\n------------------------\n\n"
            )
            self.results_text.insert(
                "end",
                "FILE DETAILS\n\n"
            )

            for result in results:
                self.results_text.insert(
                    "end",
                    result + "\n"
                )

            self.results_text.configure(
                state="disabled"
            )

            self.progress.set(1)

            self.status_label.configure(
                text="Automation completed successfully."
            )

            self.update_dashboard()

        except Exception as error:

            self.progress.set(0)
            self.status_label.configure(
                text="Automation failed."
            )

            messagebox.showerror(
                "Automation Error",
                str(error)
            )

    def update_dashboard(self):

        total_files = sum(
            self.last_stats.values()
        )

        self.total_value.configure(
            text=str(total_files)
        )

        for category, label in self.stat_cards.items():

            value = self.last_stats.get(
                category, 0
            )
            label.configure(
                text=str(value)
            )

        max_value = max(
            self.last_stats.values(),
            default=0
        )

        for category, widgets in self.chart_bars.items():

            bar, value_label = widgets

            value = self.last_stats.get(
                category, 0
            )

            percentage = (
                value / max_value
                if max_value > 0
                else 0
            )

            bar.set(percentage)
            value_label.configure(
                text=str(value)
            )

        if self.selected_folder:

            self.dashboard_folder_label.configure(
                text=(
                    "Last selected folder:\n"
                    f"{self.selected_folder}"
                )
            )

        else:

            self.dashboard_folder_label.configure(
                text="Last selected folder:\nNone"
            )

        if total_files > 0:

            self.dashboard_status_label.configure(
                text="System status: READY"
            )
            self.dashboard_message_label.configure(
                text="Last automation completed successfully."
            )

        else:

            self.dashboard_status_label.configure(
                text="System status: WAITING"
            )
            self.dashboard_message_label.configure(
                text="Select a folder to begin."
            )

    def show_dashboard(self):

        self.organizer_view.pack_forget()

        self.dashboard_view.pack(
            fill="both",
            expand=True
        )

        self.update_dashboard()

    def show_organizer(self):

        self.dashboard_view.pack_forget()

        self.organizer_view.pack(
            fill="both",
            expand=True
        )

        self.status_label.configure(
            text="File Organizer selected."
        )

    def show_reports(self):

        self.dashboard_view.pack_forget()

        self.organizer_view.pack(
            fill="both",
            expand=True
        )

        self.status_label.configure(
            text="Report generated."
        )

        self.results_text.configure(
            state="normal"
        )
        self.results_text.delete(
            "1.0", "end"
        )

        total_files = sum(
            self.last_stats.values()
        )

        self.results_text.insert(
            "end",
            "AUTOMATION REPORT\n"
        )
        self.results_text.insert(
            "end",
            "========================\n\n"
        )
        self.results_text.insert(
            "end",
            f"Total files organized: {total_files}\n\n"
        )

        for category, count in self.last_stats.items():
            self.results_text.insert(
                "end",
                f"{category}: {count}\n"
            )

        self.results_text.insert(
            "end",
            "\n========================\n"
        )

        if total_files == 0:

            self.results_text.insert(
                "end",
                "\nNo automation has been executed yet."
            )

        else:

            self.results_text.insert(
                "end",
                "\nStatus: COMPLETED\n"
            )
            self.results_text.insert(
                "end",
                "\nThe latest automation was completed successfully."
            )

        self.results_text.configure(
            state="disabled"
        )


if __name__ == "__main__":
    app = BusinessFileAutomation()
    app.mainloop()



