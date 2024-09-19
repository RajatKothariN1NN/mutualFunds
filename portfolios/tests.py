from django.test import TestCase
from .models import Portfolio, Folio, FundFolio
from .serializers import PortfolioSerializer, FolioSerializer, FundFolioSerializer
from funds.models import Fund
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Portfolio, Folio, FundFolio
from funds.models import Fund

User = get_user_model()

class PortfolioModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)

    def test_total_invested_amount(self):
        folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')
        FundFolio.objects.create(folio=folio, fund=fund, units_held=10, average_cost=90)
        self.assertEqual(self.portfolio.total_invested_amount(), 900)

    def test_total_current_value(self):
        folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')
        FundFolio.objects.create(folio=folio, fund=fund, units_held=10, average_cost=90)
        self.assertEqual(self.portfolio.total_current_value(), 1000)

    def test_total_performance(self):
        folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')
        FundFolio.objects.create(folio=folio, fund=fund, units_held=10, average_cost=90)
        self.assertEqual(self.portfolio.total_performance(), 11.11)  # (1000 - 900) / 900 * 100

class FolioModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        self.fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')

    def test_total_invested_amount(self):
        FundFolio.objects.create(folio=self.folio, fund=self.fund, units_held=10, average_cost=90)
        self.assertEqual(self.folio.total_invested_amount(), 900)

    def test_total_current_value(self):
        FundFolio.objects.create(folio=self.folio, fund=self.fund, units_held=10, average_cost=90)
        self.assertEqual(self.folio.total_current_value(), 1000)

    def test_performance(self):
        FundFolio.objects.create(folio=self.folio, fund=self.fund, units_held=10, average_cost=90)
        self.assertEqual(self.folio.performance(), 11.11)  # (1000 - 900) / 900 * 100

class FundFolioModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        self.fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')
        self.fund_folio = FundFolio.objects.create(folio=self.folio, fund=self.fund, units_held=10, average_cost=90)

    def test_total_invested_amount(self):
        self.assertEqual(self.fund_folio.total_invested_amount(), 900)

    def test_current_value(self):
        self.assertEqual(self.fund_folio.current_value(), 1000)

    def test_performance(self):
        self.assertEqual(self.fund_folio.performance(), 11.11)  # (1000 - 900) / 900 * 100


class PortfolioSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.serializer = PortfolioSerializer(instance=self.portfolio)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'folios', 'created_at', 'total_invested_amount', 'total_current_value', 'performance']))

class FolioSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        self.serializer = FolioSerializer(instance=self.folio)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'created_at', 'fundfolios', 'total_invested_amount', 'total_current_value', 'performance']))

class FundFolioSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        self.fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')
        self.fund_folio = FundFolio.objects.create(folio=self.folio, fund=self.fund, units_held=10, average_cost=90)
        self.serializer = FundFolioSerializer(instance=self.fund_folio)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'folio', 'fund', 'units_held', 'average_cost', 'current_value', 'performance']))


class PortfolioAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client.login(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)

    def test_get_portfolio(self):
        response = self.client.get(f'/portfolios/portfolio/{self.portfolio.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class FolioAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client.login(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')

    def test_list_folios(self):
        response = self.client.get('/portfolios/folios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Folio 1', str(response.data))

    def test_create_folio(self):
        response = self.client.post('/portfolios/folios/create/', {'name': 'Folio 2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Folio 2')

class FundFolioAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client.login(email='test@example.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user)
        self.folio = Folio.objects.create(portfolio=self.portfolio, name='Folio 1')
        self.fund = Fund.objects.create(name='Fund 1', nav=100, fund_type=None, risk_profile=None, expected_returns='5%', investment_duration='1 year')
        self.fund_folio = FundFolio.objects.create(folio=self.folio, fund=self.fund, units_held=10, average_cost=90)

    def test_list_fundfolios(self):
        response = self.client.get('/portfolios/fundfolios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Fund 1', str(response.data))

    def test_create_fundfolio(self):
        response = self.client.post('/portfolios/fundfolios/create/', {'folio': self.folio.id, 'fund': self.fund.id, 'units_held': 10, 'average_cost': 90})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['units_held'], 10)