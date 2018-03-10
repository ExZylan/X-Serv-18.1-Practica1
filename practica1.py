#!/usr/bin/python3

import webapp

contents = {
	'0': 'http://www.google.es'
}
contents2 = {
	'http://www.google.es': '/0'
}

formulario = """
	<form action="/" method="POST">
	Url:<br>
	<input type="text" name="enlace" value=""><br>
	<input type="submit" value="Enviar">
</form>
"""

def dictionary(contents):
	enlaces = "<br>"
	for x in contents:
		enlaces = enlaces + "<a href=" + contents[x]+ ">" + str(x) + "</a>" + ": " + "<a href= " + contents[x] + ">"+ contents[x] + "</a><br>"
	return enlaces 

def search(contents, exist, url):
	for x in contents:
		if contents[x] == url:
			exist = True
	return exist

def read(contents):
	n = len(contents)
	f = open("URLS.txt")
	for linea in f.read().splitlines():
		print(linea)
		contents[str(n)] = linea
		contents2[linea] = str(n)
		n = n + 1
	f.close()

def write(contents, url):
	f = open ("URLS.txt", "a")
	f.write(url)
	f.close()

class contentApp(webapp.webApp):

	def __init__(self, hostname, port):
		read(contents)
		super().__init__(hostname, port)

	def parse(self, request):
		return(request.split()[0], request.split()[1], request) #hacemos split una vez y me quedo con el primero

	def process(self, parsedRequest): # parsedRequest es una tupla (metodo, recurso) de la peticion
		exist = False
		vacio = False

		method, recurso, peticion = parsedRequest
		recurso = recurso.split("/")[1]			
		if method == "POST":
			url = peticion.split('\r\n\r\n', 1)[1].split('=')[1]
			if url != "":
				if url.startswith("http"):
					url = url.split("F")[2]
					exist = search(contents, exist, ("http://" + url))
					if not exist:
						contents[str(len(contents))] = ("http://" + url)
						contents2[("http://" + url)] = str(len(contents))
						write(contents, ("http://" + url + "\n"))
				else:
					exist = search(contents, exist, ("http://" + url))
					if not exist:
						contents[str(len(contents))] = ("http://" + url)
						contents2[("http://" + url)] = str(len(contents))
						write(contents, ("http://" + url + "\n"))
			else:
				vacio = True
		
		if not vacio:
			print(contents)
			if not exist:
				if recurso != "" and recurso != "favicon.ico":
					print(recurso)
					if int(recurso) < len(contents):
						return("302 HTTP REDIRECT", "<html><head><meta http-equiv=Refresh content=0;url=" +contents[recurso]+"></head></html>")
					else:
						return ("404 NOT FOUND", "<html>Recurso no disponible!!!</html>")
				else:
					return("200 OK", "<html>Introduce URLS!<br>" + formulario + dictionary(contents) + "</html>")
			else:
				return ("200 OK", "<html><a href=" + ("http://" + url)+ ">" + str(contents2[("http://" + url)]) + "</a>" + ": " + "<a href= " + ("http://" + url) + ">"+ ("http://" + url) + "</a></html>")
		else:
			return ("404 NOT FOUND", "<html>Error al ingrersar la URL!!!</html>")


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)