# Gmail keyword filter

This project was developed for personal use in filtering company names from emails in order to dynamically create and update a list of the companies already applied to.

Because of this, it only looks for emails that have the "work" label in gmail, but this can be changed in the customizations section.

It uses a modified version of the Gmail API python quickstart, which is under Apache licence 2.0: https://developers.google.com/workspace/gmail/api/quickstart/python

## Instructions

1. Activate your gmail API and add your personal *credentials.json* to the main directory by following the instructions in https://developers.google.com/workspace/gmail/api/quickstart/python
2. Run *main.py*

## Customizations

- Change query from "label:work" in `get_mails` function in *quickstart.py* to any other gmail search query.
- Modify the frequency of updates while in the infinite loop by changing `time.sleep(10)` to any amount of seconds desired.
- Remove lower/uppercase ignore by removing `.lower()` function calls.
