# NASA SUITS Development Dashboard

A development dashboard for the Columbia University Lunar Lions NASA SUITS project. This web application provides various tools and visualizations to assist in the development of EVA interface systems.

## Features

- **Vital Signs Monitor**: Real-time visualization of astronaut vital signs and suit telemetry
- **Navigation System**: 2D map interface with position tracking and waypoint management
- **Procedure Tracker**: Interactive checklist system for EVA procedures
- **Geology Tools**: XRF data visualization and sample management
- **Alert System**: Real-time monitoring and warning system
- **Mission Timeline**: Time tracking and schedule management

## Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open a web browser and navigate to `http://localhost:5000`

## Project Structure

```
LunarLionsWeb/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS, images)
└── templates/         # HTML templates
    ├── base.html     # Base template with common layout
    ├── index.html    # Dashboard homepage
    ├── vitals.html   # Vital signs monitor
    ├── navigation.html
    ├── procedures.html
    ├── geology.html
    ├── alerts.html
    └── timeline.html
```

## Development

Each page is designed to be modular and extensible. The vitals page is currently implemented as an example. To implement other pages:

1. Create a new template in the `templates` directory
2. Add any necessary static files
3. Implement the corresponding route in `app.py`
4. Add any required API endpoints

## Features to Implement

- [ ] Navigation map using Leaflet.js
- [ ] Interactive procedure checklists
- [ ] XRF data visualization
- [ ] Alert notification system
- [ ] Mission timeline tracker
- [ ] Interoperability with other systems

## Contributing

1. Create a new branch for your feature
2. Implement your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the NASA SUITS challenge and is subject to NASA's terms and conditions.