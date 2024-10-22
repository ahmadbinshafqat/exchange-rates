# Exchange Rates API

A FastAPI application that fetches exchange rates from the European Central Bank (ECB) and stores them in a DynamoDB database. The application includes a scheduled background job that runs daily at 10:00 PM to update the exchange rates. It also provides an API endpoint to retrieve the latest exchange rates with a comparison to the previous day's rates.

## Features

- Fetches exchange rates from the ECB in XML format.
- Stores exchange rates in a DynamoDB table.
- Scheduled background job to update exchange rates every day at 10:00 PM.
- API endpoint to retrieve current exchange rates and compare them with the previous day's rates.

## Technologies Used

- FastAPI
- Boto3 (AWS SDK for Python)
- APScheduler (for scheduling tasks)
- LocalStack (for local AWS service emulation)
- Docker

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd exchange_rates_api
   ```

2. Build and run the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This command will start the FastAPI application along with LocalStack to simulate DynamoDB.

### Configuration

The application is configured to connect to a LocalStack instance of DynamoDB. You can modify the `db.py` file to change the endpoint if you're using a different environment.

### API Endpoints

- **GET /exchange-rates**

  Retrieve the current exchange rates and compare them with the previous day's rates.

  **Response:**

  ```json
  {
      "exchange_rates": [
          {
              "currency": "USD",
              "current_rate": 1.15,
              "previous_rate": 1.10,
              "change": 0.05
          },
          ...
      ]
  }
  ```

### Running the Background Job

The background job is set to run at 10:00 PM (UTC) daily. It fetches the latest exchange rates from the ECB and stores them in the DynamoDB database. You can check the logs to see if the job is running as expected.

### Testing

You can test the API by making a GET request to the `/exchange-rates` endpoint using tools like `curl` or Postman:

```bash
curl http://localhost:8000/exchange-rates
```

### Cleanup

To stop the application, you can use:

```bash
docker-compose down
```