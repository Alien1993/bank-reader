const API_URL = './api/movements/';

const status = (response) => {
  if (response.status >= 200 && response.status < 300) {
    return Promise.resolve(response);
  }
  return Promise.reject(new Error(response.statusText));
};

const json = response => response.json();

const error = (er) => {
  // TODO: Show some kind of alert to user
  console.error(er);
};

const buildURL = (params) => {
  // Creates params string
  const formattedParams = Object.keys(params)
    .map(key => (`${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`))
    .join('&');

  return `${API_URL}?${formattedParams}`;
};

// Fetches data from API with given params and executes callback if  data is
// returned successfully
const getMovements = async (params, callback) => {
  // Builds URL and adds passed parameters
  const url = buildURL(params);

  await fetch(url)
    .then(status)
    .then(json)
    .then((data) => {
      callback(data);
    })
    .catch(error);
};

export default (getMovements);
