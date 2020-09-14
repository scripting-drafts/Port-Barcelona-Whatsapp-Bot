from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep
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

locMSGCA = "Si us plau, comparteixi la seva localització\n"
locMSGES = "Por favor, comparta su localización\n"
locMSGEN = "Please, share your location\n"
locMSGFR = "S'il vous plaît, partager votre emplacement\n"
locMSG = [locMSGCA, locMSGES, locMSGEN, locMSGFR]

waitCA = "Un altre usuari està reportant. Si us plau, envïi el mateix missatge en uns segons.\n"
waitES = "Otro usuario está reportando. Por favor, envíe el mismo mensage en unos segundos.\n"
waitEN = "Another user is reporting. Please, send the same message in a few seconds.\n"
waitFR = "Un autre utilisateur fait un rapport. Veuillez envoyer le même message dans quelques secondes.\n"
wait = [waitCA, waitES, waitEN, waitFR]

endMSGCA = "Gràcies\n"
endMSGES = "Gracias\n"
endMSGEN = "Thank you\n"
endMSGFR = "Mersi\n"
End = [endMSGCA, endMSGES, endMSGEN, endMSGFR]

reString = re.compile('(\d+\.\d+)')
data = {}
user_queue = []
x = 0
y = 0

profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webnotifications.enabled", False)
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

