const API_URL = 'http://localhost:8000/api/attacks';
const COUNTRY_COORDS_URL = 'https://restcountries.com/v3.1/all?fields=cca2,latlng,name';
const UPDATE_INTERVAL_MS = 60 * 1000; // 1 minute

let countryData = null;
let globeInstance = null;

document.addEventListener('DOMContentLoaded', () => {

  globeInstance = Globe()
    (document.getElementById('globeViz'))
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
    .pointColor(() => '#ff6347')
    .onPointClick(d => {
      alert(`
        Country: ${d.countryName}
        Rank: ${d.rank}
        Value: ${d.value} requests
      `);
    });

  // This function fetches all the necessary data
  async function fetchAllData() {
    try {
      const [apiResponse, countriesResponse] = await Promise.all([
        fetch(API_URL),
        fetch(COUNTRY_COORDS_URL)
      ]);

      if (!apiResponse.ok || !countriesResponse.ok) {
        throw new Error('Failed to fetch data from one or more sources.');
      }

      const apiData = await apiResponse.json();
      countryData = await countriesResponse.json();

      console.log('Fetched API data:', apiData);
      console.log('Fetched Country data:', countryData);

      updateGlobe(apiData);

    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  // Function to get country coordinates from alpha2 code
  function getCountryCoords(alpha2) {
    if (!countryData) return null;
    // The API returns an array, so we need to find the correct country object
    const country = countryData.find(c => c.cca2 === alpha2);
    if (country) {
      const [lat, lng] = country.latlng;
      return { lat, lng };
    }
    return null;
  }

  // Update the globe visualization with the latest data
  function updateGlobe(data) {
    if (data && data.cloudflare_geo_data && data.cloudflare_geo_data.top_0) {
      const geoData = data.cloudflare_geo_data.top_0;

      const attackLocations = geoData.map(d => {
        const coords = getCountryCoords(d.originCountryAlpha2);
        if (coords) {
          return {
            ...coords,
            size: d.value / 10,
            countryName: d.originCountryName,
            value: d.value,
            rank: d.rank
          };
        }
        return null;
      }).filter(d => d !== null);

      globeInstance
        .pointsData(attackLocations)
        .pointAltitude(d => d.size)
        .pointColor(d => '#ff6347');
    }
  }

  // --- Data Loading and Initialization ---
  fetchAllData();
  setInterval(fetchAllData, UPDATE_INTERVAL_MS);
});