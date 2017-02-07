# uefi_py
python tool to prase UEFI bios

usage: main.py [-h] {prase,var} ...

optional arguments:
  -h, --help   show this help message and exit

commands:
  {prase,var}
    prase      prase uefi bios fv
    var        prase uefi bios variable

usage: main.py prase [-h] -f BIN -n FVNAME

optional arguments:
  -h, --help  show this help message and exit
  -f BIN      BIOS binary file path
  -n FVNAME   fv name {NV/DXE/PEI} //to do later

usage: main.py var [-h] -f BIN -vs VPDSIZE -ws VPDWORKINGSIZE
                   [-vn VARIABLENAME]

optional arguments:
  -h, --help          show this help message and exit
  -f BIN              BIOS binary file path
  -vs VPDSIZE         vpd size of the variable
  -ws VPDWORKINGSIZE  ftw working size of the variable
  -vn VARIABLENAME    variable name

