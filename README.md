# Whatsapp_Integration - Django

Django Rest Frame Work backend

## Tech Stack

**Server:** Python 3.10.x, uv, Django, Django Rest Framework


### Prerequisites
* Python 3.10.x
* [UV](https://pypi.org/project/uv/) as dependency manager
* Default sqlite database is used
* Twilio account for sending and receving whatsapp messages

## Local Installation

1. Go to the folder where you want to install the application
```bash
cd <project_dir>
```
2. Clone the project
```bash
  git clone <giturl>
```
3. Set the Twilio account for getting TWILIO_ACCOUNT_SID and AUTH_TOKEN
```bash
  https://www.twilio.com/docs
```
4. Add the Twilio credentials to docker-compose.yml file
```bash
  TWILIO_ACCOUNT_SID=<twilio account SID>
  TWILIO_AUTH_TOKEN=<Auth token>
```
8. Create a super user
```bash
   uv run python manage.py createsuperuser
```
9. Run the docker
```bash
  docker-compose up
```
10. Endpoint
http://127.0.0.1:8000/

## Redis and Celery Setup

1. To start redis locally
```bash
   redis-server
```
2. To run the celery worker locally
```bash
   celery -A whatsapp_integration.celery.app worker --loglevel=info
```

## Webhook Setup
1. Add the webhook url in settings in twilio account. For local setup, use ngrok
```bash
   https://<your_ngrok_subdomain>.ngrok.io/webhook/  
```





