const Pikaday = require('pikaday');
const moment = require('moment');

const DATE_FORMAT = 'DD-MM-YYYY';

let startDate = moment().add(-14, 'days').toDate();
let endDate = moment().toDate();

// let dateFromPicker;
// let dateToPicker;

let updateStartDate;
let updateEndDate;

// const updateStartDate = () => {
//   dateFromPicker.setStartRange(startDate);
//   dateToPicker.setStartRange(startDate);
//   dateToPicker.setMinDate(startDate);
// };

// const updateEndDate = () => {
//   dateFromPicker.setEndRange(endDate);
//   dateFromPicker.setMaxDate(endDate);
//   dateToPicker.setEndRange(endDate);
// };

function dateFromOnSelect() {
  startDate = this.getDate();
  updateStartDate();
}

function dateToOnSelect() {
  endDate = this.getDate();
  updateEndDate();
}

const dateFromPicker = new Pikaday({
  field: document.getElementById('date-from-input'),
  format: DATE_FORMAT,
  defaultDate: new Date(),
  firstDay: 1,
  showDaysInNextAndPreviousMonths: true,
  onSelect: dateFromOnSelect,
});

const dateToPicker = new Pikaday({
  field: document.getElementById('date-to-input'),
  format: DATE_FORMAT,
  defaultDate: new Date(),
  firstDay: 1,
  showDaysInNextAndPreviousMonths: true,
  onSelect: dateToOnSelect,
});

updateStartDate = () => {
  dateFromPicker.setStartRange(startDate);
  dateToPicker.setStartRange(startDate);
  dateToPicker.setMinDate(startDate);
};

updateEndDate = () => {
  dateFromPicker.setEndRange(endDate);
  dateFromPicker.setMaxDate(endDate);
  dateToPicker.setEndRange(endDate);
};


dateFromPicker.gotoToday();
dateToPicker.gotoToday();

document.getElementById('date-from-input').value =
  moment(startDate).format(DATE_FORMAT);

document.getElementById('date-to-input').value =
  moment(endDate).format(DATE_FORMAT);

updateStartDate();
updateEndDate();

export default (dateFromPicker);
