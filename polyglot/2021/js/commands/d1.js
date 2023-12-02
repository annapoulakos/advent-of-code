const files = require('../utils/filesystem.js');
const utils = require('../utils/utils.js');

var _internal = {};

function _setup(test) {
    const url = `../data/day-${test?'ex-':''}1.txt`;
    _internal.data = files.load_int(url);
    console.log(_internal.data.length);
}

function _part1() {
    const vals = _internal.data.slice(1).map((v,i) => {
        return v > _internal.data[i]? 1: 0;
    });
    console.log(vals.reduce((a,b) => a+b, 0));
}

function _part2() {
    console.log('d1.part2');
    let r = utils.range(_internal.data.length - 2);
    let vals = _internal.data.map((v,i) => {
        return [v, _internal.data[i+1], _internal.data[i+2]].reduce((a,b) => a+b, 0);
    });
    let fin = vals.slice(1).map((v,i) => v > _internal.data[i]? 1: 0);
    console.log(fin.reduce((a,b) => a+b, 0));
}



module.exports = {
    setup: _setup,
    part1: _part1,
    part2: _part2,
};
