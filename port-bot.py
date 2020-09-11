from selenium import webdriver
from selenium.webdriver import ActionChains
import requests
import re

msgWelcome = '''Benvingut al Port de Barcelona. Envia *ca* per continuar en català.
Bienvenido al Puerto de Barcelona. Envía *es* para continuar en español.
Welcome to the Port of Barcelona. Send *en* to continue in English.
Bienvenue au Port de Barcelona. Envoyer *fr* pour continuer en français.\n'''

msgInstrCa = '''Si us plau, indiqui el tipus d'incidència que vol reportar:
*abocament*, *objecte*, *animals*, *olors*, *soroll*, *pols*, *fum*, *altres*\n'''

msgInstrEs = '''Por favor, indique el tipo de incidencia que desea reportar:
*vertido*, *objeto*, *animales*, *olores*, *ruido*, *polvo*, *humo*, *otros*\n'''

msgInstrEn = '''Please, tell us the kind of incident you would like to report:
*spill*, *object*, *animals*, *smell*, *noise*, *dust*, *smoke*, *others*\n'''

msgInstrFr = '''Veuillez nous indiquer le type d'incident que vous souhaitez signaler:
*gaspillage*, *objet*, *animaux*, *odeur*, *bruit*, *poussière*, *fumée*, *autres*\n'''

vLangs = ["ca","es","en","fr"]
vInstr = [msgInstrCa,msgInstrEs,msgInstrEn,msgInstrFr]

msgIncAbCa = ["Especifiqui: *mar*, *dàrsena* o *calzada*\n"]
msgIncObCa = ["Especifiqui: *flotant* o *calzada*\n"]
msgIncAnCa = ["Especifiqui: *mar*, *calzada* o *aus mortes*\n"]
msgIncOlCa = ["Especifiqui: *mala olor* o *olor química*\n"]
msgIncSoCa = ["Especifiqui: *port*, *embarcació*\n"]
msgIncPoCa = ["Especifiqui: *port*, *soja*\n"]
msgIncFuCa = ["Especifiqui: *port*, *embarcació* o *altres*\n"]

msgIncAbEs = ["Especifique: *mar*, *dársena* o *calzada*\n"]
msgIncObEs = ["Especifique: *flotante* o *calzada*\n"]
msgIncAnEs = ["Especifique: *mar*, *calzada* o *aves muertas*\n"]
msgIncOlEs = ["Especifique: *mal olor* u *olor químico*\n"]
msgIncSoEs = ["Especifique: *puerto* o *embarcación*\n"]
msgIncPoEs = ["Especifique: *puerto* o *soja*\n"]
msgIncFuEs = ["Especifique: *puerto*, *embarcación* u *otros*\n"]

msgIncAbEn = ["Specify: *sea*, *dock* or *road*\n"]
msgIncObEn = ["Specify: *floating* or *road*\n"]
msgIncAnEn = ["Specify: *sea*, *road* or *dead birds*\n"]
msgIncOlEn = ["Specify: *bad smell* or *chemical smell*\n"]
msgIncSoEn = ["Specify: *harbour* or *ship*\n"]
msgIncPoEn = ["Specify: *harbour* or *soy*\n"]
msgIncFuEn = ["Specify: *harbour*, *ship* or *others*\n"]

msgIncAbFr = ["Spécifier: *mer*, *dock* or *chaussée*\n"]
msgIncObFr = ["Spécifier: *flottant* or *chaussée*\n"]
msgIncAnFr = ["Spécifier: *mer*, *chaussée* or *oiseaux morts*\n"]
msgIncOlFr = ["Spécifier: *mal odeur* or *odeur chimique*\n"]
msgIncSoFr = ["Spécifier: *port* or *bateau*\n"]
msgIncPoFr = ["Spécifier: *port* or *soja*\n"]
msgIncFuFr = ["Spécifier: *port*, *bateau* or *autres*\n"]

vIncidentsCa = ["abocament","objecte","animals","olors","soroll","pols","fum","altres"]
vIncidentsEs = ["vertido","objeto","animales","olores","ruido","polvo","humo","otros"]
vIncidentsEn = ["spill", "object", "animals", "smell", "noise", "dust", "smoke", "others"]
vIncidentsFr = ["gaspillage", "objet", "animaux", "odeur", "bruit", "poussière", "fumée", "autres"]
vIncidents = [vIncidentsCa,vIncidentsEs, vIncidentsEn, vIncidentsFr]

vIncCa = [msgIncAbCa, msgIncObCa, msgIncAnCa, msgIncOlCa, msgIncSoCa, msgIncPoCa, msgIncFuCa]
vIncEs = [msgIncAbEs, msgIncObEs, msgIncAnEs, msgIncOlEs, msgIncSoEs, msgIncPoEs, msgIncFuEs]
vIncEn = [msgIncAbEn, msgIncObEn, msgIncAnEn, msgIncOlEn, msgIncSoEn, msgIncPoEn, msgIncFuEn]
vIncFr = [msgIncAbFr, msgIncObFr, msgIncAnFr, msgIncOlFr, msgIncSoFr, msgIncPoFr, msgIncFuFr]
vInc = [vIncCa, vIncEs, vIncEn, vIncFr]

