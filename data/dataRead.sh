#!/bin/sh

now=$(date +"%d.%m.%Y_%H%M%S")
# If wc output gives us more than 3 we make a backup archive at /local/backups
if [ "$(ls -1 /local/files | wc -l)" -gt 3 ] 
    then
        tar -czf /local/backups/data_backup."$now".tgz /local/files/data*
        rm /local/files/data*
fi
# Let's create a data file containing all the data in the webapp database
sudo mysql -e "SELECT Articles.id, magazines.name AS Magazine, article_types.type AS Type, author.author AS Author 
FROM (((webapp.Articles
INNER JOIN webapp.magazines ON Articles.magazines_id = magazines.id)
INNER JOIN webapp.article_types ON Articles.article_types_id = article_types.id)
INNER JOIN webapp.author ON Articles.author_id = author.id) ORDER BY Articles.id;" | tee /local/files/data."${now}".txt

