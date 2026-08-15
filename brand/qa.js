const sharp = require('/Users/pratham/madeboring/site/node_modules/sharp');
const S = '/private/tmp/claude-502/-Users-pratham/4eed19d0-0848-4e3a-a61e-012788cbfae7/scratchpad/qa';
(async () => {
  const cells = [];
  for (const [f, n] of [['icon-16',16],['icon-32',32],['icon-48',48],['icon-64',64],['apple-touch-icon',180],['maskable-512',512]]) {
    // nearest-neighbour blow-up so pixel damage at real size is visible
    cells.push(await sharp(`assets/field/png/${f}.png`)
      .resize(300, 300, { kernel: 'nearest' }).toBuffer());
  }
  const W = 300, g = 10;
  await sharp({ create: { width: W*6 + g*7, height: W + g*2, channels: 3,
    background: '#999' } })
    .composite(cells.map((input, i) => ({ input, left: g + i*(W+g), top: g })))
    .png().toFile(`${S}/icons.png`);
  console.log('qa sheet written');
})();
