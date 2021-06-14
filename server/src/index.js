require('dotenv').config();

// Express App Setup
const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const cors = require('cors');
const uuid = require('uuid/v4');

// Config
const config = require('./config');

// Initialization
const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

// Postgres client
const { Pool } = require('pg');
const pgClient = new Pool({
  user: config.pgUser,
  host: config.pgHost,
  database: config.pgDatabase,
  password: config.pgPassword,
  port: config.pgPort
});
pgClient.on('error', () => console.log('Lost Postgres connection'));

// Express route handlers
app.get('/v1/test', (req, res) => {
  const test = {"foo": "bar"}
  res.status(200).json(test);
});

// Get all data
app.get('/v1/tickers', async (req, res) => {
  const items = await pgClient.query('SELECT * FROM public."wsb-test"');
  const tickers = {
    result: items.rows
  };
  res.status(200).json(tickers);
});

// Server
const port = process.env.PORT || 3001;
const server = http.createServer(app);
server.listen(port, () => console.log(`Server running on port ${port}`));