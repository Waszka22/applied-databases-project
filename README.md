## Project Description

This repository contains the submission for the **Applied Databases** module, part of the **Higher Diploma in Science in Computing in Data Analytics at ATU**.

This is a console Conference Management System built in Python, designed to handle core event data such as speakers, sessions, attendees, companies, and rooms.

The project combines two types of databases to showcase different data modeling approaches:

- **MySQL** handles structured data and standard operations  
- **Neo4j** manages relationships between attendees through a graph-based approach  

---
## Application Features

| Feature                     | Description                                      |
|----------------------------|--------------------------------------------------|
| View Speakers & Sessions   | Browse speakers and their sessions               |
| View Attendees by Company  | See attendees grouped by company                 |
| Add New Attendee           | Add a new attendee to the system                 |
| View Connected Attendees   | View attendee connections                        |
| Add Attendee Connections   | Create connections between attendees             |
| View Rooms                 | Check available rooms                            |
| Exit Application           | Close the application                            |

---

## Technologies Used

- Python 3
- MySQL 
- Neo4j
- PyMySQL

 ---

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the repository

`git clone https://github.com/Waszka22/applied-databases-project`

`cd applied-databases-project`

### 2. Install dependencies

`pip install mysql-connector-python`
`pip install neo4j`

### 3. Set up databases

* MySQL
* Neo4j

### 4. Run the application

`python main.py`





