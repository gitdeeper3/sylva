exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
  };

  try {
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    const status = {
      service: 'SYLVA Operational Intelligence',
      version: '2.5.0',
      supabase: {
        configured: !!(supabaseUrl && supabaseKey),
        url: supabaseUrl ? '✓' : '✗',
        key: supabaseKey ? '✓' : '✗'
      },
      timestamp: new Date().toISOString(),
      endpoints: {
        'get-fire-zones': '/api/get-fire-zones'
      }
    };

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(status, null, 2)
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
