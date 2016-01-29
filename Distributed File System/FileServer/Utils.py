import os
class FileServer():

    def __init__(self, fileLoc):
        self.fileLoc = fileLoc

    def existingFile(self, filename):

        if os.path.exists(filename):
            return True
        return False

    def CREATE(self, request):

        response = 'ERROR! Directory \"{}\" does not exist'.format(dirname) #returns this response if directory doesn't exist 
        filename = request.split(" ")[0].split("=")[1]

        dirname = os.path.dirname(filename)
        if os.path.exists(self.fileLoc+dirname):
            if os.path.exists(self.fileLoc+filename):
                response = 'ERROR! File \"{}\" already exists'.format(filename)
            else:
                open(self.fileLoc+filename, 'a').close()
                response = 'OK. File \"{}\" created'.format(filename)
        return response

    def RENAME(self, filename, newfilename):
        pass

    def REMOVE(self, request):

        filename = request.split(" ")[0].split("=")[1]
        response = "ERROR! Filename \"{}\" does not exist".format(filename)
        if os.path.exists(self.fileLoc+filename):
            if os.path.isdir(self.fileLoc+filename):
                response = "ERROR! {} is a directory".format(filename)
            else:
                os.remove(self.fileLoc+filename)
                response = "OK. {} removed".format(filename)
        return response

    def READ(self, request):

        response = "ERROR: READ failed"
        request = request.split(" ", 2)
        
        if len(request) is not 3:
            response = "ERROR: Incorrect command"
        filename = request[0].split("=")[1]
        offset = int(request[1].split("=")[1])
        count = int(request[2].split("=")[1])

        if self.existingFile(self.fileLoc+filename):
            file = open(self.fileLoc+filename, "r")
            file.seek(offset)
            read = file.read(count)
            file.close()
            response = "OK: \n{}".format(read)
        return response

    def WRITE(self, request):

        response = "ERROR! Write failed"
        request = request.split(" ", 2)

        if len(request) is not 3:
            response = "ERROR! Incorrect command"

        filename = request[0].split("=")[1]
        offset = int(request[1].split("=")[1])
        content = request[-1].split("=", 1)[-1]

        if self.existingFile(self.fileLoc+filename):
            file = open(self.fileLoc+filename, "w")
            file.seek(offset)
            file.write(content)
            file.close()
            response = "OK! Write completed"
        else:
            response = "ERROR! {} does not exist".format(filename)

        return response

    def MKDIR(self, request):

        response = 'ERROR: Directory \"{}\" does not exist'.format(dirname)
        filename = request.split(" ")[0].split("=")[1]
        dirname = os.path.dirname(filename)

        if os.path.exists(self.fileLoc+dirname):
            if os.path.exists(self.fileLoc+filename):
                response = 'ERROR! Directory \"{}\" already exists'.format(filename)
            else:
                os.mkdir(self.fileLoc+filename)
                response = 'OK. Directory \"{}\" created'.format(filename)
        return response

    def RMDIR(self, request):

        filename = request.split(" ")[0].split("=")[1]
        response = 'ERROR! Directory \"{}\" does not exist'.format(filename) #returns this response if directory doesn't exist 
        filename = request.split(" ")[0].split("=")[1]

        if os.path.exists(self.fileLoc+filename):
            os.rmdir(self.fileLoc+filename)
            response = "OK. {} removed".format(filename)
        return response

    