# Hatch Lab WB analysis template maker

## Installation

### Requirements
- git
- python3

### Installation
1. Make or find a directory where you would like to install the tool.
2. In Terminal (located in /Applications/Utilities), copy and paste the following:

`git clone https://github.com/hatch-lab/WB-templater.git`

3. Generate a virtual Python environment:

``python3 -m venv .env
source .env/bin/activate``

4. Install dependencies:
`pip install -U pip
pip install -r requirements.txt
deactivate`

5. The tool should now be installed.

## Quickstart
Before using, you will need to reactivate the Python virtual environment. Once done, you should deactivate it:

``source .env/bin/activate
python make-template.py ../Path/To/File.xlsx --conditions=4 --ab=V5 --ab=HSP90 --loading-ctrl=GAPDH
deactivate``

## Options
`--conditions`
The number of conditions to analyze. This is probably the number of lanes you want to look at.

`--ab`
The name of an antibody you’re using.

`--loading-ctrl`
The name of the loading control.

## Examples
* I have 10 lanes, all stained for V5 using GAPDH as a loading control. I would enter the following:

``source .env/bin/activate
python make-template.py ../Path/To/File.xlsx --conditions=10 --ab=V5 --loading-ctrl=GAPDH
deactivate``

* I have 5 conditions that I’ve loaded twice into 10 lanes. Half will be stained for V5, the other half for EGFP, all using GAPDH as loading control.

``source .env/bin/activate
python make-template.py ../Path/To/File.xlsx --conditions=5 --ab=V5 --ab=EGFP --loading-ctrl=GAPDH
deactivate``

* I have 5 conditions that I’ve loaded twice into 10 lanes. Half will be stained for V5 with GAPDH as a loading control, the other half for EGFP with HSP90 as a loading control:

``source .env/bin/activate
python make-template.py ../Path/To/File.xlsx --conditions=5 --ab=V5 --loading-ctrl=GAPDH --ab=EGFP --loading-ctrl=HSP90
deactivate``