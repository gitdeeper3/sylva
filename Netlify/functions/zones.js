const { createClient } = require('@supabase/supabase-js');

exports.handler = async (event, context) => {
  // CORS headers للاتصال من sylva.netlify.app
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json',
    'Cache-Control': 'public, max-age=300'
  };

  // Preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  try {
    // المفاتيح السرية من متغيرات البيئة في Netlify
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Supabase credentials not configured');
    }

    const supabase = createClient(supabaseUrl, supabaseKey);

    // جلب جميع مناطق الحرائق مع بيانات أنواع الوقود
    const { data: zones, error } = await supabase
      .from('fire_zones')
      .select(`
        *,
        fuel_types!fire_zones_primary_fuel_code_fkey (
          fuel_name,
          validation_pod,
          weight_wind,
          weight_dfm
        )
      `)
      .order('zone_name');

    if (error) throw error;

    // جلب إحصائيات أنواع الوقود
    const { data: fuelTypes, error: fuelError } = await supabase
      .from('fuel_types')
      .select('*')
      .order('fuel_name');

    if (fuelError) throw fuelError;

    // حساب إحصائيات شمال إفريقيا
    const northAfricaCountries = ['Morocco', 'Algeria', 'Tunisia', 'Libya', 'Egypt'];
    const northAfricaZones = zones?.filter(z => 
      northAfricaCountries.includes(z.region)
    ) || [];

    // حساب مستويات الخطر
    const riskLevels = {
      critical: 0,
      veryHigh: 0,
      high: 0,
      moderate: 0
    };

    zones?.forEach(zone => {
      const distance = zone.wui_distance_km || 2.0;
      if (distance < 1.5) riskLevels.critical++;
      else if (distance < 2.0) riskLevels.veryHigh++;
      else if (distance < 2.5) riskLevels.high++;
      else riskLevels.moderate++;
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        timestamp: new Date().toISOString(),
        data: {
          zones: zones || [],
          fuelTypes: fuelTypes || [],
          stats: {
            totalZones: zones?.length || 0,
            northAfricaZones: northAfricaZones.length,
            northAfricaCountries: northAfricaZones.reduce((acc, zone) => {
              acc[zone.region] = (acc[zone.region] || 0) + 1;
              return acc;
            }, {}),
            totalStructures: zones?.reduce((sum, z) => sum + (z.wui_structures_estimate || 0), 0) || 0,
            fuelTypesCount: fuelTypes?.length || 0,
            riskDistribution: riskLevels
          }
        }
      })
    };

  } catch (error) {
    console.error('❌ Supabase error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};
