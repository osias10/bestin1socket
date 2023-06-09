import socket
import logging
import xmltodict

_LOGGER = logging.getLogger(__name__)

READ_SIZE=4096

class Bestin():
    def __init__(self, serverIp, serverPort, wallpadIp, wallpadPort):
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.wallpadIp = wallpadIp
        self.wallpadPort = wallpadPort
    
    def requestToWallpad(self, req):
        res = self.request(self.wallpadIp, self.wallpadPort, req)
        return res
    def requestToServer(self, req):
        res = self.request(self.serverIp, self.serverPort, req)
        return res

    def request(self, ip, port, request):
        #_LOGGER.debug('Request --> %s' % request)
        try:
            request = request.encode()
        except:
            pass

        bestinSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bestinSocket.settimeout(5)
        bestinSocket.connect((ip, port))

        bestinSocket.sendall(request)

        response = bestinSocket.recv(READ_SIZE)
        #if len(response) == READ_SIZE:
        #    _LOGGER.critical("Possibly incomplete read!")
        bestinSocket.close()

        try:
            response = response.decode('EUC-KR')
        except:
            pass
        #_LOGGER.debug('Response <-- %s' % response)
        return response

    def XMLRequest(self, reqname, action, dev_num='null', unit_num='null', ctrl_action='null'):
        '''Send an XML request
        This is a subset of the true API ... but it's good enough for now'''

        request = ('<?xml version="1.0" encoding="utf-8"?>'
                   f'<imap ver = "1.0" address ="{self.wallpadIp}" sender = "mobile">'
                   f'	<service type = "request" name = "{reqname}">'
                   '		<target name = "internet" id = "1" msg_no = "11"/>'
                   f'		<action>"{action}"</action>'
                   f'		<params dev_num = "{dev_num}" unit_num = "{unit_num}" ctrl_action = "{ctrl_action}"/>'
                   '	</service>'
                   '</imap>')
        return request

    def ParseXMLResponse(self, response):
        '''Parse an XML response, return an array of resuts on success, or False on failure'''
        # Danger Will Robinson: early returns abound
        if not response:
            return False

        try:
            responsedict = xmltodict.parse(response)
            result = responsedict['imap']['service']['@result']
            if result != 'ok':
                _LOGGER.error("Failed RPC result: %s" % responsedict)
                return False
            else:
                _LOGGER.debug(responsedict['imap']['service']['status_info'])
                return responsedict['imap']['service']['status_info']
        except:
            _LOGGER.critical("exeption in result parsing")
            _LOGGER.critical(response)
            return False

        return False
    def CheckUnitStatus(self, result):
        try:
            unitStatus = result['@unit_status']
            if unitStatus == "on":
                return True
            else :
                return False
        except:
            return False