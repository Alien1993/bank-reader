import getMovements from '../client';

// Mocks fetch
global.fetch = require('jest-fetch-mock');

it('Verifies callback is executed correctly after sucessful response', async () => {
  fetch.mockResponse(JSON.stringify([{ data: 1 }, { data: 2 }]), { status: 200 });

  const mockCallback = jest.fn();
  const params = { date_from: '2017-12-04', date_to: '2018-01-04' };

  await getMovements(params, mockCallback);

  expect(mockCallback).toBeCalled();
  expect(mockCallback).toBeCalledWith([{ data: 1 }, { data: 2 }]);
});

it('Verifies callback is not executed after failure response', async () => {
  fetch.mockReject(new Error('Some Error'));

  const mockCallback = jest.fn();
  const params = { date_from: '2017-12-04', date_to: '2018-01-04' };

  await getMovements(params, mockCallback);

  expect(mockCallback).not.toBeCalled();
});
