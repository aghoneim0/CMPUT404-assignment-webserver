#!/usr/bin/python
import SocketServer,os
from os import curdir, sep
    
class MyWebServer(SocketServer.BaseRequestHandler):

    # Create the Header and attach it to the Data 
    def create_header(self,data,head_type):
            if head_type == 404:
                    header='HTTP/1.1 404 Not Found\r\n'
                    head_type='html'
            else:
                    header='HTTP/1.1 200 OK\r\n'
  
            header+='Server: MyWebServer\r\n'
            header+='Connection: close\r\n'
            header+='Content-Type: text/%s\r\n\r\n' % head_type
            header+=data
            data=header

            return data

    # list a Folder contents
    def make_index2 (self,folder_name):
        html ='<html><head>List of Folders and Files</head><body><br>'
        path= os.path.dirname(os.path.realpath("server.py"))
        final=folder_name.split(path+'//www/')
        final='/'.join(final)
        final = final.split('/')
        num=len(final)-1
        final = final[num]
        for f in os.listdir(folder_name):
                
                html+='<a href="%s">%s</a><br>' % ('./'+final+'/'+f,f)
                        
        html+='<br></body></html>'

        return html
        
    #Reads the file and send it back 
    def get_file (self,requ):
            print 'Get File Data : '+requ
            if "www" not in requ :
                                requ= "/www"+requ
            try:
		    f = open(curdir+ requ)
		    file_data=f.read()
		    f.close

            except IOError as e : 
                     data='<html><head><h2>Error 404! Page not Found</h2></head>'
                     error=self.create_header(data,404)
                     self.request.sendall(error)
                     print 'error in file openin'
            return file_data

    #Over ride the current handle function in  BaseRequestHandler   
    def handle(self):
            
        self.data =  self.request.recv(1024).strip()

        self.data=self.data.split('GET ')
	self.data=self.data[1].split('HTTP/1.1')
   	# To get the Requested file from the request data
        requ=self.data[0]
	requ=requ.replace(' ','')
               

        if ".html" in requ:
                print "In Html"
                data = self.get_file(requ)
                data = self.create_header(data,'html')
                self.request.sendall(data)
                return

        if ".css" in requ:
                 print "In Css"
		 temp_css=requ
		 Flag=0
		 temp_css=temp_css.split('/')
		 # This cheap fix is done because of the trailing slash in the URL
		 # Basically rewriting  any path that 1) doesn't end with /  2) doesn't contain .html or .css 3) Ends with /
		 if len(temp_css) == 2: # The Length of the Array will be 2 if the Requested URL is /deep and it will be greater if /deep/
			Flag=1
		 if Flag == 1: # Make sure the Array is 2 and  nothing else so it won't screw up anything else 
			 if 'Referer' in self.data[1]:# To get the URL using the referer
				ref=self.data[1].split('Referer: http://127.0.0.1:8080') # Get the  URL from the Referer for example if its  http://127.0.0.1:8080/deep
				ref=ref[1].split("\r\nConnection")
				ref=ref[0].strip('/') # this will return deep
				if '.' not in ref:
					ref='/'+ref+'/' # add back slashes to deep : /deep/
					requ=ref+requ  # add the folde name to the requested css file so /deep/*.css
		 #End of the cheap fix 
                 data = self.get_file(requ)
                 data = self.create_header(data,'css')
                 self.request.sendall(data)
                 return
                         
        if  "/../"  in requ:
                data='<html><head><h2>Error 404! You dont have Permission.</h2></head>'
                error=self.create_header(data,404)
                self.request.sendall(error)
                return
                
        if  "." not in requ:

                if 'www' not in requ :
                        requ='www'+requ

                path_name= os.path.dirname(os.path.realpath("server.py"))
                # do stuff
                path_name=path_name+'/'+requ
                if os.path.isdir(path_name):
                        
                        if 'index.html' in os.listdir(path_name):
                                data = self.get_file('/'+requ+'/index.html')
                                data = self.create_header(data,'html')
                                self.request.sendall(data)
                                return
                        else:
                                data = self.make_index2(path_name)
                                data = self.create_header(data,'html')
                                self.request.sendall(data)
                                return
                else:
                        data='<html><head><h2>Error 404! Page not Found</h2></head>'
                        error=self.create_header(data,404)
                        self.request.sendall(error)
                        print 'error  ' + requ
                        return 

                                
                                                 
if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()



