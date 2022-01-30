#!/bin/sh 
while [ TRUE ]; do
    #Current number of files
    files=$(ls -1 /local/backups/ | wc -l)
    
    #Finding current total size of files
    bytes=$(du -b /local/backups/ | cut -f1)
    
    # If total amount of files is greater than specified, send an e-mail
    if [ "$files" -gt "$1" ]; then
        echo "Warning! Number of files in /local/backups directory is more than $1" | mail -s "Backup files alert!" root@data
    fi
    
    # If total size of files in bytes is greater than specified, send an e-mail
    if [ "$bytes" -gt "$2" ]; then
        echo "Warning! Total size of /local/backups directory is more than $2 bytes" | mail -s "Backup size alert!" root@data
    fi

    # A time between check-ups.
    sleep "$3"
done





