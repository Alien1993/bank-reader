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

const currencies = {
  EUR: '€',
  USD: '$',
};

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

const createMovementListElement = (movement) => {
  const item = document.createElement('li');

  // Date
  const date = document.createTextNode(movement.date);
  const dateParagraph = document.createElement('p');
  dateParagraph.className = 'date';
  dateParagraph.appendChild(date);

  // Description
  const description = document.createTextNode(movement.description);
  const descriptionParagraph = document.createElement('p');
  descriptionParagraph.className = 'description';
  descriptionParagraph.appendChild(description);

  // Amount
  const amount = document.createTextNode(`${Math.abs(movement.amount).toFixed(2)} ${currencies[movement.amount_currency]}`);
  const amountHeader = document.createElement('h4');
  amountHeader.className = 'amount';
  amountHeader.appendChild(amount);

  const amountDescriptionContainer = document.createElement('div');
  amountDescriptionContainer.className = 'amount-description-container';
  amountDescriptionContainer.appendChild(amountHeader);
  amountDescriptionContainer.appendChild(descriptionParagraph);

  item.appendChild(dateParagraph);
  item.appendChild(amountDescriptionContainer);

  return item;
};

const updateMovementList = (movements, container) => {
  // Removes currently shown Movements
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }

  const fragment = document.createDocumentFragment();

  // Creates and appends list of movements to container
  movements.forEach((movement) => {
    const el = createMovementListElement(movement);
    fragment.appendChild(el);
  });
  container.appendChild(fragment);
};

const globalProcessor = (data) => {
  const bubbleCategories = new Set();
  const bubbleData = [];
  const barData = [{ data: [] }];
  const greatestSpendings = [];
  const smallestSpendings = [];

  data.forEach((movement) => {
    // Only losses should be shown
    if (movement.amount < 0) {
      bubbleCategories.add(movement.category);
      bubbleData.push(bubbleChartProcessor(movement));
      barData[0].data.push(barChartProcessor(movement));

      greatestSpendings.push(movement);
      smallestSpendings.push(movement);
    }
  });

  // Sorts spendings
  greatestSpendings.sort((m1, m2) => {
    const amount1 = Number(m1.amount);
    const amount2 = Number(m2.amount);
    if (amount1 < amount2) {
      return -1;
    } else if (amount1 > amount2) {
      return 1;
    }
    return 0;
  });

  smallestSpendings.sort((m1, m2) => {
    const amount1 = Number(m1.amount);
    const amount2 = Number(m2.amount);
    if (amount1 > amount2) {
      return -1;
    } else if (amount1 < amount2) {
      return 1;
    }
    return 0;
  });

  // We only want to see some Movements for these lists
  greatestSpendings.splice(5);
  smallestSpendings.splice(5);

  updateMovementList(greatestSpendings, document.getElementById('greatest-spendings-list'));
  updateMovementList(smallestSpendings, document.getElementById('smallest-spendings-list'));

  createBubbleChart('bubble-chart-container', bubbleCategories, bubbleData);
  createBarChart('bar-chart-container', barData);
};

export { bubbleChartProcessor, barChartProcessor, globalProcessor };
