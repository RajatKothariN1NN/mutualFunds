# Mutual Funds Investment Platform

## Project Overview
This application helps clients invest in mutual funds, allowing users to buy/sell funds, manage their portfolios, and get AI-generated portfolio recommendations based on their financial goals, risk profiles, and other parameters. The application is built using Django for the backend, PostgreSQL for data storage, Celery and Redis for task handling and caching, and integrates an AI assistant to help users curate custom portfolios.

### Core Features:
- **Buy and sell mutual funds**: Users can buy and sell from a list of available mutual funds.
- **Portfolio Management**: Users can view their holdings and check their portfolio's performance.
- **AI Portfolio Assistant**: Curates a custom portfolio based on goals, themes, return expectations, duration, and risk profile.
- **High performance**: Optimized for handling big data with Redis caching and asynchronous task processing using Celery.

## Technologies Used
- **Backend**: Django (Django REST Framework)
- **Database**: PostgreSQL
- **Cache & Message Broker**: Redis
- **Asynchronous Task Queue**: Celery
- **AI Assistant**: Integrated using external AI service (e.g., OpenAI)
- **Frontend**: Django templates or React (optional)

## Prerequisites
Before running the project, make sure you have the following installed:
- Python 3.10+
- PostgreSQL
- Redis
- Virtualenv

# High-Level Design (HLD)



Architecture Overview:


Frontend:
i. Simple UI built using Django templates or a lightweight frontend framework like React.
ii. Communicates with the backend via REST APIs.

Backend:
i. Django-based REST API for business logic, using Django REST Framework.
ii. Handles user authentication, fund transactions, and portfolio management.

Redis:
i. Caching frequently accessed data (e.g., fund listings, user portfolios).
ii. Used as a message broker for Celery.

Database:
i. PostgreSQL for persistent storage of user data, transactions, fund details, and portfolio information.

AI Integration:
i. Separate module or service for generating portfolio recommendations.

Asynchronous Processing:
i. Celery for handling background tasks, such as data processing and AI-driven recommendations.


2. Component Diagram:

Frontend:
i. Interfaces with backend APIs for user actions (buy/sell funds, view portfolio).

Backend:
i. Django REST Framework for API endpoints.
ii. Redis for caching.
iii. PostgreSQL for data storage.

AI Module:
i. Integrated for generating recommendations based on user input.

Celery Workers:
i. Processes background tasks asynchronously (e.g., heavy data processing, AI recommendations).


3. Data Flow:

User Requests:
i. Sent from the frontend to the backend via REST APIs.

Backend Processing:
i. Handles requests, interacting with PostgreSQL and Redis as needed.

Data Caching:
i. Frequently accessed data cached in Redis to improve response times.

AI Integration:
i. Backend sends requests to the AI module for portfolio recommendations.

Background Tasks:
i. Managed by Celery to keep the frontend responsive.



### Low-Level Design (LLD)


Database Schema:

User:
id (PK), username, email, password_hash, created_at

Fund:
id (PK), name, fund_type, nav, risk_level, created_at

Transaction:
id (PK), user_id (FK), fund_id (FK), amount, transaction_type, transaction_date

Portfolio:
id (PK), user_id (FK), fund_id (FK), units_held, average_cost, current_value


2. API Endpoints:

Authentication:
i. POST /api/auth/register/: Register a new user.
ii. POST /api/auth/login/: User login and token generation.

Fund Management:
i. GET /api/funds/: List all available funds (cached).
ii. POST /api/funds/buy/: Buy a fund.
iii. POST /api/funds/sell/: Sell a fund.

Portfolio Management:
i. GET /api/portfolio/: View user’s portfolio.
ii. GET /api/portfolio/recommendations/: Get AI-generated portfolio recommendations.

AI Integration:
i. POST /api/ai/recommend/: Generate portfolio recommendations based on user input.


3. Internal Workflows:

Fund Purchase Workflow:
i. User submits a buy request.
ii. Backend verifies authentication and fund availability.
iii. Creates a new Transaction record and updates the user's portfolio.
iv. Caches fund details in Redis.

AI Recommendation Workflow:
i. User requests portfolio recommendations.
ii. Backend triggers a Celery task that calls the AI module.
iii. AI module generates recommendations and returns them.

Data Caching Workflow:
i. Cache frequently accessed data in Redis.
ii. Implement cache invalidation strategies (e.g., on fund updates).


4. Celery Task Queue:

Task Handling:
i. Queue tasks like AI recommendations and large transaction processing.
ii. Redis as the message broker.

Redis Caching Strategy:

i. Caching Fund Listings:
 Store fund listings with a TTL (Time-To-Live) to keep the cache fresh.
ii. Caching Portfolio Data:
Cache portfolio summaries to reduce load on the database.

## Installation and Setup

```bash
1. Clone the Repository
git clone https://github.com/yourusername/mutualFunds.git
cd mutualFunds

2. Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows

3. Install Dependencies
pip install -r requirements.txt

4. Set Up PostgreSQL Database
Create a new PostgreSQL database and update the DATABASES setting in mutualfunds/settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. Run Database Migrations
python manage.py migrate

6. Set Up Redis for Caching and Celery

Make sure Redis is running locally. You can start it using the command:
redis-server

 Update your mutualfunds/settings.py with Redis configurations:
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

7. Start Celery Worker
In a new terminal window, activate the virtual environment and start the Celery worker:
celery -A mutualFunds worker --loglevel=info

8. Start the Django Development Server
python manage.py runserver

9. Set Up AI Integration
If you're using an external AI service (e.g., OpenAI), add your API key to the project. You can create a .env file or include it in your settings.
AI_API_KEY = 'your_openai_api_key'

Usage
Once the project is running:

i Open your browser and navigate to http://127.0.0.1:8000/.
ii You can register, log in, and start exploring features like buying/selling mutual funds, managing portfolios, and using the AI assistant for recommendations.

Testing
You can run tests using Django's built-in testing framework:
python manage.py test

Deployment
To deploy this application, you can containerize it using Docker or deploy it to a cloud platform such as AWS, Heroku, or DigitalOcean.

Example Dockerfile (Optional)
Here's a basic Dockerfile to containerize the application:
# Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

License
This project is licensed under the BSD-3-Clause License. See the LICENSE file for more details.

Contact
For any questions or issues, feel free to contact:

Rajat Kothari: jainrjk9199@gmail.com