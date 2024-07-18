import subprocess

class stmdevice:
    def __init__(self):
        self.si = subprocess.STARTUPINFO()
        self.si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.result=''
    
    def unlock(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -ob rdp=0xAA',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Option Bytes successfully programmed" in self.result) or ("Warning: Option Byte: rdp, value: 0xAA, was not modified.\n\nWarning: Option Bytes are unchanged, Data won't be downloaded" in self.result) :
            return 0
        else:
            return -1
    
    def lock(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -ob BOOT_LOCK=0x1 -ob nBOOT0=0x0 -ob nSWBOOT0=0x0 -ob nBOOT1=0x1 -ob RDP=0xBB',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Option Bytes successfully programmed" in self.result) or ("Warning: Option Byte: rdp, value: 0xBB, was not modified.\n\nWarning: Option Bytes are unchanged, Data won't be downloaded" in self.result) :
            return 0
        else:
            return -1
    
    def reset(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -rst',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Software reset is performed" in self.result) :
            return 0
        else:
            return -1
    
    def hard_reset(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -HardRst',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Hard reset is performed" in self.result) :
            return 0
        else:
            return -1
        
    def run(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -run',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Core run" in self.result) :
            return 0
        else:
            return -1
    
    def erase(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -vb 1 --erase all',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Mass erase successfully achieved" in self.result):
            return 0
        else:
            return -1
    
    def flash(self,fname):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -vb 1 --download '+ fname +' --verify',startupinfo=self.si,capture_output=True,text=True).stdout
        if ("Download verified successfully" in self.result):
            return 0
        else:
            return -1
    
