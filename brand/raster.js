const sharp = require('/Users/pratham/madeboring/site/node_modules/sharp');
const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync('assets/jobs.json', 'utf8'));
(async () => {
  for (const j of jobs) {
    const buf = fs.readFileSync(j.src);
    const meta = await sharp(buf).metadata();
    // render the vector at the exact output size instead of scaling a raster
    const density = Math.min(2400, Math.max(72, 72 * (j.w / meta.width)));
    let img = sharp(buf, { density });
    img = j.h ? img.resize(j.w, j.h, { fit: 'fill' }) : img.resize({ width: j.w });
    await img.png({ compressionLevel: 9 }).toFile(j.out);
  }
  for (const pal of ['field', 'forest']) {
    const bufs = [16, 32, 48].map(s => [s, fs.readFileSync(`assets/${pal}/png/icon-${s}.png`)]);
    const n = bufs.length;
    const head = Buffer.alloc(6);
    head.writeUInt16LE(0, 0); head.writeUInt16LE(1, 2); head.writeUInt16LE(n, 4);
    let off = 6 + 16 * n; const dirs = [];
    for (const [s, b] of bufs) {
      const d = Buffer.alloc(16);
      d.writeUInt8(s % 256, 0); d.writeUInt8(s % 256, 1);
      d.writeUInt16LE(1, 4); d.writeUInt16LE(32, 6);
      d.writeUInt32LE(b.length, 8); d.writeUInt32LE(off, 12);
      off += b.length; dirs.push(d);
    }
    fs.writeFileSync(`assets/${pal}/png/favicon.ico`,
      Buffer.concat([head, ...dirs, ...bufs.map(x => x[1])]));
  }
  console.log('rasterised', jobs.length, 'files + 2 ico');
})();
