#Created By MythB # http://github.com/MythB
"""
mystats module for BombSquad version 1.4.143
Provides functionality for dumping player stats to disk between rounds.
To use this, add the following 2 lines to bsGame.ScoreScreenActivity.onBegin():
import mystats
mystats.update(self.scoreSet) 
"""
import threading
import json
import os
import urllib2

def update(score_set):
    #look at score-set entries to tally per-account kills for this round
    account_kills = {}
    account_killed = {}
    account_scores = {}
    account_played = {}
    account_name = {}
    for p_entry in score_set.getValidPlayers().values():
        account_id = p_entry.getPlayer().get_account_id()
        if account_id is not None:
            account_kills.setdefault(account_id, 0)
            account_kills[account_id] += p_entry.accumKillCount
            account_killed.setdefault(account_id, 0)
            account_killed[account_id] += p_entry.accumKilledCount
            account_scores.setdefault(account_id, 0)
            account_scores[account_id] += p_entry.accumScore
            account_played.setdefault(account_id, 0)
            account_played[account_id] += 1
            account_name.setdefault(account_id, p_entry.nameFull)
            account_name[account_id] = p_entry.nameFull
    # Ok; now we've got a dict of account-ids and kills.
    # Now lets kick off a background thread to load existing scores
    # from disk, do display-string lookups for accounts that need them,
    # and write everything back to disk (along with a pretty html version)
    # We use a background thread so our server doesn't hitch while doing this.
    UpdateThread(account_kills,account_killed,account_scores,account_played,account_name).start()
class UpdateThread(threading.Thread):
    def __init__(self, account_kills, account_killed, account_scores, account_played, account_name):
        threading.Thread.__init__(self)
        self._account_kills = account_kills
        self._account_killed = account_killed
        self._account_scores = account_scores
        self._account_played = account_played
        self._account_name = account_name
    def run(self):
        # pull our existing stats from online disk
        try:
            import ftplib
            from ftplib import FTP_TLS
            ftp = FTP_TLS('address')
            ftp.login('user','password')
            ftp.prot_p()
            ftp.cwd('/files/')
            dir = ftp.nlst()
            if 'stats.json' in dir:
               File = open("stats.json", "wb")
               ftp.retrbinary('RETR stats.json', File.write)
               File.close()
               File = open("stats.json", "r")
               stats = json.loads(File.read())
               File.close()
            else:
               stats = {}
               print 'stats file not exist on ftp'
        except Exception:
               print 'error while connecting ftp'
               bs.screenMessage('CONNECTION ERROR',color=(1,0,0))
        else:    
               # now add this batch of kills to our persistant stats
               for account_id, kill_count in self._account_kills.items():
                   # add a new entry for any accounts that dont have one
                   if account_id not in stats:
                       # also lets ask the master-server for their account-display-str.
                       # (we only do this when first creating the entry to save time,
                       # though it may be smart to refresh it periodically since
                       # it may change)
                       url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                       response = json.loads(
                           urllib2.urlopen(urllib2.Request(url)).read())
                       name_html = response['name_html']
                       stats[account_id] = {'kills': 0, 'killed': 0, 'scores': 0, 'played': 0, 'name_html': name_html}
                   # now increment their kills whether they were already there or not
                   stats[account_id]['kills'] += kill_count
               for account_id, killed_count in self._account_killed.items():
                   stats[account_id]['killed'] += killed_count
               for account_id, scores_count in self._account_scores.items():
                   stats[account_id]['scores'] += scores_count
               for account_id, played_count in self._account_played.items():
                   stats[account_id]['played'] += played_count
               for account_id, name in self._account_name.items():
                   stats[account_id]['name_full'] = name
                   
               # dump our stats back to disk
               File = open("stats.json", "w")
               File.write(json.dumps(stats,indent=4))
               File.close()
               File = open("stats.json", "r")
               ftp.storbinary('STOR stats.json', File)
               File.close()
                   
               # lastly, write a pretty html version.
               # our stats url could point at something like this...
               entries = [(a['kills'], a['killed'], a['scores'], a['played'], a['name_html']) for a in stats.values()]
               # this gives us a list of kills/names sorted high-to-low
               entries.sort(reverse=True)
               htmlFile = open("statspage.html", "wb")
               htmlFile.write('<head><meta charset="UTF-8"></head><body>')
               for entry in entries:
                   kills = str(entry[0])
                   killed = str(entry[1])
                   scores = str(entry[2])
                   played = str(entry[3])
                   name = entry[4].encode('utf-8')
                   htmlFile.write(kills + ' kills ' + killed + ' deaths ' + scores + ' score ' + played + ' games : ' + name + '<br>')
               htmlFile.write('</body>')
               htmlFile.close()
               htmlFile = open("statspage.html", "r")
               ftp.storbinary('STOR statspage.html', htmlFile)
               htmlFile.close()
               ftp.quit()
                
                    
               # aaand that's it!  There IS no step 27!
               print 'Added',len(self._account_played),'Log entries.'
        