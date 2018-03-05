# -*- coding: utf-8 -*-

from .. import retention
import pytest


class TestRetention:

    def test_invalid_type(self):
        with pytest.raises(NotImplementedError):
            retention.Retention.get_retention('invalid_retention')


class TestRetentionProfit:

    @pytest.fixture(scope="module")
    def profit_retention(self):
        return retention.Retention.get_retention('profit')

    @pytest.fixture(scope="module")
    def goods_retention(self):
        return retention.RetentionActivity(100000, 90, 2.0)

    def test_calculate_retention_without_activity(self, profit_retention):
        with pytest.raises(AttributeError):
            profit_retention.calculate_retention_value(0, 0)

    """ Tests sin acumulados """
    def test_calculate_retention_without_accumulated_less_than_minimum(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(0, 50000)[1] == 0

    def test_calculate_retention_without_accumulated_less_than_minimum_tax(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(0, 102000)[1] == 0

    def test_calculate_retention_without_accumulated(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(0, 200000)[1] == 2000

    """ Tests con acumulados """
    def test_calculate_retention_with_accumulated_less_than_minimum(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(40000, 50000)[1] == 0

    def test_calculate_retention_with_accumulated_less_than_minimum_tax(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(50000, 70000)[1] == 400

    def test_calculate_retention_with_accumulated_less_than_minimum_tax_no_val(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(50000, 52000)[1] == 0

    def test_calculate_retention_with_accumulated_equal_than_minimum(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(100000, 5000)[1] == 100

    def test_calculate_retention_with_accumulated_higher_than_minimum(self, profit_retention, goods_retention):
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(150000, 5000)[1] == 100

    def test_calculate_retention_with_accumulated_higher_than_minimum_without_retention_before(
            self, profit_retention, goods_retention):
        """
        En el caso que sea la primer retencion del mes, si ya sobrepaso el acumulado, se debe sumar lo no retenido
        """
        profit_retention.activity = goods_retention
        assert profit_retention.calculate_retention_value(102000, 5000)[1] == 140
