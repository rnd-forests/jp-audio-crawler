'use strict';

const fs = require('fs');
const md5 = require('md5');
const download = require('download');
const puppeteer = require('puppeteer');

async function getSpeech(text) {
    let audio = "";
    let promises = [];

    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();

    // Track the requests and find the request URL to the audio file
    page.on('request', (request) => {
        if (request.url.endsWith('.wav')) {
            audio = request.url;
        }
    });

    // Go to the destination page
    await page.goto('http://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index');

    // Fill the desired Japanese text into the textarea
    await page.type('textarea[name="data[Phrasing][text]"]', text);

    // Click on execution button
    const executionBtnSelector = 'input[value="実行"]';
    await page.click(executionBtnSelector);

    // Synthesize the audio
    const createBtnSelector = 'input[value="作成"]';
    await page.waitForSelector(createBtnSelector, {visible: true});
    await page.click(createBtnSelector);

    // Play the audio in order to get the URL
    const playBtnSelector = 'input[value="再生"]';
    await page.waitForSelector(playBtnSelector, {visible: true});
    await page.click(playBtnSelector);

    // We're done
    await browser.close();

    return audio;
}

function downloadSpeech(text, audioDir='audio') {
    getSpeech(text).then(audio => {
        let target = audioDir + '/' + md5(text) + '.wav';
        download(audio).then(stream => {
            fs.writeFileSync(target, stream);
        });
    });
}

const texts = [
    '小林さんは、その話を疑っているようだ',
    '本当だと思っている',
    '本当ではないと思っている',
    'よく知っている',
    'よく知らない'
];

for (let text of texts) {
    downloadSpeech(text);
}
