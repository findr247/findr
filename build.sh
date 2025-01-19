# build.sh

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Install dependencies
python3 -m pip install -r requirements.txt

#python3 -m spacy download en_core_web_sm

# Run migrations
#python manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

python manage.py process_tasks