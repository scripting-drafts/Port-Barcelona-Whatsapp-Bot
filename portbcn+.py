from selenium import webdriver
import requests
from time import sleep
from sys import argv

script, input_file = argv
target = open(input_file, 'w')

browser = webdriver.Firefox()
browser.get('https://web.whatsapp.com')

bot_users = {}
lang = ''
opcErr = True

msgWelcome = '''Benvingut al Port de Barcelona. Envia *ca* per continuar en català.
Bienvenido al Puerto de Barcelona. Envía *es* para continuar en español.
Welcome to the Port of Barcelona. Send *en* to continue in English.
Bienvenue au Port de Barcelona. Envoyer *fr* pour continuer en français.\n'''

msgInstrCa = '''Mostra les instruccions per reportar incidents enviant *incident*.
Consulta l'estat de la mar enviant *mar*.
Envia *contacte* per descobrir com contactar-nos.
Envia *llei* per consultar la Llei de Privadesa de Dades.
Surt enviant *desactiva*.\n'''

msgIncidentCa = '''Si us plau, indiqui el tipus d'incidència que vol reportar:
*abocament*, *objecte*, *animals*, *olors*, *soroll*, *pols*, *fum*, *altres*.\n'''
msgMarCa = "Aquí podràs comprovar l'estat de la mar.\n"
msgContactCa = '''Si precisa més informació truqui al telèfon d'informació del Port de Barcelona 932986000.
Si prefereix reportar un incident per via telefònica truqui a la Policia Portuaria 932234662.
Pot trobar la resta de números aquí http://www.portdebarcelona.Ca/es/web/autoritat-portuaria/directorio/.\n'''
msgLleyCa = "Les seves dades estan subjectes a la normativa del Port de Barcelona.\n"

msgInstrEs = '''Muestra las instrucciones para reportar incidentes enviando *incidente*.
Consulte el estado del mar enviando *mar*.
Envíe *contacto* para descubrir como contactar con nosotros.
Envíe *ley* para mostrar la Ley de Privacidad de Datos.
Salga enviando *desactiva*.\n'''

msgIncidentEs = '''Por favor, indique el tipo de incidencia que desea reportar:
*vertido*, *objeto*, *animales*, *olor*, *ruido*, *polvo*, *humo*, *otros*.\n'''
msgMarEs = "Aquí podrá ver el estado del mar.\n"
msgContactEs = '''Si precisa más información llame al teléfono de información del Puerto de Barcelona 932986000.
Si prefiere reportar un incidente por vía telefónica llame a la Policia Portuaria 932234662.
Puede encontrar el resto de números aquí http://www.portdebarcelona.Ca/es/web/autoritat-portuaria/directorio/.\n'''
msgLleyEs = "Sus datos estan sujetos a la normativa del Puerto de Barcelona.\n"

vLangs = ["ca","es","en","fr"]
vInstr = [msgInstrCa,msgInstrEs]

vOptionsCa = ["incident", "mar", "contacte", "llei"]
vOptionsEs = ["incidente", "mar", "contacto", "ley"]
vOptions = [vOptionsCa, vOptionsEs]

vActionsCa = [msgIncidentCa,msgMarCa,msgContactCa,msgLleyCa]
vActionsEs = [msgIncidentEs,msgMarEs,msgContactEs,msgLleyEs]
vActions = [vActionsCa, vActionsEs]

msgDesactCa = "A reveure!\n"
msgDesactEs = "Hasta luego!\n"
msgDesactEn = "See you!\n"
msgDesactFr = "Au revoir!\n"

vDesactCa = ["desactiva"]
vDesactEs = ["desactiva"]
vDesactEn = ["deactivate"]
vDesactFr = ["déactiver"]
vDesactiva = [vDesactCa, vDesactEs, vDesactEn, vDesactFr]

vDesactivAct = [msgDesactCa, msgDesactEs,msgDesactEn, msgDesactFr]

msgIncAbCa = ["Especifiqui: *mar*, *dàrsena* o *calzada* \n"]
msgIncObCa = ["Especifiqui: *flotant* o *calzada* \n"]
msgIncAnCa = ["Especifiqui: *mar*, *calzada* o *aus mortes* \n"]
msgIncOlCa = ["Especifiqui: *mal olor* o *olor químic* \n"]
msgIncSoCa = ["Especifiqui: *port*, *embarcació* \n"]
msgIncPoCa = ["Especifiqui: *port*, *soja* \n"]
msgIncFuCa = ["Especifiqui: *port*, *embarcació* o *altres* \n"]
msgIncAlCa = ["Ok \n"]

