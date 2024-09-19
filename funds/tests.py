from django.test import TestCase
from .serializers import FundSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Fund, FundType, RiskProfile, Theme
class FundModelTests(TestCase):
    def setUp(self):
        self.fund_type = FundType.objects.create(name='Equity')
        self.risk_profile = RiskProfile.objects.create(name='High')
        self.theme = Theme.objects.create(name='Growth')

    def test_create_fund(self):
        fund = Fund.objects.create(
            name='Growth Fund',
            fund_type=self.fund_type,
            nav='100.00',
            risk_profile=self.risk_profile,
            expected_returns='12%',
            investment_duration='5 years'
        )
        fund.themes.add(self.theme)
        self.assertEqual(fund.name, 'Growth Fund')
        self.assertEqual(fund.nav, '100.00')
        self.assertIn(self.theme, fund.themes.all())


class FundSerializerTests(APITestCase):
    def setUp(self):
        self.fund_type = FundType.objects.create(name='Equity')
        self.risk_profile = RiskProfile.objects.create(name='High')
        self.theme = Theme.objects.create(name='Growth')
        self.fund = Fund.objects.create(
            name='Growth Fund',
            fund_type=self.fund_type,
            nav='100.00',
            risk_profile=self.risk_profile,
            expected_returns='12%',
            investment_duration='5 years'
        )
        self.fund.themes.add(self.theme)
        self.serializer = FundSerializer(instance=self.fund)

    def test_fund_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Growth Fund')
        self.assertEqual(data['nav'], '100.00')
        self.assertEqual(data['themes'][0]['name'], 'Growth')



class FundListViewTests(APITestCase):
    def setUp(self):
        self.fund_type = FundType.objects.create(name='Equity')
        self.risk_profile = RiskProfile.objects.create(name='High')
        self.theme = Theme.objects.create(name='Growth')
        self.fund = Fund.objects.create(
            name='Growth Fund',
            fund_type=self.fund_type,
            nav='100.00',
            risk_profile=self.risk_profile,
            expected_returns='12%',
            investment_duration='5 years'
        )
        self.fund.themes.add(self.theme)
        self.client.force_authenticate(user=self.create_superuser())

    def test_fund_list(self):
        url = '/api/funds/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Growth Fund', [fund['name'] for fund in response.data])

class FundDetailViewTests(APITestCase):
    def setUp(self):
        self.fund_type = FundType.objects.create(name='Equity')
        self.risk_profile = RiskProfile.objects.create(name='High')
        self.theme = Theme.objects.create(name='Growth')
        self.fund = Fund.objects.create(
            name='Growth Fund',
            fund_type=self.fund_type,
            nav='100.00',
            risk_profile=self.risk_profile,
            expected_returns='12%',
            investment_duration='5 years'
        )
        self.fund.themes.add(self.theme)
        self.client.force_authenticate(user=self.create_superuser())

    def test_fund_detail(self):
        url = f'/api/funds/{self.fund.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Growth Fund')

class AvailableFundListViewTests(APITestCase):
    def setUp(self):
        self.fund_type = FundType.objects.create(name='Equity')
        self.risk_profile = RiskProfile.objects.create(name='High')
        self.theme = Theme.objects.create(name='Growth')
        self.fund = Fund.objects.create(
            name='Growth Fund',
            fund_type=self.fund_type,
            nav='100.00',
            risk_profile=self.risk_profile,
            expected_returns='12%',
            investment_duration='5 years'
        )
        self.fund.themes.add(self.theme)
        self.client.force_authenticate(user=self.create_superuser())

    def test_available_fund_list(self):
        url = f'/api/funds/available/{self.fund.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Growth Fund', [fund['name'] for fund in response.data])

class UpdateFundValueViewTests(APITestCase):
    def setUp(self):
        self.fund_type = FundType.objects.create(name='Equity')
        self.risk_profile = RiskProfile.objects.create(name='High')
        self.theme = Theme.objects.create(name='Growth')
        self.fund = Fund.objects.create(
            name='Growth Fund',
            fund_type=self.fund_type,
            nav='100.00',
            risk_profile=self.risk_profile,
            expected_returns='12%',
            investment_duration='5 years'
        )
        self.fund.themes.add(self.theme)
        self.client.force_authenticate(user=self.create_superuser())

    def test_update_fund_value(self):
        url = f'/api/funds/{self.fund.id}/update-value/'
        data = {'current_value': '120.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fund.refresh_from_db()
        self.assertEqual(self.fund.nav, '120.00')



