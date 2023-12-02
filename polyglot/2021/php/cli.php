#!/usr/bin/php
<?php

if (php_sapi_name() !== 'cli') {
    exit;
}

require __DIR__ . '/vendor/autoload.php';

$day = strtoupper($argv[1]);
$part = $argv[2];


use Commands\D1;

$command = new $day();
$command->{'part_'.$part}($part);
