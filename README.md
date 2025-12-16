# Event Resource Allocation System

A Flask-based web application for managing events and allocating resources to them, with conflict detection and utilization reporting.

## Features

- **Event Management**: Create, view, and delete events with start and end times.
- **Resource Management**: Add and remove resources with types.
- **Resource Allocation**: Allocate resources to events with automatic conflict detection.
- **Reports**: View resource utilization reports showing used hours, free hours, and percentage utilization over a week.

## Installation

1. Clone or download the project files.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`.

## Database

The application uses SQLite (`db.sqlite3`) for data storage. The database is automatically created when the app runs for the first time.

## Usage

- **Home**: Landing page.
- **Events**: Manage events (add, delete).
- **Resources**: Manage resources (add, delete).
- **Allocate**: Assign resources to events (checks for conflicts).
- **Report**: View weekly resource utilization.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS (via Jinja2 templates)

## Contributing

Feel free to submit issues or pull requests for improvements.