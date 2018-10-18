        ###### bs.game == class activity(object) == onBEgin ######
        bs.gameTimer(100,call=self._checkChat,repeat=True)
    def _checkChat(self):
        temp = bsInternal._getChatMessages()

        if len(temp)>0:
                lastm = temp[len(temp)-1]
                if '/' in lastm:
                    import MythBAdminCommands
                    MythBAdminCommands.cmd(lastm)
                    
        ################OR 23858 bsUI change ###############################
def _handleLocalChatMessage(msg):
    global gPartyWindow
    if '/' in msg:
       import MythBAdminCommands
       MythBAdminCommands.cmd(msg)
    if gPartyWindow is not None and gPartyWindow() is not None:
        gPartyWindow().onChatMessage(msg)
        #####################add is if you use handlelocalchatmessage ############################
        import bsUI
        bs.realTimer(10000,bs.Call(bsUI.onPartyIconActivate,(0,0)))## THATS THE TRICKY PART check ==> 23858 bsUI / _handleLocalChatMessage
        # use only for server !! coz chat windows must always opened
                
                
       #################################################################
                ##dont remember mystats.py##
        
        
        ############bs.teamgame top####################################
gDefaultTeamColors = ((0.0, 1.0, 0.0), (1.0, 0.0, 0.0))

gDefaultTeamNames = ("LIGHT SIDE", "DARK SIDE")

gTeamSeriesLength = 24

gFFASeriesLength = 24

Team Game Max Players = 999 # find

    #######################################################################
    
    ################for server linux #####################################
chmod 777 bs_headless
chmod 777 bombsquad_server
chmod 777 config.py 

or fuck them all "sudo chmod -R 777 bsserver izinleri ver"

sudo timedatectl set-timezone Europe/Istanbul

sudo apt-get install python2.7 libsdl2-2.0
tmux
./bombsquad_server or nohup ./bombsquad_server & #<--- my choise

###########################################################################