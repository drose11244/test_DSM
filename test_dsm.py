from selenium import webdriver
from time import sleep
import pytest
import logging
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



class TestExample():
    @pytest.fixture()
    def test_setup(self):
        self.driver = webdriver.Chrome('../chromedriver')
        self.driver.maximize_window()
        url = "https://demo.synology.com/zh-tw/dsm"
        self.driver.get(url)
        btn = self.driver.find_element_by_xpath('//div[@id="proBtn"]//button[@class="common-demo-site-btn btn-prepare"]')
        btn.click()
        try:
        # Get machine status
            WebDriverWait(self.driver, 60,1).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="syno-sysinfo-system-health-summary syno-sysinfo-system-health-content-header-normal"]'))
            )
            self.package_center = self.driver.find_element_by_xpath('//*[@id="sds-desktop-shortcut"]/div/li[1]')
            self.package_center .click()
            yield
        finally:
            self.driver.close()
            self.driver.quit()

    def test_openWidwons(self, test_setup):

        getXpath_windows_btn = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[12]/div[18]/div[2]/div/div/div/div/div[1]"))
        )
        
        btn_id = getXpath_windows_btn.get_attribute('id')

        btn_list = self.getID("ext-gen", btn_id, 4)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, btn_id))
        )

        close_btn = self.driver.find_element_by_id(btn_id)
        restore_btn = self.driver.find_element_by_id(btn_list[1])
        max_btn = self.driver.find_element_by_id(btn_list[2])
        min_btn = self.driver.find_element_by_id(btn_list[3])

        restore_btn.click()
        logging.info('Restore')
        max_btn.click()
        logging.info('Max')
        min_btn.click()
        logging.info('Min')
        self.package_center.click()
        logging.info('open packager')
        close_btn.click()
        logging.info('Close')
        assert True

    def getID(self,prefix ,id, length):
        get_len = len(id) - len(prefix)
        get_id = id[(-get_len):]
        list_id = []
        for i in range(length):
            id = int(get_id) - i
            list_id.append(prefix + str(id))
        return list_id
    @pytest.mark.t1
    def test_openSearch(self, test_setup):

        search_word = "php"
        input_btn = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[12]/div[18]/div[3]/div[1]/div/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td[4]/div[1]/input'))
        )
        input_btn.click()
        sleep(1)
        input_btn.send_keys(search_word)
        input_btn.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="SYNO.SDS.PkgManApp.SearchResult.Panel"]//div[@class="syno-pkglist-container"]'))
        )
        packages_list = self.driver.find_elements_by_xpath('//div[@id="SYNO.SDS.PkgManApp.SearchResult.Panel"]//div[@class="syno-pkglist-container"]')
        len_package = len(packages_list)

        results = []
        for i in range(len_package):
            get_id = packages_list[i].get_attribute('id')
            get_id = self.getID("ext-comp-", get_id, 1)
            xpath = '//div[@id=\"'+get_id[0]+'"]//div[@class="syno-pkglist-card"]//span[@class="syno-pkglist-title"]'
            list_packages_name = self.driver.find_elements_by_xpath(xpath)
            for i in list_packages_name:
                result = i.get_attribute('outerText')
                results.append(result)

        logging.info(results)
        assert results == ["PHP 5.6","PHP 7.0","PHP 7.2","PHP 7.3", "PHP 7.4","phpMyAdmin"]
    

