import os
import win32com.client


def run(task):

    input_file = task["input"]
    recipient = task["recipient"]
    subject = task["subject"]
    body = task["body"]

    if not os.path.isfile(input_file):
        raise FileNotFoundError(
            f"Excel file does not exist: {input_file}"
        )

    outlook = win32com.client.Dispatch("Outlook.Application")

    mail = outlook.CreateItem(0)

    mail.To = recipient
    mail.Subject = subject
    mail.Body = body

    mail.Attachments.Add(input_file)

    # Display only.
    # This does NOT send the email.
    mail.Display()

    print("\nOutlook email prepared.")
    print(f"Recipient : {recipient}")
    print(f"Subject   : {subject}")
    print(f"Attachment: {input_file}")
    print("Status    : DISPLAYED - NOT SENT")

    return {
        "success": True,
        "task_id": "015",
        "recipient": recipient,
        "subject": subject,
        "attachment": input_file,
        "sent": False
    }