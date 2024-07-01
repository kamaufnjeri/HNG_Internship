# HNG Internship Stage One Task One

This repository contains the code for a basic Flask web server, which exposes an API endpoint to return the IP address, location, and temperature of client.

## Features

- A home route to test the Flask application.
- An API endpoint that:
  - Receives a visitor's name as a query parameter.
  - Retrieves the requester's IP address.
  - Determines the location based on the IP address.
  - Fetches the current temperature for the location.
  - Returns a JSON response containing the client's IP address, location, and a greeting message including the temperature.

## API Endpoint

### [GET] `/api/hello`

**Query Parameters:**

- `visitor_name` (optional): The name of the visitor. Default is "Guest".

**Example Request:**


**Example Response:**
```json
{
  "client_ip": "127.0.0.1",
  "location": "New York",
  "greeting": "Hello, Mark!, the temperature is 11 degrees Celsius in New York"
}
