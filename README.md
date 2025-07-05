# Calendar App

A modern, responsive calendar application built with FastAPI and vanilla JavaScript. Features a clean UI with dynamic font scaling for event titles and a RESTful API backend.

## Features

- 📅 Monthly calendar view with navigation
- ➕ Add, edit, and delete events
- 🔤 Dynamic font scaling for event titles based on length
- 💾 Persistent storage using file-based system
- 🌐 RESTful API backend
- 📱 Responsive design for mobile and desktop
- 🎨 Clean, modern UI with hover effects

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Storage**: JSON file-based (easily replaceable with database)
- **Server**: Uvicorn ASGI server

## Installation

### Prerequisites

- Python 3.8+ (tested with Python 3.12)
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd calendar
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
calendar/
├── main.py                 # FastAPI application and API endpoints
├── requirements.txt        # Python dependencies
├── events.json            # Event storage (created automatically)
├── static/
│   ├── css/
│   │   └── styles.css     # Application styles
│   └── js/
│       └── script.js      # Frontend JavaScript
├── templates/
│   └── index.html         # Main HTML template
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## API Documentation

The FastAPI application provides the following endpoints:

### Get All Events
```
GET /api/events
```
Returns all events organized by date.

### Get Events by Date
```
GET /api/events/{date}
```
Returns events for a specific date (format: YYYY-MM-DD).

### Create Event
```
POST /api/events/{date}
Content-Type: application/json

{
    "title": "Event title",
    "date": "ISO date string"
}
```

### Update Event
```
PUT /api/events/{date}/{event_id}
Content-Type: application/json

{
    "title": "Updated event title"
}
```

### Delete Event
```
DELETE /api/events/{date}/{event_id}
```

## Features in Detail

### Dynamic Font Scaling

The application automatically adjusts event title font sizes based on the number of words:
- 1-3 words: 16px (larger, more prominent)
- 4-6 words: 14px (moderate size)
- 7+ words: 12px or smaller

This ensures optimal readability while maximizing the use of available space in calendar cells.

### Responsive Design

The calendar adapts to different screen sizes:
- Desktop: Full-featured calendar with hover effects
- Mobile: Touch-friendly interface with adjusted cell sizes

### Event Management

- Click on any calendar day to add a new event
- Click on an existing event to edit or delete it
- Events are immediately saved and persist between sessions

## Development

### Running in Development Mode

For development with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Event categories with color coding
- [ ] Recurring events
- [ ] Event reminders and notifications
- [ ] Calendar sharing functionality
- [ ] Import/Export (iCal format)
- [ ] Week and day views
- [ ] Drag-and-drop event management
- [ ] Search functionality

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.