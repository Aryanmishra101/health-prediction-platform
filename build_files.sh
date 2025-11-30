pip install -r requirements.txt
cd healthpredict && python3.9 manage.py migrate --noinput
python3.9 healthpredict/manage.py collectstatic --noinput
