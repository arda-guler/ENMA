import tkinter as tk
from tkinter import ttk
import sys

import nozzle_design
from unit_converter import *

head_offset = 5
N_entries = 0
abs_column = 0

entries = []
text_entries = []
entry_unit_vars = []

def is_run_from_idle():
    return bool("idlelib" in sys.modules)

if is_run_from_idle():
    print("Please do not run the program on IDLE. Use the terminal/cmd instead.")
    quit()

class entry:
    def __init__(self, entry_field, entry_label, unit_field, unit_type):
        self.entry_field = entry_field
        self.entry_label = entry_label
        self.unit_field = unit_field
        self.unit_type = unit_type

    def get_value(self):
        if not self.entry_field.get("1.0", "end-1c") == "":
            if self.unit_type == "float":
                return float(self.entry_field.get("1.0", "end-1c"))
            elif self.unit_type == "int":
                return int(float(self.entry_field.get("1.0", "end-1c")))
            elif self.unit_type == "string":
                return self.entry_field.get("1.0", "end-1c")
        else:
            return None

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

def show_about():
    about_win = tk.Toplevel()
    about_win.title("About ENMA")
    about_text = "Empirical Nozzle optimization & Mach distribution Analysis\n"
    about_text += "Thrust-optimized bell nozzle design using Rao's method and Mach distribution computer.\n"
    about_text += "Written by H. A. Güler (arda-guler @ Github). All rights reserved.\n\n"
    about_text += "The software is provided as-is, without warranty of any kind, express or implied.\n"
    about_text += "Analysis results are preliminary, and variations from experimental results should be expected."
    about_label = tk.Label(about_win, text=about_text)
    about_label.pack()

def create_entry(label, units, unit_type):
    global N_entries, entries, head_offset, text_entries, entry_unit_vars

    abs_offset = head_offset + N_entries

    entry_unit = tk.StringVar()
    entry_unit.set(units[0])
    entry_unit_vars.append(entry_unit)
    
    new_label = tk.Label(mw, text=label, anchor='e')
    new_label.grid(row = abs_offset, column = 0 + abs_column*3, sticky="e")
    
    new_textfield = tk.Text(mw, height=1, width=10)
    new_textfield.grid(row = abs_offset, column = 1 + abs_column*3)
    new_textfield.bind("<Tab>", focus_next_widget)
    text_entries.append(new_textfield)
    
    new_unitpicker = tk.OptionMenu(mw, entry_unit, *units)
    new_unitpicker.config(width=10)
    new_unitpicker.grid(row = abs_offset, column=2 + abs_column*3)

    new_entry = entry(new_textfield, label, entry_unit, unit_type)
    entries.append(new_entry)

    N_entries += 1

def create_label(label):
    global N_entries, head_offset

    abs_offset = head_offset + N_entries

    new_label = tk.Label(mw, text=label)
    new_label.grid(row = abs_offset, column = 0 + abs_column*3, columnspan=3)

    N_entries += 1

def export_file():
    global entries

    save_filename = filename_field.get("1.0", "end-1c")
    if not save_filename.endswith(".nozzle"):
        save_filename = save_filename + ".nozzle"

    with open(save_filename, "w") as cf:
        for entry in entries:
            cf.write(str(entry.entry_label) + " " + str(entry.get_value()) + " "  + str(entry.unit_field.get()) + "\n")

def import_file():
    global entries, entry_unit_vars, text_entries
    global material_unit, no_unit, length_units, angle_units, mass_flow_units, pressure_units, temperature_units,\
           velocity_units, conductivity_units, molecular_mass_units, viscosity_units, time_units

    import_filename = filename_field.get("1.0", "end-1c")
    if not import_filename.endswith(".nozzle"):
        import_filename = import_filename + ".nozzle"

    import_file = open(import_filename, "r")
    import_lines = import_file.readlines()
    import_file.close()

    for n_line in range(len(entries)):
        line = import_lines[n_line]
        line = line[:-1]
        line = line.split(" ")

        cval = ""
        for element in line:
            if not element == line[-1]:
                try:
                    cval = float(element)
                except:
                    pass
                
                text_entries[n_line].delete('1.0',"end")
                text_entries[n_line].insert('1.0',str(cval))
                
            else:
                entry_unit_vars[n_line].set(element)

