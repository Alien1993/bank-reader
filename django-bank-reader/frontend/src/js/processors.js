import createBubbleChart from './bubble-chart-controller';
import createBarChart from './bar-chart-controller';

const moment = require('moment');

const dayColors = [
  '#F44336',
  '#9C27B0',
  '#3F51B5',
  '#00BCD4',
  '#4CAF50',
  '#FFC107',
  '#FF5722',
];

// Processes a single movement and returns an objects
// representing a single bubble in a Bubble Chart
const bubbleChartProcessor = (movement) => {
  const date = moment.utc(movement.date, 'YYYY-MM-DD');
  return {
    // Sets movement amount has visual z so that smaller bubbles
    // are drawn above bigger one and easier to select
    zIndex: movement.amount,
    data: [{
      y: date.valueOf('x'),
      z: Math.abs(movement.amount),
      name: movement.category,
      color: dayColors[date.weekday()],
      description: movement.description,
    }],
  };
};

const barChartProcessor = (movement) => {
  const date = moment.utc(movement.date, 'YYYY-MM-DD');
  return {
    y: Math.abs(movement.amount),
    x: date.valueOf('x'),
    name: movement.category,
    color: dayColors[date.weekday()],
    description: movement.description,
  };
};

const globalProcessor = (data) => {
  const bubbleCategories = new Set();
  const bubbleData = [];
  const barData = [{ data: [] }];

  data.forEach((movement) => {
    // Only losses should be shown on Bubble and Bar charts
    if (movement.amount < 0) {
      bubbleCategories.add(movement.category);
      bubbleData.push(bubbleChartProcessor(movement));
      barData[0].data.push(barChartProcessor(movement));
    }
  });

  createBubbleChart('bubble-chart-container', bubbleCategories, bubbleData);
  createBarChart('bar-chart-container', barData);
};

export { bubbleChartProcessor, barChartProcessor, globalProcessor };
