# Financial Sentiment Analysis Prototype

This project is a simple end-to-end solution that retrieves financial news data, processes it, uses a pre-trained sentiment analysis model to determine the sentiment of the news, and exposes the result via a REST API.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Dependencies](#dependencies)
- [Docker](#docker)
- [Design Choices](#design-choices)
- [License](#license)

## Project Structure

The project is structured as follows:

```
financial-sentiment-analysis/
├── app.py                  # FastAPI application
├── api_client.py           # Financial news API client
├── preprocessor.py         # Text preprocessing module
├── sentiment_analyzer.py   # FinBERT sentiment analysis
├── aggregator.py           # Sentiment aggregation logic
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md               # Project documentation
```

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vedant0321/Fin_Senitment_Analysis
   cd financial-sentiment-analysis
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory based on the `.env.example` file.
   - Add your Finnhub API key to the `.env` file:
     ```
     API_KEY=your_finnhub_api_key
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application locally (form the project directory), use the following command:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

- **Sentiment Analysis**:
  - Endpoint: `/sentiment`
  - Method: `POST`
  - Parameters:
    - `ticker` (str): The stock symbol of the company (e.g., "AAPL" for Apple Inc.).
    - `days` (int): The number of days to consider for sentiment analysis.

## Testing the API

1. Open your browser and navigate to `http://127.0.0.1:8000/docs`.
2. You will see the FastAPI Swagger UI.
3. Select the `/sentiment` endpoint and click "Try it out".
4. Enter the `ticker` name and the number of `days` for analysis.
5. Click "Execute" to see the sentiment analysis results.

**Sample Output**
```json
{
  "ticker": "AAPL",
  "period": {
    "from": "2023-03-20",
    "to": "2023-03-25"
  },
  "sentiment": {
    "overall_sentiment": "positive",
    "confidence": 0.75,
    "distribution": {
      "positive": 0.75,
      "neutral": 0.2,
      "negative": 0.05
    },
    "average_scores": {
      "positive": 0.68,
      "neutral": 0.25,
      "negative": 0.07
    },
    "item_count": 20
  },
  "news_items": [
    {
      "datetime": 1679673600,
      "headline": "Apple's new product announcement exceeds expectations",
      "sentiment": "positive",
      "score": 0.92
    },
    // More news items...
  ]
}

```

## Dependencies

All necessary Python dependencies are listed in the `requirements.txt` file.

## Docker

A `Dockerfile` is provided to containerize the application. To build and run the Docker container, follow these steps:

1. **Build the Docker Image:**
```bash
docker build -t financial-sentiment-analysis-v2 .

```

2. **Run the Docker Container:**
```bash
docker run -d -p 8000:8000 financial-sentiment-analysis-v2

```

## Design Choices

- **API Client**: Uses Finnhub API to retrieve financial news data.
- **Preprocessing**: Cleans and preprocesses textual data.
- **Sentiment Analysis**: Utilizes the FinBERT model from Hugging Face.
- **Aggregation**: Averages sentiment scores to produce an overall sentiment.
- **API**: Built using FastAPI for a lightweight and efficient REST API.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](#license) file for details.

## System Configuration

- The user has a valid Finnhub API key, which can be generated from [here](https://finnhub.io).
- The system has at least 8GB of RAM for optimal performance.

