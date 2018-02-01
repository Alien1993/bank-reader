import Highcharts from 'highcharts';

const moment = require('moment');

const createBarChart = (container, series) => {
  Highcharts.chart(container, {
    chart: {
      type: 'column',
      zoomType: 'xy',
    },

    legend: {
      enabled: false,
    },

    title: {
      text: '',
    },

    plotOptions: {
      column: {
        stacking: 'normal',
        dataLabels: {
          enabled: false,
        },
      },
    },

    xAxis: {
      title: {
        text: 'Date',
      },
      type: 'datetime',
    },

    yAxis: {
      title: {
        text: 'Amount',
      },
      stackLabels: {
        enabled: true,
      },
      startOnTick: false,
      endOnTick: false,
    },

    tooltip: {
      useHTML: true,
      headerFormat: '<table>',
      pointFormatter() {
        return `<tr><th>Amount</th><td>${this.y}</td></tr>
        <tr><th>Date</th><td>${moment(this.x).format('ddd, Do MMMM YYYY')}</td></tr>
        <tr><th>Category</th><td>${this.name}</td></tr>
        <tr>${this.description}</tr>`;
      },
      footerFormat: '</table>',
      followPointer: true,
    },

    series,
  });
};


export default createBarChart;
