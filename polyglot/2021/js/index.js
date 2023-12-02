const day = process.argv[2];
const test = !!Number(process.argv[3]);

console.log(process.argv);
console.log(`day? ${day}`);
console.log(`test? ${test}`);

command = require(`./commands/d${day}.js`);
command.setup(test);
command.part1();
command.part2();
