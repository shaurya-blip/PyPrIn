# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~ PPrin Packer ~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~ By SblipDev  ~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# --------- ERRORS ------------ #

class PPrinError(Exception):
    """Base class for exceptions in this module."""
    pass
# bruh

class ForeignLanguageError(PPrinError):
    pass

# ----------------------------- #

import os
import shutil
import json

class PPrin:
    """
    Base class for PPrin Packer.
    
    pid -- Program ID : str
    pname -- Program Name : str
    ppath -- Program Path : str
    pauthor -- Program Author : str
    pversion -- Program Version : float
    pdependency -- Program : list
    """
    
    def __init__(self, pid, pname, ppath, pauthor, pversion, pdependency):
        """
        Check arguments above.
        Raises ForeignLanguageError if the specified file is not python or ipython.
        """
        
        if ppath.endswith('.py') or ppath.endswith('.ipy'):
            pass
        else:
            raise ForeignLanguageError("Only Python and IPython files are supported.")
        
        self.pid = pid
        self.pname = pname
        self.ppath = ppath
        self.pauthor = pauthor
        self.pversion = pversion
        self.pdependency = pdependency
        
        self.pprinpathjustname = ppath.replace('.py', '')
        self.pprinname = self.pprinpathjustname+".pprin"
        self.pprinunpackednm = self.pprinpathjustname + ".tmppprin"
        

    def __str__(self):
        return self.__class__.__name__ + " Object : " + str(self.__dict__)
    
    def __repr__(self): 
        return self.__class__.__name__ + "(" + str(self.__dict__) + ")"
    
    def if_exists(self,path):
        if os.path.exists(path):
            return True
        else:
            return False
        
    
    def write_file(self, path, content):
        path = self.pprinunpackednm + "/" + path
        
        f = open(path, 'w+')
        f.write(content)
        f.close()

        return path
    
    def read_file(self, path):
        f = open(path, 'r')
        content = f.read()
        f.close()
        return content
    
    def make_archive(self, source, destination):
        # Made folder an archive for easy unpacking.
        shutil.make_archive(destination, 'zip', source)
    
    def create_pprin_file(self):
        if self.if_exists("pprinunpackednm") is True:
            shutil.rmtree(self.pprinunpackednm, ignore_errors=False, onerror=None)
        
        os.makedirs(self.pprinunpackednm)
        
        self.write_file(self.pprinpathjustname+".py", self.read_file(self.ppath))
        
        conf = {
            "PID":self.pid,
            "NAME": self.pname,
            "PATH": os.path.abspath(self.ppath),
            "AUTHOR": self.pauthor,
            "VERSION": self.pversion,
            "DEPENDENCY": self.pdependency,
        }
        
        out_file_json = open(self.pprinunpackednm+"/"+self.pprinpathjustname+"-conf.json", 'w+')
        json.dump(conf, out_file_json, indent=4)
        out_file_json.close()
        
        self.make_archive(self.pprinunpackednm, self.pprinname)
        
        shutil.rmtree(self.pprinunpackednm, ignore_errors=False, onerror=None)
        
        return self.pprinname
        
object1= PPrin("lol-ok", "lol", "program1.py", 'aki', '0.1', 'none')
object1.create_pprin_file()

