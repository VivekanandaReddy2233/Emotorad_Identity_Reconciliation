from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Database file name
db_file = 'contacts.db'

# Helper function to execute SQL commands
def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}

# Initialize the database and create the contacts table
def init_db():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phoneNumber TEXT,
        email TEXT,
        linkedId INTEGER,
        linkPrecedence TEXT NOT NULL DEFAULT 'primary',
        createdAt TEXT NOT NULL,
        updatedAt TEXT NOT NULL,
        deletedAt TEXT
    )
    """
    execute_query(create_table_query)

# API endpoint to identify contacts
@app.route('/identify', methods=['POST'])
def identify():
    data = request.get_json()
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')

    # Validate input
    if not email and not phoneNumber:
        return jsonify({"error": "Email or phone number must be provided."}), 400

    # Find matching contacts
    query = """
    SELECT * FROM contacts 
    WHERE (email = ? AND email IS NOT NULL) OR (phoneNumber = ? AND phoneNumber IS NOT NULL)
    """
    matching_contacts = execute_query(query, (email, phoneNumber), fetch_all=True)

    if not matching_contacts:
        # Create a new primary contact if no match exists
        now = datetime.utcnow().isoformat()
        insert_query = """
        INSERT INTO contacts (email, phoneNumber, linkPrecedence, createdAt, updatedAt) 
        VALUES (?, ?, 'primary', ?, ?)
        """
        execute_query(insert_query, (email, phoneNumber, now, now))
        contact_id = execute_query("SELECT last_insert_rowid()", fetch_one=True)[0]
        return jsonify({
            "primaryContactId": contact_id,
            "emails": [email] if email else [],
            "phoneNumbers": [phoneNumber] if phoneNumber else [],
            "secondaryContactIds": []
        }), 200

    # Process matching contacts
    primary_contact = None
    secondary_contacts = []
    emails = set()
    phoneNumbers = set()

    for contact in matching_contacts:
        contact_id, contact_phone, contact_email, linked_id, link_precedence, *_ = contact
        emails.add(contact_email)
        phoneNumbers.add(contact_phone)
        if link_precedence == 'primary' and not primary_contact:
            primary_contact = contact
        else:
            secondary_contacts.append(contact)

    # If no primary contact is found, set the first contact as primary
    if not primary_contact:
        primary_contact = matching_contacts[0]
        primary_contact_id = primary_contact[0]
        update_query = "UPDATE contacts SET linkPrecedence = 'primary' WHERE id = ?"
        execute_query(update_query, (primary_contact_id,))

    primary_contact_id = primary_contact[0]

    # Add new secondary contacts if needed
    now = datetime.utcnow().isoformat()
    if email and email not in emails:
        insert_query = """
        INSERT INTO contacts (email, phoneNumber, linkedId, linkPrecedence, createdAt, updatedAt) 
        VALUES (?, NULL, ?, 'secondary', ?, ?)
        """
        execute_query(insert_query, (email, primary_contact_id, now, now))
        secondary_contact_id = execute_query("SELECT last_insert_rowid()", fetch_one=True)[0]
        secondary_contacts.append((secondary_contact_id, email, None, primary_contact_id, 'secondary'))
        emails.add(email)

    if phoneNumber and phoneNumber not in phoneNumbers:
        insert_query = """
        INSERT INTO contacts (email, phoneNumber, linkedId, linkPrecedence, createdAt, updatedAt) 
        VALUES (NULL, ?, ?, 'secondary', ?, ?)
        """
        execute_query(insert_query, (phoneNumber, primary_contact_id, now, now))
        secondary_contact_id = execute_query("SELECT last_insert_rowid()", fetch_one=True)[0]
        secondary_contacts.append((secondary_contact_id, None, phoneNumber, primary_contact_id, 'secondary'))
        phoneNumbers.add(phoneNumber)

    # Prepare response
    secondary_contact_ids = [contact[0] for contact in secondary_contacts]
    secondary_emails = [contact[1] for contact in secondary_contacts if contact[1]]
    secondary_phone_numbers = [contact[2] for contact in secondary_contacts if contact[2]]

    return jsonify({
        "primaryContactId": primary_contact_id,
        "emails": list(emails),
        "phoneNumbers": list(phoneNumbers),
        "secondaryContactIds": secondary_contact_ids,
        "secondaryEmails": secondary_emails,
        "secondaryPhoneNumbers": secondary_phone_numbers
    }), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
