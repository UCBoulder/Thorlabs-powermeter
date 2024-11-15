# Thorlabs-powermeter
python communication to thorlabs powermeter head

## Installation
Download the powermeter software from [Thorlabs website](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OPM)

The .dll files and drivers should be included in the software installation.

Go to line 292 & line 297 of TLPMX.py in the repo.

Change the path to where the TLPMX_64.dll file is located on your local computer.

install ctypes
```
pip install ctypes
```