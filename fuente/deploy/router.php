<?php
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$f = $_SERVER['DOCUMENT_ROOT'] . $p;
if ($p !== '/' && substr($p,-1) !== '/' && !file_exists($f)) { http_response_code(404); readfile($_SERVER['DOCUMENT_ROOT'].'/404.html'); return true; }
return false;
