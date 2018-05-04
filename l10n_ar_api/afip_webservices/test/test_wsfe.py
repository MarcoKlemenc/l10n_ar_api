# -*- coding: utf-8 -*-
import pytest
import sys, os
from datetime import date
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
import wsfe
from l10n_ar_api import documents
import wsaa
import files
import copy

class TestWsfe:

    @pytest.fixture
    def invoice_test(self):
        
        invoice_test = wsfe.invoice.ElectronicInvoice(001)
        invoice_test.concept = 01
        
        invoice_test.document_date = date.today()
        invoice_test.service_from = date.today() - relativedelta(days=15)
        invoice_test.service_to = date.today() + relativedelta(days=15)
        invoice_test.payment_due_date = date.today() + relativedelta(days=30)
        
        invoice_test.taxed_amount = 10000.0
        invoice_test.untaxed_amount = 150.0
        invoice_test.exempt_amount = 200.0
 
        invoice_test.customer_document_type = "80"
        invoice_test.customer_document_number = "30709653543"
               
        invoice_test.mon_id = "PES"
        invoice_test.mon_cotiz = 1
            
        return invoice_test   
    
    @pytest.fixture(scope="module")
    def wsfe_test(self):
        #Logeo
        token = wsaa.tokens.AccessRequerimentToken('wsfe')
        signed_tra = token.sign_tra(files.private_key, files.certificate) 
        wsaa_test = wsaa.wsaa.Wsaa()
        login_fault = wsaa_test.login(signed_tra)

        #Token
        token = wsaa.tokens.AccessToken()
        token.create_token_from_login(login_fault)
        return wsfe.wsfe.Wsfe(token, '20311641531')

    def test_check_webservice_status(self, wsfe_test):
        wsfe_test.check_webservice_status()

    def test_get_last_number(self, wsfe_test):
        wsfe_test.get_last_number(0001, '001')

    def test_get_last_number_invalid_document(self, wsfe_test):
        with pytest.raises(Exception):
            wsfe_test.get_last_number(0001, '092')

    def test_invoice_no_taxes(self, wsfe_test, invoice_test):
        response = wsfe_test.get_cae([invoice_test], 0001)[0]
        assert response.FeCabResp.Resultado == 'R'

    def test_invoice_invalid_tax(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(8, 2100, 10000))
        response = wsfe_test.get_cae([invoice_test], 0001)[0]
        assert response.FeCabResp.Resultado == 'R'

    def test_invoice(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(5, 2100.0, 10000.0))
        response = wsfe_test.get_cae([invoice_test], 0001)[0]
        assert response.FeCabResp.Resultado == 'A'

    def test_invoice_invalid_tribute(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(5, 2100, 10000))
        invoice_test.add_tribute(documents.tax.Tribute(76, 500, 1000, 5))
        response = wsfe_test.get_cae([invoice_test], 0001)[0]
        assert response.FeCabResp.Resultado == 'R'

    def test_invoice_tribute(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(5, 2100, 10000))
        invoice_test.add_tribute(documents.tax.Tribute(2, 500, 1000, 5))
        response = wsfe_test.get_cae([invoice_test], 0001)[0]
        assert response.FeCabResp.Resultado == 'A'

    def test_multiple_invoices_different_code(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(5, 2100, 10000))
        invoice_test.add_tribute(documents.tax.Tribute(2, 500, 1000, 5))
        new_invoice = copy.copy(invoice_test)
        new_invoice.document_code = 2
        with pytest.raises(AttributeError):
            wsfe_test.get_cae([invoice_test, new_invoice], 0001)

    def test_multiple_invoices_partial(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(4, 1050, 10000))
        invoice_test.add_tribute(documents.tax.Tribute(2, 500, 1000, 5))
        new_invoice = copy.copy(invoice_test)
        new_invoice.customer_document_type="312"
        response = wsfe_test.get_cae([invoice_test, new_invoice], 0001)[0]
        assert response.FeCabResp.Resultado == 'P'

    def test_multiple_invoices(self, wsfe_test, invoice_test):
        invoice_test.add_iva(documents.tax.Iva(5, 2100, 10000))
        invoice_test.add_tribute(documents.tax.Tribute(2, 500, 1000, 5))
        new_invoice = copy.copy(invoice_test)
        response = wsfe_test.get_cae([invoice_test, new_invoice], 0001)[0]
        assert response.FeCabResp.Resultado == 'A'
