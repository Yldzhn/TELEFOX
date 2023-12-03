from tinydb import TinyDB, Query

VT = TinyDB("requests.json")
def inputSave (time,msg,lnk) :
    VT.insert({"Timestamp":str(time),"Message":msg,"Link":lnk})
def inputSearch(msg):
    q=Query()
    qMatch = VT.search(q.Message == msg)
    return qMatch