cnt = 10

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
        user_id = driver.find_element_by_css_selector('.DP7CM > ._3ko75._5h6Y_._3Whw5').text.replace('+', '00').replace(' ', '')
        if user_id not in user_queue:
            user_queue.append(user_id)
        user_id = user_queue[0]

        if user_id not in [*data]:
            text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
            text_box.send_keys(msgWelcome)
            data[user_id] = ['init']
            user_queue.remove(user_id)

        else:
            while len(data[user_id]) == 1 and cnt:
                message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]
                text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                try:
                    message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                    bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
                except Exception:
                    bot_message = ''

                if message.text.lower() in vLangs and bot_message == '':
                    data[user_id].append(vLangs[vLangs.index(message.text.lower())])
                    text_box.send_keys(vInstr[vLangs.index(data[user_id][1])])
                    user_queue.remove(user_queue[0])
                    break
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
                        next_user_id = driver.find_element_by_css_selector('.DP7CM > ._3ko75._5h6Y_._3Whw5').text.replace('+', '00').replace(' ', '')
                        if next_user_id != user_id:
                            next_text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                            next_text_box.send_keys(wait[0] + wait[1] + wait[2] + wait[3])
                            if next_user_id not in user_queue:
                                user_queue.append(next_user_id)
                except Exception:
                    pass
                sleep(1)
                cnt -= 1

            user_id = user_queue[0]
            cnt = 10

            while len(data[user_id]) == 2 and cnt:
                message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]
                text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                try:
                    message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                    bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
                except Exception:
                    bot_message = ''

                if message.text.lower() in vIncidents[vLangs.index(data[user_id][1])] and bot_message == '':
                    if message.text.lower() == vIncidents[vLangs.index(data[user_id][1])][7]:
                        inc_type = vIncidents[1][vIncidents[vLangs.index(data[user_id][1])].index(message.text.lower())]
                        text_box.send_keys(locMSG[vLangs.index(data[user_id][1])])
                        data[user_id].append(inc_type)
                        data[user_id].append(inc_type)
                        user_queue.remove(user_queue[0])
                        break
                    else:
                        inc = vIncidents[vLangs.index(data[user_id][1])].index(message.text.lower())
                        inc_type = vIncidents[1][vIncidents[vLangs.index(data[user_id][1])].index(message.text.lower())]
                        text_box.send_keys(vInc[vLangs.index(data[user_id][1])][inc])
                        data[user_id].append(inc_type)
                        user_queue.remove(user_queue[0])
                        break
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
                        next_user_id = driver.find_element_by_css_selector('.DP7CM > ._3ko75._5h6Y_._3Whw5').text.replace('+', '00').replace(' ', '')
                        if next_user_id != user_id:
                            next_text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                            next_text_box.send_keys(wait[vLangs.index(data[user_id][1])])
                            if next_user_id not in user_queue:
                                user_queue.append(next_user_id)
                except Exception:
                    pass
                sleep(1)
                cnt -= 1

            user_id = user_queue[0]
            cnt = 10

            while len(data[user_id]) == 3 and cnt:
                message = driver.find_elements_by_css_selector("._3Whw5.selectable-text.invisible-space.copyable-text")[-1]
                text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                try:
                    message_context = driver.find_elements_by_css_selector(".eRacY")[-1]
                    bot_message = message_context.find_element_by_css_selector("._2oWZe._2HWXK")
                except Exception:
                    bot_message = ''

                if message.text.lower() in vIncDetail[vLangs.index(data[user_id][1])] and bot_message == '':
                    inc_detail = vIncDetail[1][vIncDetail[vLangs.index(data[user_id][1])].index(message.text.lower())]
                    text_box.send_keys(locMSG[vLangs.index(data[user_id][1])])
                    data[user_id].append(inc_detail)
                    user_queue.remove(user_queue[0])
                    break
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
                        next_user_id = driver.find_element_by_css_selector('.DP7CM > ._3ko75._5h6Y_._3Whw5').text.replace('+', '00').replace(' ', '')
                        if next_user_id != user_id:
                            next_text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                            next_text_box.send_keys(wait[vLangs.index(data[user_id][1])])
                            if next_user_id not in user_queue:
                                user_queue.append(next_user_id)
                except Exception:
                    pass
                sleep(1)
                cnt -= 1

            user_id = user_queue[0]
            cnt = 10

            # elif get_pic:
            #     if sth:
            #         get_pic()

            while len(data[user_id]) == 4 and cnt:
                text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                try:
                    locationClass = driver.find_element_by_css_selector('._2geuz')
                    locationURL = locationClass.get_attribute('href')
                    coordinates = re.findall(reString, locationURL)
                    data[user_id][0] = str('{:>016d}'.format(x))
                    data[user_id].append(coordinates[0])
                    data[user_id].append(coordinates[1])
                    data[user_id].append(locationURL)
                    response = requests.post('http://127.0.0.1:8000/input/' + user_id + '/', headers={ 'content-Type': 'application/json'}, data= '{"id":"' + data[user_id][0] + '", "inc_type":"' + data[user_id][2] + '", "inc_detail":"' + data[user_id][3] + '", "lat":"' + data[user_id][4] + '", "lon":"' + data[user_id][5] + '", "url":"' + data[user_id][6] + '", "pic":"https://drive.google.com/file/d/16udAHXF3QNouyb6bXUNgIQYW_bUzhSDp/preview", "is_active":"True"}')
                    if any('400', '422') in response:
                        data[user_id][0].replace(re.compile('.*'), str('{:>016d}'.format(x)))
                        requests.post('http://127.0.0.1:8000/invalid_input/' + user_id + '/', headers={ 'content-Type': 'application/json'}, data='{"id":"' + data[user_id][0] + '", "data":"' + data[user_id] + '"}')
                        x += 1
                    text_box.send_keys(End[vLangs.index(data[user_id][1])])

                    user_box = driver.find_element_by_css_selector('._2kHpK')
                    actionChains = ActionChains(driver)
                    actionChains.context_click(user_box).perform()
                    delete_button = driver.find_elements_by_css_selector('.Ut_N0.n-CQr')[2]
                    delete_button.click()
                    delete = driver.find_element_by_css_selector('.S7_rT.FV2Qy')
                    delete.click()

                    x += 1
                    user_queue.remove(user_queue[0])
                    del data[user_id]
                except Exception:
                    pass
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
                        next_user_id = driver.find_element_by_css_selector('.DP7CM > ._3ko75._5h6Y_._3Whw5').text.replace('+', '00').replace(' ', '')
                        if next_user_id != user_id:
                            next_text_box = driver.find_element_by_css_selector("._2FVVk._2UL8j > ._3FRCZ.copyable-text.selectable-text")
                            next_text_box.send_keys(wait[vLangs.index(data[user_id][1])])
                            if next_user_id not in user_queue:
                                user_queue.append(next_user_id)
                except Exception:
                    pass
                sleep(1)
                cnt -= 1
            cnt = 10
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
# user_id_context: '.DP7CM'
# user_id: "._3ko75._5h6Y_._3Whw5"
