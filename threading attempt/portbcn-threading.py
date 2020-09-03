from selenium import webdriver
import requests
from time import sleep
import re
from threading import Thread

reString = re.compile('(\d+\.\d+)')

msgWelcome = '''Benvingut al Port de Barcelona. Envia *ca* per continuar en català.
Bienvenido al Puerto de Barcelona. Envía *es* para continuar en español.
Welcome to the Port of Barcelona. Send *en* to continue in English.
Bienvenue au Port de Barcelona. Envoyer *fr* pour continuer en français.\n'''

msgInstrCa = '''Si us plau, indiqui el tipus d'incidència que vol reportar:
*abocament*, *objecte*, *animals*, *olors*, *soroll*, *pols*, *fum*, *altres*.\n'''

msgInstrEs = '''Por favor, indique el tipo de incidencia que desea reportar:
*vertido*, *objeto*, *animales*, *olor*, *ruido*, *polvo*, *humo*, *otros*.\n'''

msgInstrEn = '''Please, tell us the kind of incident you would like to report:
*spill*, *object*, *animals*, *smell*, *noise*, *dust*, *smoke*, *others*.\n'''

vLangs = ["ca","es","en","fr"]
vInstr = [msgInstrCa,msgInstrEs]

msgIncAbCa = ["Especifiqui: *mar*, *dàrsena* o *calzada* \n"]
msgIncObCa = ["Especifiqui: *flotant* o *calzada* \n"]
msgIncAnCa = ["Especifiqui: *mar*, *calzada* o *aus mortes* \n"]
msgIncOlCa = ["Especifiqui: *mala olor* o *olor química* \n"]
msgIncSoCa = ["Especifiqui: *port*, *embarcació* \n"]
msgIncPoCa = ["Especifiqui: *port*, *soja* \n"]
msgIncFuCa = ["Especifiqui: *port*, *embarcació* o *altres* \n"]
msgIncAlCa = ["Ok \n"]

msgIncAbEs = ["Especifique: *mar*, *dársena* o *calzada* \n"]
msgIncObEs = ["Especifique: *flotante* o *calzada* \n"]
msgIncAnEs = ["Especifique: *mar*, *calzada* o *aves muertas* \n"]
msgIncOlEs = ["Especifique: *mal olor* u *olor químico* \n"]
msgIncSoEs = ["Especifique: *puerto* o *embarcación* \n"]
msgIncPoEs = ["Especifique: *puerto* o *soja* \n"]
msgIncFuEs = ["Especifique: *puerto*, *embarcación* u *otros* \n"]
msgIncAlEs = ["Ok \n"]

msgIncAbEn = ["Specify: *sea*, *dock* or *road* \n"]
msgIncObEn = ["Specify: *floating* or *road* \n"]
msgIncAnEn = ["Specify: *sea*, *road* or *dead birds* \n"]
msgIncOlEn = ["Specify: *bad smell* or *chemical smell* \n"]
msgIncSoEn = ["Specify: *harbour* or *ship* \n"]
msgIncPoEn = ["Specify: *harbour* or *soy* \n"]
msgIncFuEn = ["Specify: *harbour*, *ship* or *others* \n"]
msgIncAlEn = ["Ok \n"]

msgIncAbFr = ["Spécifier: *mer*, *dock* or *chaussée* \n"]
msgIncObFr = ["Spécifier: *flottant* or *chaussée* \n"]
msgIncAnFr = ["Spécifier: *mer*, *chaussée* or *oiseaux morts* \n"]
msgIncOlFr = ["Spécifier: *mal odeur* or *odeur chimique* \n"]
msgIncSoFr = ["Spécifier: *port* or *bateau* \n"]
msgIncPoFr = ["Spécifier: *port* or *soja* \n"]
msgIncFuFr = ["Spécifier: *port*, *bateau* or *autres* \n"]
msgIncAlFr = ["Ok \n"]

vIncidentsCa = ["abocament","objecte","animals","olors","soroll","pols","fum","altres"]
vIncidentsEs = ["vertido","objeto","animales","olores","ruido","polvo","humo","otros"]
vIncidentsEn = ["spill", "object", "animals", "smell", "noise", "dust", "smoke", "others"]
vIncidentsFr = ["gaspillage", "objet", "animaux", "odeur", "bruit", "poussière", "fumée", "autres"]
vIncidents = [vIncidentsCa,vIncidentsEs, vIncidentsEn, vIncidentsFr]

vIncCa = [msgIncAbCa, msgIncObCa, msgIncAnCa, msgIncOlCa, msgIncSoCa, msgIncPoCa, msgIncFuCa, msgIncAlCa]
vIncEs = [msgIncAbEs, msgIncObEs, msgIncAnEs, msgIncOlEs, msgIncSoEs, msgIncPoEs, msgIncFuEs, msgIncAlEs]
vIncEn = [msgIncAbEn, msgIncObEn, msgIncAnEn, msgIncOlEn, msgIncSoEn, msgIncPoEn, msgIncFuEn, msgIncAlEn]
vIncFr = [msgIncAbFr, msgIncObFr, msgIncAnFr, msgIncOlFr, msgIncSoFr, msgIncPoFr, msgIncFuFr, msgIncAlFr]
vInc = [vIncCa, vIncEs, vIncEn, vIncFr]

