find backup -type f | grep -v ".sha256" > flst.txt
feh --action1 'mvrel.sh "%F" dup' --action2 'mvrel.sh "%F" other' --action5 'mvrel.sh "%F" junk' --action3 'mvrel.sh "%F" doc' --auto-rotate -d --fullscreen -f flst.txt
#--fullscreen 
