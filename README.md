# Emotorad Backend Task: Identity Reconciliation

## Overview

The **Identity Reconciliation** service is designed to manage and consolidate user contact information for **Zamazon.com**. The service allows linking multiple contact details (such as emails and phone numbers) to a single individual, organizing them into primary and secondary contacts. This API processes JSON payloads containing contact information, creates or updates the user's contact records, and returns consolidated contact details.

## Features

- **Identify Endpoint**: Handles a POST request to consolidate contact information for an individual.
- **Contact Linking**: Links multiple phone numbers and emails to a single individual, ensuring proper distinction between primary and secondary contacts.
- **Database**: Uses SQLite to persist contact data in a lightweight, structured manner.
- **JSON Response**: Returns consolidated contact details in a structured JSON format.

## Requirements

Before running this project, ensure you have the following installed on your machine:

- **Python 3.6+**: Python version 3.6 or higher.
- **Flask**: Python web framework for building the REST API.
- **SQLite3**: A lightweight database used to store contact details.

## Setup and Execution

Follow the steps below to set up and run the project locally:

### 1. Clone the Repository

Clone the project repository to your local machine using Git:

git clone https://github.com/VivekanandaReddy2233/emotorad-identity-reconciliation.git
cd emotorad-identity-reconciliation

### 2. Install Dependencies

Install the required Python dependencies:

pip install -r requirements.txt

### 3. Initialize the Database

Initialize the SQLite database with the necessary contacts table:

python app.py

This command will create the SQLite database and set up the required table for storing contact information.

### 4. Run the Application

Start the Flask development server:

python app.py

The server will run at http://127.0.0.1:5000/ by default.

### 5. Test the Service with Postman

To test the /identify endpoint, use Postman with the following steps:

### Step 1: Open Postman

Download and install Postman if you haven’t already.

### Step 2: Create a New Request

Open Postman.

Click on New and select Request.

Name the request (e.g., "Test Identify API") and select a collection (or create a new one).

Click Save.

### Step 3: Configure the Request

Set the HTTP method to POST.

Enter http://127.0.0.1:5000/identify in the URL field.

### Step 4: Add JSON Payload

.Select the Body tab.

.Choose the raw option.

.In the dropdown next to raw, select JSON (application/json).

## **Enter the following JSON payload**:

```plaintext
{
  "email": "admin@example.com",
  "phoneNumber": "1234567890"
}
```
---

### Step 5: Send the Request

.Click the Send button in Postman. You should receive a response with consolidated contact details in JSON format.

## **Example Response**:
```plaintext
{
    "primaryContactId": 1,
    "emails": ["admin@example.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": []
}
```
### Database Schema

## **The contacts table schema is as follows**:
```plaintext
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phoneNumber TEXT,
    email TEXT,
    linkedId INTEGER,
    linkPrecedence TEXT NOT NULL DEFAULT 'primary',
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL
)
```

### Fields:

.id: Unique identifier for the contact.
.phoneNumber: The contact's phone number (optional).
.email: The contact's email address (optional).
.linkedId: The ID of the primary contact to which this contact is linked.
.linkPrecedence: Indicates whether the contact is primary or secondary.
.createdAt: Timestamp of when the contact was created.
.updatedAt: Timestamp of when the contact was last updated.

### Error Handling

The application includes basic error handling. Here are some common error scenarios:

Example: Missing Both email and phoneNumber

## **If both fields are missing, the response will look like this**:
```plaintext
{
    "error": "Both email and phoneNumber are required."
}
```

### Conclusion

This project demonstrates a web service that efficiently manages customer contact information. It integrates advanced techniques for linking multiple data points (such as emails and phone numbers) to a single individual while ensuring proper organization and consolidation of contact details.
# Identity_Reconciliation
# Identity_Reconciliation
# Emotorad_Identity_Reconciliation
# Emotorad_Identity_Reconciliation
