# Liminal Frequencies

A sophisticated web application that bridges the gap between music and literature, creating personalized recommendations based on your preferences in either medium.

## Features

- Music-to-Books recommendations using Spotify's audio features
- Books-to-Music recommendations based on mood and themes
- Clean, minimalist interface inspired by Japanese listening bars
- Integration with Spotify and Google Books APIs

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a `.env` file with:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   FLASK_SECRET_KEY=your_secret_key
   ```
5. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
liminal_frequencies/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   ├── models/
│   ├── routes/
│   └── utils/
├── config.py
├── requirements.txt
└── app.py
```

## Technologies Used

- Python/Flask
- Spotify API
- Google Books API
- SQLAlchemy
- HTML5/CSS3/JavaScript