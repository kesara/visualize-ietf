# visualize-ietf
Visualization of IETF (Internet Engineering Task Force) IDs (Internet Draft) and RFC (Request for Comments)

[![IETF Internet Draft (ID) Authoring Visualization - January 2021- July 2021 on Youtube](screenshot.png)](https://www.youtube.com/watch?v=55KZ-cNHOoo)

## Installation

* Clone project

```
git clone https://github.com/kesara/visualize-ietf.git
```

* Create and activate Python venv. (Tested with Pythn 3.9)

```
cd visualize-ietf
python -m venv venv
. venv/bin/activate
```

* Install Python dependencies

```
pip install -r requirements.txt
```

* Install [gource](https://gource.io/).

* Get Bibxml3 references.

```
rsync -avz rsync.ietf.org::xml2rfc.bibxml/bibxml3/*.xml bibxml3
```

## Usage

* Created a sorted ID log

```
python id_log.py > id.log && sort -n id.log > id.log.sorted
```

* Create the visualization

```
gource --log-format custom --date-format '%Y-%m-%d' -a 0.5 --hide filenames,root -s 3 --bloom-intensity 0.01 --dir-name-depth 2 id.log.sorted
```

## Legend
![legend](colour_codes.png "Legend")
