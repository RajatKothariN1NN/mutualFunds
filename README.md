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

## Features in detail

1. **User Management**
   - User registration and login with JWT authentication.
   - User profile including profile picture, PAN, and phone number verification.

2. **Fund Management**
   - Buy and sell mutual funds.
   - List all available funds with caching using Redis.

3. **Portfolio Management**
   - View and manage user portfolios.
   - Calculate and display total invested amount, profits, and percentage earned for portfolios, folios, and funds.

4. **Folio Management**
   - Create, view, and manage multiple folios within a single portfolio.
   - Associate multiple funds with each folio.

5. **AI Portfolio Recommendations**
   - Generate custom portfolio recommendations based on user goals, themes, expected returns, investment duration, and risk profile.
   - Integration with OpenAI for generating recommendations.

6. **Asynchronous Processing**
   - Background tasks for AI recommendations and heavy data processing using Celery.

## Views

1. **Authentication Views**
   - `RegisterUserView`: Register a new user.
   - `LoginUserView`: User login and token generation.

2. **Fund Management Views**
   - `ListFundsView`: List all available funds.
   - `BuyFundView`: Buy a mutual fund.
   - `SellFundView`: Sell a mutual fund.

3. **Portfolio Management Views**
   - `ViewPortfolioView`: View user’s portfolio.
   - `PortfolioOverviewView`: Get an overview of portfolio investments and performance.

4. **Folio Management Views**
   - `CreateFolioView`: Create a new folio.
   - `ManageFolioView`: Manage existing folios.

5. **AI Integration Views**
   - `GenerateRecommendationsView`: Get AI-generated portfolio recommendations based on user input.

## APIs

1. **Authentication**
   - `POST /api/auth/register/`: Register a new user.
   - `POST /api/auth/login/`: User login and token generation.

2. **Fund Management**
   - `GET /api/funds/`: List all available funds (cached).
   - `POST /api/funds/buy/`: Buy a fund.
   - `POST /api/funds/sell/`: Sell a fund.

3. **Portfolio Management**
   - `GET /api/portfolio/`: View user’s portfolio.
   - `GET /api/portfolio/overview/`: Get portfolio overview (total invested amount, profits, percentage earned).

4. **Folio Management**
   - `POST /api/folio/create/`: Create a new folio.
   - `GET /api/folio/{folio_id}/`: View folio details.
   - `PUT /api/folio/{folio_id}/`: Update folio details.

5. **AI Integration**
   - `POST /api/ai/recommendations/`: Generate portfolio recommendations based on user requirements.

## Database Design

### User
- `id` (PK): Integer
- `username`: String
- `email`: String
- `password_hash`: String
- `created_at`: DateTime
- `profile_pic`: URL
- `PAN`: String
- `phone_number`: String (verified)

### Fund
- `id` (PK): Integer
- `name`: String
- `fund_type`: String
- `nav`: Decimal
- `risk_profile`: String
- `expected_returns`: String
- `investment_duration`: String
- `themes`: Array of Strings
- `created_at`: DateTime

### Transaction
- `id` (PK): Integer
- `user_id` (FK): Integer
- `fund_id` (FK): Integer
- `portfolio_number`: String
- `amount`: Decimal
- `transaction_type`: String
- `transaction_date`: DateTime

### Portfolio
- `id` (PK): Integer
- `user_id` (FK): Integer
- `total_invested`: Decimal
- `total_profit`: Decimal
- `percentage_earned`: Decimal

### Folio
- `id` (PK): Integer
- `portfolio_id` (FK): Integer
- `name`: String
- `total_invested`: Decimal
- `total_profit`: Decimal
- `percentage_earned`: Decimal

### FundFolio (Many-to-Many Relationship)
- `fund_id` (FK): Integer
- `folio_id` (FK): Integer

## Low-Level Design (LLD)

### Models
- **User:** Custom user model with additional fields for profile picture, PAN, and phone verification.
- **Fund:** Includes attributes like type, NAV, risk profile, and themes.
- **Transaction:** Records buy/sell transactions with a reference to the user, fund, and portfolio number.
- **Portfolio:** Tracks total invested amount, profit, and percentage earned.
- **Folio:** Contains information about individual folios, including their performance metrics.

### API Endpoints
- Authentication views for user registration and login.
- CRUD operations for fund management and portfolio management.
- AI integration endpoint for generating recommendations.

### Data Flow
- User interacts with API endpoints.
- Backend processes requests, interacts with the database, and communicates with the AI service for recommendations.
- Data is cached in Redis to optimize performance.

## High-Level Design (HLD)

### Architecture Overview

- **Frontend:**
  - Simple UI using Django templates or React.
  - Communicates with the backend via REST APIs.

- **Backend:**
  - Django-based REST API using Django REST Framework (DRF).
  - Handles user authentication, fund transactions, portfolio management, and AI recommendations.

- **Redis:**
  - Caches frequently accessed data such as fund listings and portfolio summaries.
  - Used as a message broker for Celery tasks.

- **Database:**
  - PostgreSQL for persistent storage of user data, transactions, fund details, portfolios, and folios.

- **AI Integration:**
  - OpenAI for generating portfolio recommendations based on user requirements.

- **Asynchronous Processing:**
  - Celery for handling background tasks such as AI recommendations and heavy data processing.

### Component Diagram

- **Frontend:** Interfaces with backend APIs for user actions (buy/sell funds, view portfolio).
- **Backend:** Django REST Framework for API endpoints, Redis for caching, PostgreSQL for data storage.
- **AI Module:** Integrated for generating recommendations based on user input.
- **Celery Workers:** Processes background tasks asynchronously.

## Architecture

1. **Frontend Layer:**
   - Users interact with a web interface built with Django templates or React.

2. **API Layer:**
   - Exposes RESTful endpoints for interacting with user data, fund transactions, and portfolios.

3. **Business Logic Layer:**
   - Handles core functionality including fund management, portfolio calculations, and recommendation processing.

4. **Data Layer:**
   - **PostgreSQL:** Stores user data, transactions, fund details, portfolios, and folios.
   - **Redis:** Caches data to improve response times and manage Celery tasks.

5. **AI Integration:**
   - **OpenAI:** Used to generate portfolio recommendations based on user input.

6. **Asynchronous Processing:**
   - **Celery:** Manages background tasks to keep the system responsive and handle complex operations.


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