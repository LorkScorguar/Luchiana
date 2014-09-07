Client=Import('Client.py')
Import('Securite.py')
Client.connect()
Client.sendMsg("L","florent;,;lucie")
rep=Client.receiveMsg()

"<html>"
"<head>"
"<title>Luchiana IA</title>"
"<link rel='stylesheet' type='text/css' href='design.css'>"
"<meta name='viewport' content='width=device-width'/>"
"</head>"
"<body>"
"<h1>Luchiana</h1>"
"<form><input type='text' name='texte' /><input type='submit' value='Envoyer' /></form>"
try:
    text=QUERY['texte']
    Client.sendMsg("T",text)
    type,rep=Client.receiveMsg()
    print rep    
except:
    pass

"</body>"
"</html>"