def start_analysis():
    global material_unit, no_unit, length_units, angle_units, mass_flow_units,\
           pressure_units, temperature_units, velocity_units, conductivity_units,\
           molecular_mass_units, viscosity_units, time_units
    
    params = {}
    for entry in entries:
        cvalue = entry.get_value()
        cunit = str(entry.unit_field.get())

        if type(cvalue) == float:
            if cunit in length_units:
                converted_value = convert_unit(cvalue, cunit, "mm")
            elif cunit in angle_units:
                converted_value = convert_unit(cvalue, cunit, "deg")
            else:
                converted_value = cvalue
        else:
            converted_value = cvalue

        params[entry.entry_label] = converted_value
        
    nozzle_design.design_and_analyze(params)

print("Please don't close this window while working with ENMA.")

mw = tk.Tk()
mw.title("ENMA")
mw.iconbitmap('icon.ico')
mw.geometry('1170x400')

material_unit = ["[Material]"]
no_unit = ["# (unitless)"]
length_units = ["mm", "cm", "m", "km"]
angle_units = ["deg", "rad"]
mass_flow_units = ["kg/s"]
pressure_units = ["MPa", "kPa", "Pa", "bar", "atm"]
temperature_units = ["K", "C"]
velocity_units = ["m/s", "km/s"]
conductivity_units = ["W/(m*K)"]
molecular_mass_units = ["g/mol", "kg/kmol"]
viscosity_units = ["millipoise", "kg/(m*s)"]
time_units = ["s", "min", "hr"]

import_button = tk.Button(mw, text="Import Design", width=15, command=import_file)
import_button.grid(row=0, column=0, sticky="w")

export_button = tk.Button(mw, text="Export Design", width=15, command=export_file)
export_button.grid(row=1, column=0, sticky="w")

filename_field_label = tk.Label(mw, text="Filename/path:")
filename_field_label.grid(row=0, column=1, columnspan=2, sticky="w")
filename_field = tk.Text(mw, height=1, width=25)
filename_field.grid(row=1, column=1, columnspan=2)

analyze_button = tk.Button(mw, text="DESIGN & ANALYZE", width=25, height=1, font=("Arial",17), command=start_analysis, bg="red", fg="white")
analyze_button.grid(row=0, column=6, columnspan=3, rowspan=3)

about_button = tk.Button(mw, text="About", command=show_about)
about_button.grid(row=0, column=3, columnspan=3, rowspan=2)

hsep1 = ttk.Separator(mw, orient='horizontal')
hsep1.place(relx=0, rely=0.16, relwidth=1, relheight=0.2)

inputs_label = tk.Label(mw, text="DESIGN PARAMETERS", font=("Arial", 13))
inputs_label.grid(row=3, column=0, columnspan=9)

create_label("Nozzle Geometry")
create_entry("Throat Diameter", length_units, "float")
create_entry("Exit Diameter", length_units, "float")
create_entry("% Length to Equivalent Cone (optional)", length_units, "float")
create_entry("Parabola Start Angle (optional)", angle_units, "float")
create_entry("Exit Angle (optional)", angle_units, "float")
abs_column += 1
N_entries = 0

create_label("Process Setup")
create_entry("Throat Plot Fineness (optional)", no_unit, "int")
create_entry("Parabola Fineness (optional)", no_unit, "int")
abs_column += 1
N_entries = 0

create_label("Combustion Thermodynamics")
create_entry("Combustion Gases Gamma (optional)", no_unit, "float")

mw.mainloop()
