const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const url = 'https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did=SE17&type=balance_VI';

axios(url)
  .then(response => {
    const html = response.data;
    const $ = cheerio.load(html);
    const table = $('table').eq(3);
    const rows = [];

    table.find('tr').each((i, elem) => {
      const cells = $(elem).find('td').map((i, elem) => $(elem).text()).get();
      if (cells.length > 0) {
        rows.push(cells);
      }
    });

    const header = rows.shift().map((title, index) => ({ id: index.toString(), title }));
    const records = rows.map(row => row.reduce((obj, val, i) => ({ ...obj, [i]: val }), {}));

    const csvWriter = createCsvWriter({
      path: 'output.csv',
      header
    });

    csvWriter.writeRecords(records)
      .then(() => console.log('The CSV file was written successfully'));
  })
  .catch(console.error);