vIncDetailCa = ["mar", "dàrsena", "calzada", "flotant", "aus mortes", "mala olor", "olor química", "port", "embarcació", "soja", "altres"]
vIncDetailEs = ["mar", "dársena", "calzada", "flotante", "aves muertas", "mal olor", "olor químico", "puerto", "embarcación", "soja", "otros"]
vIncDetailEn = ["sea", "dock", "road", "floating", "dead birds", "bad smell", "chemical smell", "harbour", "ship", "soy", "others"]
vIncDetailFr = ["mer", "dock", "chaussée", "flottant", "oiseaux morts", "mal odeur", "odeur chimique", "port", "bateau", "soja", "autres"]
vIncDetail = [vIncDetailCa, vIncDetailEs, vIncDetailEn, vIncDetailFr]

locMSGCA = ["Si us plau, comparteixi la seva localització \n"]
locMSGES = ["Por favor, comparta su localización \n"]
locMSGEN = ["Please, share your location \n"]
locMSGFR = ["S'il vous plaît, partager votre emplacement \n"]
locMSG = [locMSGCA, locMSGES, locMSGEN, locMSGFR]

profile = webdriver.FirefoxProfile()
profile.set_preference("dom.push.enabled", False)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.set_preference('privacy.trackingprotection.enabled', True)
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
profile.update_preferences()

driver = webdriver.Firefox(profile)
driver.implicitly_wait(10)
driver.get('https://web.whatsapp.com')

cnt1, cnt2, cnt3, cnt4 = 20, 20, 20, 20

def report(driver):
    while True:
        try:
            id = driver.find_element_by_css_selector("._3ko75._5h6Y_._3Whw5").text.replace('+', '00').replace(' ', '')
            text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
            message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]

            try:
                message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
            except Exception:
                bot_message = ''
                pass

            if 'port' in message.text.lower():
                response = requests.post('http://127.0.0.1:8000/users/' + id + '/', headers={ 'content-Type': 'application/json'}, data = '{"id":"' + id + '"}')
                text_box.send_keys(msgWelcome)
                cnt1 = 0

            while cnt1 != 20:
                message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]
                if message.text.lower() in vLangs:
                    if message.text.lower() == vLangs[0]:
                        lang = 0
                    elif message.text.lower() == vLangs[1]:
                        lang = 1
                    elif message.text.lower() == vLangs[2]:
                        lang = 2
                    elif message.text.lower() == vLangs[3]:
                        lang = 3
                    inc_lang = message.text.lower()
                    text_box.send_keys(vInstr[lang])
                    cnt1 = 20
                    cnt2 = 0
                else:
                    sleep(1)
                    cnt1 +=1

            while cnt2 != 20:
                message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]
                try:
                    message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                    bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
                except Exception:
                    bot_message = ''
                    pass
                if message.text.lower() in vIncidents[lang] and bot_message == '':
                    inc = vIncidents[lang].index(message.text.lower())
                    inc_type = vIncidents[1][vIncidents[lang].index(message.text.lower())]
                    text_box.send_keys(vInc[lang][inc])
                    cnt2 = 20
                    cnt3 = 0
                else:
                    sleep(1)
                    cnt2 +=1

            while cnt3 != 20:
                message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]
                try:
                    message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                    bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
                except Exception:
                    bot_message = ''
                    pass
                if message.text.lower() in vIncDetail[lang] and bot_message == '':
                    inc_detail = vIncDetail[1][vIncDetail[lang].index(message.text.lower())]
                    text_box.send_keys(locMSG[lang])
                    cnt3 = 20
                    cnt4 = 0
                else:
                    sleep(1)
                    cnt3 +=1

            while cnt4 != 20:
                locationClass = driver.find_element_by_css_selector('._2geuz')
                if locationClass:
                    locationURL = locationClass.get_attribute('href')
                    coordinates = re.findall(reString, locationURL)
                    reponse = requests.post('http://127.0.0.1:8000/input/' + id + '/', headers={ 'content-Type': 'application/json'}, data= '{"id":"' + id + '", "inc_type":"' + inc_type + '", "inc_detail":"' + inc_detail + '", "lat":"' + coordinates[0] + '", "lon":"' + coordinates[1] + '"}')
                    cnt4 = 20
                else:
                    sleep(1)
                    cnt4 +=1

        except Exception:
            pass

ids = []

while True:
    unread = driver.find_elements_by_css_selector("._31gEB")
    try:
        if len(unread) > 0:
            ele = unread[-1]
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(ele, 0, -20)
            try:
                action.click()
                action.perform()
                action.click()
                action.perform()
                try:
                    id = driver.find_element_by_css_selector("._3ko75._5h6Y_._3Whw5").text.replace('+', '00').replace(' ', '')
                    if id not in ids:
                        ids.append(id)
                        thread = Thread(target=report(driver))
                        thread.name = str(id) + '_thread'
                        str(id) + '_thread'.start()
                        str(id) + '_thread'.join()
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        pass

# message: "._3Whw5.selectable-text.invisible-space.copyable-text"
# message_context: ".eRacY"
# bot_message: "._2oWZe._2HWXK"
# box_context: "._2FVVk._2UL8j"
# text_box: "._3FRCZ.copyable-text.selectable-text"
# location: "._2geuz"
