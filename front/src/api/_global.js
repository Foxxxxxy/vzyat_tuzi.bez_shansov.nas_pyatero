export const SERVER_ENDPOINT =
  import.meta.env.MODE === 'development'
    ? 'http://158.160.56.253:3030'
    : `http://${window.location.hostname}:3030`
