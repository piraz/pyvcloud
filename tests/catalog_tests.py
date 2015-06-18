from nose.tools import with_setup
from testconfig import config
from pyvcloud import vcloudair
from pyvcloud.vcloudair import VCA
import time


class TestCatalog:


    def __init__(self):
        self.vca = None
        self.login_to_vcloud()


    def login_to_vcloud(self):
        """Login to vCloud"""
        username = config['vcloud']['username']
        password = config['vcloud']['password']
        service_type = config['vcloud']['service_type']
        host = config['vcloud']['host']
        version = config['vcloud']['version']
        org = config['vcloud']['org']
        service = config['vcloud']['service']
        instance = config['vcloud']['instance']
        self.vca = VCA(host=host, username=username, service_type=service_type, version=version, verify=True, log=True)
        assert self.vca
        if vcloudair.VCA_SERVICE_TYPE_STANDALONE == service_type:
            result = self.vca.login(password=password, org=org)
            assert result
            result = self.vca.login(token=self.vca.token, org=org, org_url=self.vca.vcloud_session.org_url)
            assert result
        elif vcloudair.VCA_SERVICE_TYPE_SUBSCRIPTION == service_type:
            result = self.vca.login(password=password)
            assert result
            result = self.vca.login(token=self.vca.token)
            assert result
            result = self.vca.login_to_org(service, org)
            assert result
        elif vcloudair.VCA_SERVICE_TYPE_ONDEMAND == service_type:
            result = self.vca.login(password=password)
            assert result
            result = self.vca.login_to_instance(password=password, instance=instance, token=None, org_url=None)
            assert result
            result = self.vca.login_to_instance(password=None, instance=instance, token=self.vca.vcloud_session.token, org_url=self.vca.vcloud_session.org_url)
            assert result


    def logout_from_vcloud(self):
        """Logout from vCloud"""
        print 'logout'
        selfl.vca.logout()
        self.vca = None
        assert self.vca is None


    def catalog_exists(self, catalog_name, catalogs):
        for catalog in catalogs:
            if catalog.name == catalog_name:
                return True
        return False


    def test_0001(self):
        """Loggin in to vCloud"""
        assert self.vca.token


    def test_0002(self):
        """Get VDC"""
        vdc_name = config['vcloud']['vdc']
        the_vdc = self.vca.get_vdc(vdc_name)        
        assert the_vdc
        assert the_vdc.get_name() == vdc_name


    def test_0009(self):
        """Validate that catalog doesn't exist"""
        vdc_name = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        custom_catalog = config['vcloud']['custom_catalog']
        the_vdc = self.vca.get_vdc(vdc_name)
        assert the_vdc
        assert the_vdc.get_name() == vdc_name
        catalogs = self.vca.get_catalogs()
        assert not self.catalog_exists(custom_catalog, catalogs)


    def test_0010(self):
        """Create Catalog"""
        vdc_name = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        custom_catalog = config['vcloud']['custom_catalog']
        the_vdc = self.vca.get_vdc(vdc_name)
        assert the_vdc
        assert the_vdc.get_name() == vdc_name
        task = self.vca.create_catalog(custom_catalog, custom_catalog)
        assert task
        result = self.vca.block_until_completed(task)
        assert result
        catalogs = self.vca.get_catalogs()
        assert self.catalog_exists(custom_catalog, catalogs)


    def test_0011(self):
        """Upload media file"""
        vdc_name = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        custom_catalog = config['vcloud']['custom_catalog']
        media_file_name = config['vcloud']['media_file_name']
        media_name = config['vcloud']['media_name']
        the_vdc = self.vca.get_vdc(vdc_name)
        assert the_vdc
        assert the_vdc.get_name() == vdc_name
        result = self.vca.upload_media(custom_catalog, media_name, media_file_name, media_file_name)
        # assert not result
        #assert that media is there

    def test_0099(self):
        """Delete Catalog"""
        vdc_name = config['vcloud']['vdc']
        vapp_name = config['vcloud']['vapp']
        vm_name = config['vcloud']['vm']
        custom_catalog = config['vcloud']['custom_catalog']
        the_vdc = self.vca.get_vdc(vdc_name)
        assert the_vdc
        assert the_vdc.get_name() == vdc_name
        deleted = self.vca.delete_catalog(custom_catalog)
        assert deleted
        the_vdc = self.vca.get_vdc(vdc_name)
        catalogs = self.vca.get_catalogs()
        assert not self.catalog_exists(custom_catalog, catalogs)


