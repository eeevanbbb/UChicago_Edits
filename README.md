# UChicago_Edits
@UChicago_Edits is a TwitterBot that tweets whenever someone from the UChicago campus anonymously edits a Wikipedia page.

## Installation
`pip install -r requirements.txt`

## Usage
`python Main.py`

## About
UChicago_Edits listens to a stream of changes to Wikipedia articles via [WikiMon](https://github.com/hatnote/wikimon). If the edit is anonymous, and if the editor's IP address matches one of the subnets in `Subnets.txt`, [@UChicago_Edits](https://twitter.com/UChicago_edits) will send out a tweet with the title of the edited page, the location of the editor (as specified in `Subnets.txt`), and a link to the revision.

## Scripts
The `/scripts` folder contains some helpful scripts I used when compiling `Subnets.txt`. The process was ultimately a manual one, however, which involved translating DNS records for UChicago subnets into human-readable names of locations. The file is so far incomplete, and entries prefaced with `#` are inactive. If an IP address is not matched by any of the named subnets, it will fall through to the larger `/16` block and simply be labeled as `campus`.

If you notice any errors in this file, or have any additions/corrections, please let me know! Or submit a pull request. This is a work in progress and I appreciate all the help I can get.

## Twitter Account
The account [@UChicago_Edits](https://twitter.com/UChicago_edits) has been tweeting for several years by running on an instance of Ed Summer's [anon](https://github.com/edsu/anon) coffee script. As of 1/27/17, however, [@UChicago_Edits](https://twitter.com/UChicago_edits) has been running on the code in this repository. Please feel free to contribute!