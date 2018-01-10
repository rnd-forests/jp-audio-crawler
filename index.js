'use strict';

const fs = require('fs');
const uniqid = require('uniqid');
const download = require('download');
const puppeteer = require('puppeteer');

function isAborted(request) {
    const excludedUrls = [
        'http://www.google-analytics.com/ga.js',
        'https://www.google-analytics.com/ga.js',
    ];
    const excludedResources = ['image', 'stylesheet', 'font'];

    return excludedResources.includes(request.resourceType) || excludedUrls.includes(request.url);
}

async function getSpeech(text) {
    let audio = '';
    const baseUrl = 'http://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index';

    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();

    await page.setRequestInterception(true);

    page.on('request', request => {
        if (isAborted(request)) {
            request.abort();
        } else {
            if (request.url.endsWith('.wav')) {
                audio = request.url;
            }
            request.continue();
        }
    });

    await page.goto(baseUrl);

    await page.type('textarea[name="data[Phrasing][text]"]', text);

    const executionBtnSelector = 'input[value="実行"]';
    await page.click(executionBtnSelector);

    const createBtnSelector = 'input[value="作成"]';
    await page.waitForSelector(createBtnSelector, {visible: true});
    await page.click(createBtnSelector);

    const playBtnSelector = 'input[value="再生"]';
    await page.waitForSelector(playBtnSelector, {visible: true});
    await page.click(playBtnSelector);

    await browser.close();

    return audio;
}

function downloadSpeech(text, audioDir='audio') {
    getSpeech(text).then(audio => {
        console.log(audio);
        let target = audioDir + '/' + uniqid() + '.wav';
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
