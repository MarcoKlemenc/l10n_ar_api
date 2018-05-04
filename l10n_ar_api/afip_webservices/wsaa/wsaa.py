from zeep import Client
from l10n_ar_api.afip_webservices import config


class Wsaa(object):

    def __init__(self, homologation=True, url=None):
        
        if not url:
            self.url = config.authorization_urls.get('homologation') if homologation\
                else config.authorization_urls.get('production')
        else:
            self.url = url

    def login(self, tra):
        """
        :param tra: TRA que se usara para el logeo
        :return: XML con el login autorizado
        """
        
        try:
            login_fault = Client(self.url).service.loginCms(tra)
        except Exception:
            raise Exception("Error al autenticarse")
        
        return login_fault
