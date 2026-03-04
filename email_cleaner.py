import imaplib
import email

EMAIL = input("Enter your Gmail address: ")
APP_PASSWORD = input("Enter your app password: ")

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, APP_PASSWORD)
mail.select("inbox")

print("Connected to Gmail successfully!")

print("\nSearch by:")
print("1. Sender email address")
print("2. Subject Keyword")

choice = input("\nEnter 1 or 2: ")

if choice == "1":
    search_value = input("Enter sender email to search: ")
    _, messages = mail.search(None, f'FROM "{search_value}"')
elif choice == "2":
    search_value = input("Enter subject keyword to search: ")
    _, messages = mail.search(None, f'SUBJECT "{search_value}"')
else:
    print("Invalid choice")
    exit()

email_ids = [e.decode() for e in messages[0].split()]
print(f"\nFound {len(email_ids)} emails matching your search!")

print("\nPreviewing first 5 emails:\n")

for email_id in email_ids[:5]:
    _, msg_data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    print(f"From: {msg['FROM']}")
    print(f"Subject: {msg['Subject']}")
    print(f"Date: {msg['Date']}")
    print("-" * 40)

confirm = input(f"\nDelete all {len(email_ids)} emails? (yes/no): ")

if confirm == 'yes':
    email_ids_str = ",".join(email_ids)
    mail.store(str(email_id), "+FLAGS", "\\Deleted")
    mail.expunge()
    print(f"Successfully deleted {len(email_ids)} emails!")
else:
    print("Cancelled. No emails were deleted.")
mail.close()
mail.logout()
