import Highcharts from 'highcharts';

require('highcharts/highcharts-more')(Highcharts);

const moment = require('moment');

// Creates a new Bubble Chart inside container, settings categories on Y axis
const createBubbleChart = (container, categories, series) => {
  Highcharts.chart(container, {
    chart: {
      type: 'bubble',
      plotBorderWidth: 1,
      zoomType: 'xy',
    },

    legend: {
      enabled: false,
    },

    title: {
      text: '',
    },

    yAxis: {
      gridLineWidth: 1,
      title: {
        text: 'Date',
      },
      type: 'datetime',
    },

    xAxis: {
      title: {
        text: 'Categories',
      },
      type: 'category',
      categories,
    },

    tooltip: {
      useHTML: true,
      headerFormat: '<table>',
      pointFormatter() {
        return `<tr><th>Amount</th><td>${this.z}</td></tr>
          <tr><th>Date</th><td>${moment(this.y).format('ddd, Do MMMM YYYY')}</td></tr>
          <tr>${this.description}</tr>`;
      },
      footerFormat: '</table>',
      followPointer: true,
    },

    series,
  });
};


export default createBubbleChart;