msgIncAbEs = ["Especifique: *mar*, *dársena* o *calzada* \n"]
msgIncObEs = ["Especifique: *flotante*, *calzada* \n"]
msgIncAnEs = ["Especifique: *mar*, *calzada* o *aves muertas* \n"]
msgIncOlEs = ["Especifique: *mal olor* u *olor químico* \n"]
msgIncSoEs = ["Especifique: *puerto* o *embarcación* \n"]
msgIncPoEs = ["Especifique: *puerto* o *soja* \n"]
msgIncFuEs = ["Especifique: *puerto*, *embarcación* u *otros* \n"]
msgIncAlEs = ["Ok \n"]

vIncidentsCa = ["abocament","objecte","animals","olors","soroll","pols","fum", "altres"]
vIncidentsEs = ["vertido","objeto","animales","olores","ruido","polvo","humo", "otros"]
vIncidents = [vIncidentsCa,vIncidentsEs]

vIncCa = [msgIncAbCa, msgIncObCa, msgIncAnCa, msgIncOlCa, msgIncSoCa, msgIncPoCa, msgIncFuCa, msgIncAlCa]
vIncEs = [msgIncAbEs, msgIncObEs, msgIncAnEs, msgIncOlEs, msgIncSoEs, msgIncPoEs, msgIncFuEs, msgIncAlEs]
vInc = [vIncCa, vIncEs]

vIncAbSubCa = ["mar", "dàrsena", "calzada"]
vIncObSubCa = ["flotant", "calzada"]
vIncAnSubCa = ["mar", "calzada", "aus mortes"]
vIncOlSubCa = ["mal olor", "olor químic"]
vIncSoSubCa = ["port", "embarcació"]
vIncPoSubCa = ["port", "soja"]
vIncFuSubCa = ["port", "embarcació", "altres"]

vIncAbSubEs = ["mar", "dársena", "calzada"]
vIncObSubEs = ["flotante", "calzada"]
vIncAnSubEs = ["mar", "calzada", "aves muertas"]
vIncOlSubEs = ["mal olor", "olor químico"]
vIncSoSubEs = ["puerto", "embarcación"]
vIncPoSubEs = ["puerto", "soja"]
vIncFuSubEs = ["puerto", "embarcación", "otros"]

#msgErrCa = ["No he entès l'ordre. Si us plau, reescrigui-la.\n"]
#msgErrEs = ["No he podido entender la orden. Por favor, reescribala.\n"]
#msgErrEn = ["I didn't understand the command. Please, rewrite it.\n"]
#msgErrFr = ["Dejavu.\n"]

#msgErr = [msgErrCa, msgErrEs, msgErrEn, msgErrFr]

while True:
    unread = browser.find_elements_by_class_name("P6z4j")
    name,message  = '',''
    if len(unread) > 0:
        ele = unread[-1]
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(ele, 0, -20)
        try:
            action.click()
            action.perform()
            action.click()
            action.perform()
        except Exception as e:
            pass
        try:
            name = browser.find_element_by_class_name("KgevS").text
            message = browser.find_elements_by_class_name("_12pGw")[-1]
            if message.text.lower() in vLangs:
                target.write(message.text.lower() + ' ')
                if name in bot_users:
                    if message.text.lower() == vLangs[0]:
                        lang = 0
                    elif message.text.lower() == vLangs[1]:
                        lang = 1
                if name in bot_users:
                    response = vInstr[lang]
                    text_box.send_keys(response)
                opcErr = False
            if 'port' in message.text.lower():
                if name not in bot_users:
                    bot_users[name] = True
                    target.write("\n" + name + ' ')
                    text_box = browser.find_element_by_class_name("_3u328")
                    response = msgWelcome
                    text_box.send_keys(response)
                    print(name)
                opcErr = False
#                else name in bot_users:
#                    text_box = browser.find_element_by_class_name("_2S1VP")         #REVISAR QUE NO ES NECESSITI ALS DEMÉS IF
#                    response = msgWelcome
#                    text_box.send_keys(response)
#                    print(name)
#                    opcErr = False
            if lang != '':
                if message.text.lower() in vOptions[lang]:
                    target.write(message.text.lower() + ' ')
                    opt = vOptions[lang].index(message.text.lower())
                    if name in bot_users:
                        response = vActions[lang][opt]
                        text_box.send_keys(response)
                        opcErr = False
                if message.text.lower() in vIncidents[lang]:            #OPCIONS INCIDENTES
                    target.write(message.text.lower() + ' ')
                    inc = vIncidents[lang].index(message.text.lower())
                    if name in bot_users:
                        target.write(message.text.lower() + ' ')
                        response = vInc[lang][inc]
                        text_box.send_keys(response)
                        opcErr = False
                if message.text.lower() in vDesactiva[lang]:
                    target.write(message.text.lower() + ' ')
                    if name in bot_users:
                        response = vDesactivAct[lang]
                        text_box.send_keys(response)
                        del bot_users[name]
                        opcErr = False
            elif opcErr:
                if name in bot_users:
                    #response = msgErr[lang]
                    text_box.send_keys("error\n")
            opcErr = True
        except Exception as e:
            print(e)
            pass
sleep(2)
