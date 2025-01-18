# build.sh

# Update package lists and install SQLite development libraries
apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Install dependencies
python3 -m pip install -r requirements.txt

# Run migrations
#python manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput