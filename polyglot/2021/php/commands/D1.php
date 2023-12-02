<?php

namespace Commands;

class D1 {
    public function runCommand(array $argv) {
        if (isset($argv[1])) {
            $part = $argv[1];
            echo "Part: $part";
        }
    }

    public function part_1($part) {
        echo "Print: $part";
    }

    public function part_2($part) {
        echo "PART2 $part";
    }
}
