# AI News Dashboard Scrapper

A powerful, automated scraper and dashboard for tracking the latest news in Artificial Intelligence from various sources including Reddit, Ben's Bites, and The Rundown.

## 🚀 Features

- **Multi-source Scraper**: Extracts top AI posts and articles from:
  - Reddit (r/artificial, r/MachineLearning, r/Singularity)
  - Ben's Bites
  - The Rundown
- **Modern Dashboard**: A sleek, responsive web interface to browse and filter news.
- **Smart Storage**: Atomic JSON-based storage with backup systems.
- **Save for Later**: Ability to "star" or save articles for future reference.
- **Custom Server**: Lightweight Python-based backend to serve the dashboard and API.

## 🛠 Project Structure

- `dashboard.html/css/js`: The frontend interface.
- `serve_dashboard.py`: Python server to run the application.
- `tools/`:
  - `manager.py`: Orchestrates the scraping process.
  - `scrape_*.py`: Individual scraper modules.
  - `storage_manager.py`: Handles data persistence.
- `architecture/`: Documentation on system design.
- `Brand_Guidlines/`: Assets and styles for the PRISM brand redesign.

## 🚦 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AngadSinghLamba/Scrapper.git
   cd Scrapper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Scrape latest news**:
   ```bash
   python tools/manager.py
   ```

2. **Start the dashboard**:
   ```bash
   python serve_dashboard.py
   ```
   The dashboard will be available at `http://localhost:8000`.

## 🎨 Brand Redesign

This project follows the **PRISM** brand guidelines, featuring a dark aesthetic with vibrant accents and glassmorphism elements.

## 📄 License

This project is open-source and available under the MIT License.
