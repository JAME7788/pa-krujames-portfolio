const fs = require('node:fs');
const vm = require('node:vm');
const {stripTypeScriptTypes} = require('node:module');
const source = fs.readFileSync('C:/Users/KruJames/.gemini/antigravity/scratch/krujamesoncom-website/src/data/p1HourlyLessonOutlines.ts', 'utf8');
const result = stripTypeScriptTypes(source);
import('data:text/javascript;base64,' + Buffer.from(result).toString('base64')).then(module => {
  const data = module.p1HourlyLessonOutlines.slice(4, 8);
  fs.writeFileSync('qa-pa/current_outlines.json', JSON.stringify(data, null, 2));
  console.log(data.map(x => x.title).join('\n'));
});
