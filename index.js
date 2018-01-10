const { Chromeless } = require('chromeless')

async function run() {
    const chromeless = new Chromeless({
        debug: true,
        launchChrome: true
    })

    const audio = await chromeless
        .goto('http://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index')
        .type('アクセント変形を考慮した上で文としてのピッチパターンを表示します', 'textarea[name="data[Phrasing][text]"]')
        .click('input[value="実行"]')
        .click('input[value="作成"')
        .click('input[value="再生"]')
        .wait(100)
        .evaluate(() => {
            return window.location
            let baseuri = window.baseuri;
            return baseuri + 'tmp/' + wav_filename;
        });

    console.log(audio)

    await chromeless.end()
}

run().catch(console.error.bind(console))
