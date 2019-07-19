/**
 * @see https://codeburst.io/a-guide-to-automating-scraping-the-web-with-javascript-chrome-puppeteer-node-js-b18efb9e9921
 * @see https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md#
 */
//import  Puppeteer from 'puppeteer';
const Puppeteer = require('puppeteer');

const urls = [
  {
    name: 'local-hub',
    url: 'http://192.168.1.254/00000110500/gui/#/basicStatus',
  },
];

const chromeExecutableLocation = '/usr/bin/chromium-browser';

const timeRegex = /[TZ\:\.\-]/gi;


async function getPic(page) {
  const browser = await Puppeteer.launch({  executablePath: chromeExecutableLocation});
  const impression = await browser.newPage();
  await impression.goto(page.url);
  await impression.waitFor(1000 * 10);
  const timestamp = new Date();
  const timestampString = timestamp.toISOString().replace(timeRegex, '');
  await impression.screenshot({path: `/home/pi/logs/grabWeb/${timestampString}-${page.name}.png`});
  await browser.close();
}

urls.forEach(getPic);
