import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Bot:
    def __init__(
        self,
        options=None,
        close_on_exit=False,
    ):
        self.driver = Chrome(options=options)
        self.close_on_exit = close_on_exit

    def connect_ent(self, username, password):
        # Connection à l'ENT
        self.driver.get("https://netocentre.fr/")
        self.driver.implicitly_wait(3)

        lycee_btn = self.driver.find_element_by_css_selector("#brique-lycees > a")
        lycee_btn.click()

        connect_btn = self.driver.find_element_by_css_selector("#portalCASLoginLink")
        connect_btn.click()

        personnel_btn = self.driver.find_element_by_css_selector(
            "#content .panel .pull-center div:nth-child(3) button"
        )
        personnel_btn.click()

        self.driver.find_element_by_css_selector("#user").send_keys(username)
        self.driver.find_element_by_css_selector("#password").send_keys(password + Keys.ENTER)
        self.driver.implicitly_wait(3)

    def close_modal(self):
        try:
            self.driver.find_element_by_css_selector("i[title='Fermer']").click()
        except:
            print("erreur en fermant le modal")

    def open_pronote(self):
        # Ouverture de Pronote et accès à la liste des anciens bulletins
        self.driver.get("https://0450050k.index-education.net/pronote/")

        # Fermer les notifications
        time.sleep(5)
        self.close_modal()

        self.driver.find_element_by_css_selector("#GInterface\\.Instances\\[0\\]\\.Instances\\[1\\]_Combo4").click()
        self.driver.find_element_by_css_selector(
            "#GInterface\\.Instances\\[0\\]_secondMenu > div.secondmenu-container > ul > li:nth-child(3) > div > span"
        ).click()

    def telecharge_bulletins(self, nb_children):
        # Pour chaque élève télécharger tous les bulletins
        for j in range(1, nb_children + 1):
            cell = self.driver.find_element_by_css_selector(f"[id^=pere_IEHtml] >  div:nth-child({j})")
            if cell:
                print(f"Cell {j}")
                try:
                    ActionChains(self.driver).move_to_element(cell).perform()
                    cell.click()
                    time.sleep(1)
                except ElementNotInteractableException:
                    print("cell not interactable")
                except ElementClickInterceptedException:
                    print("click intercepted while changing cell")
                    self.close_modal()

    def download(self, start=1):
        # Cliquer sur chaque élève de la liste
        nb_eleves = int(len(self.driver.find_elements(By.CSS_SELECTOR, "[id^=GInterface]  article")) / 2)
        print(f"{nb_eleves=}")

        for i in range((2 * start - 1), (nb_eleves * 2), 2):
            eleve = self.driver.find_element_by_css_selector(
                f"[id^=GInterface][id$=_Contenu_1] div:nth-child({i}) article"
            )
            if eleve:
                print(f"Eleve {int((i+1)/2)}")
                try:
                    ActionChains(self.driver).move_to_element(eleve).perform()
                    print("moved to eleve")
                    eleve.click()
                    print("clicked on eleve")
                    time.sleep(1)

                    nb_bulletins = len(
                        self.driver.find_elements(By.CSS_SELECTOR, "[id^=pere_IEHtml]  .DAT_DocumentPere")
                    )
                    nb_titres = len(self.driver.find_elements(By.CSS_SELECTOR, "[id^=pere_IEHtml]  .Gras"))
                    print(f"{nb_bulletins=}")
                    self.telecharge_bulletins(nb_bulletins + nb_titres)

                except ElementNotInteractableException:
                    print("eleve not interactable")
                except ElementClickInterceptedException:
                    print("click intercepted while changing eleve")
                    self.close_modal()
