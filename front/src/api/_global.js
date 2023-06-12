export const SERVER_ENDPOINT =
  import.meta.env.MODE === 'development'
    ? 'http://localhost:3030'
    : `http://${window.location.hostname}:3030`
