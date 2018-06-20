<?php

# This script is meant for "wp eval-file".
#
# Usage:
#
#   wp --path=..... \
#      eval-file importer.php [ -fetch-attachments ] <wxr_file.xml>


$importer_plugin_file = WP_PLUGIN_DIR .
                      '/wordpress-importer/wordpress-importer.php';
if (! is_file($importer_plugin_file)) {
    ?>

File <?php echo $importer_plugin_file; ?> Not found

Please install the wordpress-importer plugin, e.g.

  wp --path=... plugin install --activate wordpress-importer

<?php
    die();
}

if (function_exists("wordpress_importer_init")) {
    ?>

Please run with wp-importer plugin skipped (add
--skip-plugins=wordpress-importer to your command line)

<?php
    die();
}

global $argv;
$filename = end($argv); reset($argv);
if (! is_file($filename)) {

    ?>
File not found: <?php echo $filename; ?>

Usage : wp eval [...] <filename>

<?php
    die();
}

// WP_LOAD_IMPORTERS must be set before loading the plugin (hence why
// the user must set the command line to skip it; see above)
define('WP_LOAD_IMPORTERS', true);
define('IMPORT_DEBUG', true);
require("$importer_plugin_file");
wordpress_importer_init();

$fetch_attachments = FALSE !== array_search("-fetch-attachments", $argv);
do_import($filename, $fetch_attachments);

############################# FUNCTIONS ##################################

function html2text ($html) {
    $html = preg_replace("|<br[ ]*[/]?>|", "\n", $html);
    $html = preg_replace("|<[/]?p[ ]*[/]?>|", "\n", $html);
    $html = preg_replace("|<[^>]*>|", "\n", $html);

    $html = str_replace("&#8220;", '"', $html);
    $html = str_replace("&#8221;", '"', $html);

    return $html;
}

function accumulate_and_transform ($buf, $phase) {
    static $accumulator = "";
    $accumulator .= $buf;
    $accumulator = html2text($accumulator);
    [$out, $accumulator] = explode("<", $accumulator);
    return $out;
}

function do_import ($filename, $fetch_attachments = false) {
    global $wp_import;
    $wp_import->fetch_attachments = $fetch_attachments;
    ob_start("accumulate_and_transform", 1);
    try {
        $wp_import->import($filename);
    } finally {
        ob_flush();
        ob_end_clean();
    }
}