vIncDetailCa = ["mar", "dàrsena", "calzada", "flotant", "aus mortes", "mala olor", "olor química", "port", "embarcació", "soja", "altres"]
vIncDetailEs = ["mar", "dársena", "calzada", "flotante", "aves muertas", "mal olor", "olor químico", "puerto", "embarcación", "soja", "otros"]
vIncDetailEn = ["sea", "dock", "road", "floating", "dead birds", "bad smell", "chemical smell", "harbour", "ship", "soy", "others"]
vIncDetailFr = ["mer", "dock", "chaussée", "flottant", "oiseaux morts", "mal odeur", "odeur chimique", "port", "bateau", "soja", "autres"]
vIncDetail = [vIncDetailCa, vIncDetailEs, vIncDetailEn, vIncDetailFr]

locMSGCA = ["Si us plau, comparteixi la seva localització\n"]
locMSGES = ["Por favor, comparta su localización\n"]
locMSGEN = ["Please, share your location\n"]
locMSGFR = ["S'il vous plaît, partager votre emplacement\n"]
locMSG = [locMSGCA, locMSGES, locMSGEN, locMSGFR]

endMSGCA = "Gràcies\n"
endMSGES = "Gracias\n"
endMSGEN = "Thank you\n"
endMSGFR = "Mersi\n"

End = [endMSGCA, endMSGES, endMSGEN, endMSGFR]

reString = re.compile('(\d+\.\d+)')
data = {}
langs = {}
#ids = list(range(1, 1000000))
x = 0

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

while True:
    try:
        unread = driver.find_elements_by_css_selector("._31gEB")
        if len(unread) > 0:
            element = unread[-1]
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(element, 0, -20)
            action.click()
            action.perform()
            action.click()
            action.perform()
    except Exception:
        pass
    try:
        id = driver.find_element_by_css_selector('.DP7CM > ._3ko75._5h6Y_._3Whw5').text.replace('+', '00').replace(' ', '')
        text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")

        if id not in [*data]:
            text_box.send_keys(msgWelcome)
            data[id] = [str('{:>016d}'.format(x))]
            x += 1

        else:
            message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]

            try:
                message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
            except Exception:
                bot_message = ''

            if len(data[id]) == 1:
                if message.text.lower() in vLangs and bot_message == '':
                    langs[id] = vLangs.index(message.text.lower())
                    text_box.send_keys(vInstr[langs[id]])
                    data[id].append(vLangs[langs[id]])

            elif len(data[id]) == 2:
                if message.text.lower() in vIncidents[langs[id]] and bot_message == '':
                    if message.text.lower() == vIncidents[langs[id]][7]:
                        inc = vIncidents[langs[id]].index(message.text.lower())
                        inc_type = vIncidents[1][vIncidents[langs[id]].index(message.text.lower())]
                        text_box.send_keys(locMSG[langs[id]])
                        data[id].append(inc_type)
                        data[id].append(inc_type)
                    else:
                        inc = vIncidents[langs[id]].index(message.text.lower())
                        inc_type = vIncidents[1][vIncidents[langs[id]].index(message.text.lower())]
                        text_box.send_keys(vInc[langs[id]][inc])
                        data[id].append(inc_type)

            elif len(data[id]) == 3:
                if message.text.lower() in vIncDetail[langs[id]] and bot_message == '':
                    inc_detail = vIncDetail[1][vIncDetail[langs[id]].index(message.text.lower())]
                    text_box.send_keys(locMSG[langs[id]])
                    data[id].append(inc_detail)

            elif len(data[id]) == 4:
                try:
                    locationClass = driver.find_element_by_css_selector('._2geuz')
                    locationURL = locationClass.get_attribute('href')
                    coordinates = re.findall(reString, locationURL)
                    data[id].append(coordinates[0])
                    data[id].append(coordinates[1])
                    data[id].append(locationURL)
                    response = requests.post('http://127.0.0.1:8000/input/' + id + '/', headers={ 'content-Type': 'application/json'}, data= '{"id":"' + data[id][0] + '", "inc_type":"' + data[id][2] + '", "inc_detail":"' + data[id][3] + '", "lat":"' + data[id][4] + '", "lon":"' + data[id][5] + '", "url":"' + data[id][6] + '", "pic":"https://drive.google.com/file/d/16udAHXF3QNouyb6bXUNgIQYW_bUzhSDp/preview"}')
                    text_box.send_keys(End[langs[id]])

                    user_box = driver.find_element_by_css_selector('._2kHpK')
                    actionChains = ActionChains(driver)
                    actionChains.context_click(user_box).perform()
                    delete_button = driver.find_elements_by_css_selector('.Ut_N0.n-CQr')[2]
                    delete_button.click()
                    delete = driver.find_element_by_css_selector('.S7_rT.FV2Qy')
                    delete.click()

                    del data[id]
                    del langs[id]

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
# user_box: '._2kHpK'
# delete_button: '.Ut_N0.n-CQr'
# delete: '.S7_rT.FV2Qy'
# id_context: '.DP7CM'
# id: "._3ko75._5h6Y_._3Whw5"
