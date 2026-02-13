// SYLVA API Configuration
// Copy to api-keys.local.js and add your keys

module.exports = {
  openweather: {
    key: process.env.OPENWEATHER_API_KEY || 'YOUR_API_KEY',
    units: 'metric'
  },
  sentinel: {
    client_id: process.env.SENTINEL_CLIENT_ID || 'YOUR_CLIENT_ID',
    client_secret: process.env.SENTINEL_CLIENT_SECRET || 'YOUR_CLIENT_SECRET'
  }
};
