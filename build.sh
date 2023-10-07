python addTable.py
python addActivity.py

git config --local user.name actions-user
git config --local user.email "actions@github.com" 
git fetch
git add *
git commit -am "GH Action File removed $(date)" 
git push -f origin main