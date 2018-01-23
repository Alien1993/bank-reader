import getMovements from './client';

const moment = require('moment');

const PARSED_DATE_FORMAT = 'DD-MM-YYYY';
const DATE_FORMAT = 'YYYY-MM-DD';

const fetch = () => {
  const dateFrom = document.getElementById('date-from-input');
  const dateTo = document.getElementById('date-to-input');
  const amountFrom = document.getElementById('amount-from-input');
  const amountTo = document.getElementById('amount-to-input');

  const params = {
    date_from: moment(dateFrom.value, PARSED_DATE_FORMAT).format(DATE_FORMAT),
    date_to: moment(dateTo.value, PARSED_DATE_FORMAT).format(DATE_FORMAT),
    amount_from: amountFrom.value,
    amount_to: amountTo.value,
  };

  getMovements(params, console.log);
};

document.getElementById('fetch-button').onclick = fetch;

export default (fetch);
