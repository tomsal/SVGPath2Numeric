# SVGPath2Numeric
This is a tiny script I used to convert paths from SVG graphics to numerical values. Matplotlib will plot the data so you can check it.

## Requirements
Python3, Numpy, Matplotlib

## Extract SVGs from PDF
Example pdf: https://arxiv.org/pdf/1511.04056.pdf

Import relevant page from PDF with Inkscape. Find the xml paths of the line (not the points). The easiest way is to click on it and enter all groups on the way. At the same time look at XML editor (Ctrl+Shift+X in inkscape).

E.g. (`SensIT_train.svg`)
```
<path
   id="path5451"
   style="fill:none;stroke:#ff00ff;stroke-width:3;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:10;stroke-opacity:1;stroke-dasharray:none"
   d="m 67.784615,79.75221 34.338465,0.864 34.33846,18.90432 34.33846,43.99488 34.33846,33.5232 34.33846,4.28544 34.33846,22.01472"
   inkscape:connector-curvature="0" />
```
The string after `d=` is what we want. Copy those strings into JSON file.

## Provide Reference values
Now, we need to provide the scale of X- and Y-Axis. Simply lookup two ticks in inkscape (enter all groups and look at XML editor).

For example in `SensIT_train.json`: the y-tick at `0.6` is at `81.79125` in SVG coordinates. Respectively, `y = 0.7` at `116.35125`, `x = 6` at `67.784615` and `x = 8` at `102.12308`.

## Save stuff as json
```
{
  "X1"   : "6,67.784615",
  "X2"   : "8,102.12308",
  "Y1"   : "0.6,81.79125",
  "Y2"   : "0.7,116.35125",
  "data" : {
    "OC1" : "m 67.784615,79.75221 34.338465,0.864 34.33846,18.90432 34.33846,43.99488 34.33846,33.5232 34.33846,4.28544 34.33846,22.01472",
    "Random" : "m 67.784615,123.81621 34.338465,8.08704 34.33846,14.13504 34.33846,11.43936 34.33846,15.65568 34.33846,12.99456 34.33846,9.26208",
    "Axis-aligned" : "m 67.784615,130.90101 34.338465,17.03808 34.33846,7.36128 34.33846,5.59872 34.33846,19.59552 34.33846,15.93216 34.33846,6.60096",
    "CO2" : "m 67.784615,155.26581 34.338465,6.35904 34.33846,7.01568 34.33846,0.24192 34.33846,3.17952 34.33846,6.7392 34.33846,8.08704",
    "Non-greedy" : "m 67.784615,163.11093 34.338465,3.59424 34.33846,0.93312 34.33846,-1.52064 34.33846,-4.56192 34.33846,0.79488 34.33846,8.36352"
   }
}
```
Note that the keys in the data directory will be used as labels for the test plot.

## Run script
```
python SVGPath2Numeric.py -o SensIT_train_num.json SensIT_train.json
```
The script will output the converted values and show you a plot so you can compare the result.
Optionally, you can specify an output JSON file, so you can use the converted data in another script (see `SensIT_train_num.json`).

## Bash batch

Run script on all files in directory `json` and save to directory `num`.
`-q` disables plot and console output.
```
for file in `ls json`; do python SVGPath2Numeric.py -o num/$file -q json/$file; done
```
