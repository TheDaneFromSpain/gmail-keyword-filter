# This script filters work_emails.txt by ignoring rows (emails) that contain the same characters as any row in company_names.txt.
#
# Thus, only emails that do not share keywords with any line in company_names.txt are displayed (ignoring lower/uppercase).
#
# It loops infinitely with a 10s delay until no emails are left.
# It is intended to manually write and save company_names.txt while it runs in order to update it.
import quickstart
import time

# Log into google account and use gmail API to create a text file containing all relevant emails.
quickstart.main()

# Read the text file containing emails.
with open("work_emails.txt", 'r') as work:
    email_text_file = list(filter(None, work.read().split('\n')))

# Loop that continuously reads a text file containing the words to filter the emails by, ignoring lower/uppercase, until no emails are left.
while True:
    with open("company_names.txt", 'r') as companies:
        company_names = list(filter(None, companies.read().lower().split('\n')))

    counter: int = 0
    for email_row in email_text_file:
        if all(name not in email_row.lower() for name in company_names):
            counter += 1
            print(email_row)

    print(f'{counter} emails remaining\n')

    if counter == 0:
        break

    time.sleep(10)