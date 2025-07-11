#-------------------------------------------------------------------------------------------
# Quantum Chemistry and Computing for the Curious: Illustrated with Python and Qiskit® code
# Python script to implement the temporary fix described in cell "Summary of updates V4"

## MIT License

# Copyright (c) 2025 Alain Chancé

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Implement temporary fix to support version 2 of Qiskit Runtime Primitives
# Check at the end of the Jupyter notebook Copy_V4.ipynb for details
#--------------------------------------------------------------------------------
import os
import shutil
import site

#---------------------------------------------------
# Set qv1 to true if Qiskit version is less than 2
#---------------------------------------------------
import qiskit
qv = qiskit.__version__
print(f"Qiskit version: {qv}")
qv1 = int(qv[0]) < 2

#------------------------
# Get site_packages path
#------------------------
import site
sitepackages = site.getsitepackages()

#---------------------------------------------------
# Write primitive_version.py into qiskit_algorithms
#---------------------------------------------------
with open(sitepackages[0] + '/qiskit_algorithms/primitive_version.py', "w") as file:
    # Write a single line to the file
    if qv1:
        file.write("primitive_v2 = False")
    else:
        file.write("primitive_v2 = True")

#--------------------------
# Define function mycopy()
#--------------------------
def mycopy(source_dir='', dest_dir='', show=True):

    if show:
        print("Source directory: ", source_dir)
        print("Destination directory: ", dest_dir)
        print("Copying files from source directory to destination directory\n")

    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)

    return
#----------------------------------------------------------------------------------

#-----------------
# Prompt the user
#-----------------
while True:
    response = input("\nDo you want to to implement the temporary fix described in cell 'Summary of updates V4' ? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        print("You chose Yes.")

        d = '/qiskit_algorithms'
        source_dir = os.path.expanduser('~' + d)
        dest_dir = os.path.expanduser(sitepackages[0] + d)
        mycopy(source_dir, dest_dir)

        d = '/qiskit/primitives'
        source_dir = os.path.expanduser('~' + d)
        dest_dir = os.path.expanduser(sitepackages[0] + d)
        mycopy(source_dir, dest_dir)

        source_dir = os.path.expanduser('~' + d + '_V1')
        mycopy(source_dir, dest_dir)

        d = '/qiskit/providers'
        source_dir = os.path.expanduser('~' + d)
        dest_dir = os.path.expanduser(sitepackages[0] + d)
        mycopy(source_dir, dest_dir)

        d = '/qiskit_nature'
        source_dir = os.path.expanduser('~' + d)
        dest_dir = os.path.expanduser(sitepackages[0] + d)
        mycopy(source_dir, dest_dir)

        break

    elif response in ['n', 'no']:
        break