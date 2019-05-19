# [eips.exposed](https://eips.exposed)

Ethereum EIP explorer

## Project Structure

### eips_exposed/processor

This processes the official EIPs GitHub repository and inserts them into a PostgreSQL database.

### eips_exposed/server

The Tornado server handling serving the frontend and GraphQL backend

### eips_exposed/frontend

The source for the frontend application.
