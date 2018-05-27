#!/bin/bash

export ROOT_SITE=www.epfl.ch
CSV_FILE=/srv/$WP_ENV/jahia2wp/src/vent-demo/data/ventilation-innov.csv

ROOT_WP_DEST=/srv/$WP_ENV/$ROOT_SITE/htdocs

# This DEMO reads the csv and migrates the content under the ROOT_SITE
# ***** It does not export missing sites nor creates destination sites. ********

# Look at demo.sh if you need to see an example to generate and export sites.
# Uncomment the following lines to try to do it for this example:

# Generate target site (as stated in the rules ventilation-innov.csv)
# python jahia2wp.py generate $WP_ENV https://www.epfl.ch/innovation --admin-password=admin --extra-config=vent-demo/data/generate-enfr.yml
# Move the accred and tequila plugins to let for local connections
# find /srv/$WP_ENV/$ROOT_SITE/ -type d \( -iname "accred" -o -iname "tequila" \) -print0 | xargs -0 -I {} mv {} {}.bak

# Export the required sites
# demo_site_export='/tmp/j2wp_demosite.csv'
# echo 'wp_site_url,wp_tagline,wp_site_title,site_type,openshift_env,category,theme,theme_faculty,status,installs_locked,updates_automatic,langs,unit_name,Jahia_zip,comment' > $demo_site_export;
# echo 'https://vpi.epfl.ch,#parser,#parser,wordpress,int,GeneralPublic,epfl-master,#parser,yes,yes,yes,#parser,vpi,vpiv,' >> $demo_site_export;
# echo 'https://social-impact.epfl.ch,#parser,#parser,wordpress,int,GeneralPublic,epfl-master,#parser,yes,yes,yes,#parser,vpi,social-impact,' >> $demo_site_export;
# echo 'https://entreprises.epfl.ch,#parser,#parser,wordpress,int,GeneralPublic,epfl-master,#parser,yes,yes,yes,#parser,vpi,entreprises,migrable' >> $demo_site_export;
# echo 'https://clipair.epfl.ch,#parser,#parser,wordpress,int,GeneralPublic,epfl-blank,#parser,yes,yes,yes,#parser,liv,clipair,' >> $demo_site_export;
# echo 'https://bioinspired.epfl.ch,#parser,#parser,wordpress,int,GeneralPublic,epfl-master,#parser,yes,yes,yes,#parser,ip,bioinspired,' >> $demo_site_export;
# echo 'https://sportstech.epfl.ch,#parser,#parser,wordpress,int,GeneralPublic,epfl-master,#parser,yes,yes,yes,#parser,vpi,sport,migrable' >> $demo_site_export;
# echo "**** Make sure the wp_exporter has port 8080 to enable the API Rest during export. By default only for jahia2wp-httpd"
# echo "IF the export failed, do a clean like: python jahia2wp.py clean $WP_ENV http://vpi.epfl.ch"
# PYTHONIOENCODING="utf-8" python jahia2wp.py export-many $demo_site_export --admin-password=admin

# 1) Delete all content (pages, media, menu, sidebars) from target WP destination tree.
./vent-demo/utils/del-posts.sh "$ROOT_WP_DEST/innovation"

# 2) RUN the migration. Force utf8 for io since c2c container uses a variant of ascii for io.
PYTHONIOENCODING="utf-8" python jahia2wp.py migrate-urls $CSV_FILE $WP_ENV --root_wp_dest=$ROOT_WP_DEST