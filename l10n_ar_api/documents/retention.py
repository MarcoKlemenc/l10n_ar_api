# -*- coding: utf-8 -*-
class Retention:

    @staticmethod
    def get_retention(retention_type):
        """ Devuelve la instancia del tipo de retencion deseado """
        if retention_type == 'profit':
            return RetentionProfit()
        else:
            raise NotImplementedError("El tipo de retencion "+retention_type+" No existe")


class RetentionActivity:

    def __init__(self, minimum_no_aplicable, minimum_tax, percentage):
        """
        :param minimum_no_aplicable: Minimo no imponible de la actividad
        :param minimum_tax: Importe minimo a retener
        :param percentage: Porcentaje de la actividad
        """
        self.minimum_no_aplicable = minimum_no_aplicable
        self.minimum_tax = minimum_tax
        self.percentage = percentage


class RetentionProfit(object):

    def __init__(self):
        self.activity = None

    def calculate_retention_value(self, accumulated, amount_to_pay):
        """
        Devuelve el valor a retener para la actividad de la retencion
        :param accumulated: Acumulado de pagos necesario para deducir el valor
        :param amount_to_pay: Importe a pagar sin impuestos
        :return: Base imponible y Valor que se debe retener
        """
        if not self.activity:
            raise AttributeError("Agregar actividad en la retencion antes de calcular el valor")

        minimum_no_aplicable = self.activity.minimum_no_aplicable
        # El acumulado se debe restar siempre, excepto en el caso que el acumulado sea mayor al minimo no imponible
        # y no se haya retenido por primera vez (porque no sobrepaso el minimo), entonces en ese caso el valor de la
        # retencion es por la anterior + la actual
        if ((accumulated - minimum_no_aplicable) * self.activity.percentage / 100) >= self.activity.minimum_tax:
            accumulated = minimum_no_aplicable

        base = amount_to_pay + accumulated - minimum_no_aplicable
        value = base * (self.activity.percentage / 100)

        if value < self.activity.minimum_tax:
            value = 0

        return base, value
