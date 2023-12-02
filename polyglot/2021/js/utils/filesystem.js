const fs = require('fs');

function _load_raw(filepath) {
    try {
        const data = fs.readFileSync(filepath, 'utf8');
        return data.trim();
    } catch (err) {
        console.error(err);
    }
}

function _load_lines(filepath) {
    const raw = _load_raw(filepath);

    return raw.split('\n').map(i => i.trim());
}

function _load_ints(filepath) {
    const raw = _load_raw(filepath);

    return raw.split('\n').map(i => parseInt(i.trim()));
}

module.exports = {
    load_raw: _load_raw,
    load_lines: _load_lines,
    load_int: _load_ints,
};
