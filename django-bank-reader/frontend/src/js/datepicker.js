const Pikaday = require('pikaday');
const moment = require('moment');

const DISPLAY_DATE_FORMAT = 'DD-MM-YYYY';

let startDate = moment().add(-14, 'days').toDate();
let endDate = moment().toDate();

let updateStartDate;
let updateEndDate;

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
  format: DISPLAY_DATE_FORMAT,
  defaultDate: new Date(),
  firstDay: 1,
  showDaysInNextAndPreviousMonths: true,
  onSelect: dateFromOnSelect,
});

const dateToPicker = new Pikaday({
  field: document.getElementById('date-to-input'),
  format: DISPLAY_DATE_FORMAT,
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
  moment(startDate).format(DISPLAY_DATE_FORMAT);

document.getElementById('date-to-input').value =
  moment(endDate).format(DISPLAY_DATE_FORMAT);

updateStartDate();
updateEndDate();
