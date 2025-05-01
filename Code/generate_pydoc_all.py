import os
import glob
import subprocess

# Folder containing your .py files
source_folder = "."

# Find all Python files
py_files = glob.glob(os.path.join(source_folder, "*.py"))

# Run pydoc -w on each
for py_file in py_files:
    module_name = os.path.splitext(os.path.basename(py_file))[0]
    print(f"Generating docs for: {module_name}")
    subprocess.run(["python", "-m", "pydoc", "-w", module_name])
