import csv
import re
from typing import List, Tuple
def normalize_phone(phone: str) -> str:
    formatted_phone = re.sub(
        r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*',
        r'+7(\2)\3-\4-\5\6\7', phone)

    match = re.search(r'(\+7\(\d{3}\)\d{3}-\d{2}-\d{2})\s?доб\.\s?(\d+)', formatted_phone)
    if match:
        formatted_phone = match.group(1)
        extension = f' доб.{match.group(2)}'
        return f'{formatted_phone}{extension}'
    else:
        return formatted_phone


def merge_duplicates(contacts: List[List[str]]) -> List[List[str]]:
    grouped_contacts = {}
    for contact in contacts:
        key = (contact[0], contact[1])
        if key not in grouped_contacts:
            grouped_contacts[key] = [contact]
        else:
            grouped_contacts[key].append(contact)

    merged_contacts = []
    for group in grouped_contacts.values():
        merged_contact = group[0]
        for other_contact in group[1:]:
            merged_contact = [x or y for x, y in zip(merged_contact, other_contact)]
        merged_contacts.append(merged_contact)

    return merged_contacts



with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f)
    contacts_list = list(rows)

for contact in contacts_list[1:]:
    contact[5] = normalize_phone(contact[5])

normalized_contacts = merge_duplicates(contacts_list[1:])


for contact in normalized_contacts:
    if len(contact[0].split()) == 3:
        contact[0], contact[1], contact[2] = contact[0].split()
    elif len(contact[0].split()) == 2:
        contact[0], contact[1] = contact[0].split()
    elif len(contact[1].split()) == 2:
        contact[1], contact[2] = contact[1].split()


normalized_contacts.sort(key=lambda x: x[0])


header = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
normalized_contacts.insert(0, header)


normalized_contacts = merge_duplicates(normalized_contacts)



with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f)
    datawriter.writerows(normalized_contacts)