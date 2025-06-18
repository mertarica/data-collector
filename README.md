# Data Collector

A full-stack application for collecting, processing, and visualizing data from the INE (Instituto Nacional de Estadística) API.

## Project Structure

```
├── backend/          # FastAPI backend server
├── frontend/         # Vue.js + TypeScript frontend
└── shared/           # Shared data and resources
```

## Features

- **Data Collection**: Fetch datasets from INE API
- **Data Processing**: Transform raw data with metadata enrichment
- **Data Visualization**: Interactive charts and data exploration
- **Export Functionality**: Download data in JSON format
- **Real-time Updates**: Live data fetching and processing

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Python 3.13** - Core programming language
- **Pydantic** - Data validation and settings management

### Frontend

- **Vue.js 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the development server:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Endpoints

- `GET /api/v1/datasets` - List available datasets
- `GET /api/v1/datasets/{code}/raw` - Get raw dataset data
- `GET /api/v1/datasets/{code}/processed` - Get processed dataset data

## Development

### Backend Development

- The backend uses FastAPI with automatic API documentation at `/docs`

### Frontend Development

- Vue 3 with Composition API
- TypeScript for type safety
- Pinia for state management
- Tailwind CSS for styling

## License

This project is licensed under the MIT License.
