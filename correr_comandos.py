import re
import asyncio
import subprocess
from typing import Self
from rich.logging import RichHandler

import logging
import functools
from mothur import comandos as co
import  time

class run_commands:

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(show_path=False)],
    )
    
    async def run_mothur_commands(self,commands,mothur_dir):
        evento_error=asyncio.Event()
        evento_warning=asyncio.Event()

        # Example Mothur commands using comandos module
        await self.execute_cmd([mothur_dir,f"#set.logfile(name=myCollectLogfile2)"],evento_error,evento_warning)

        for index,cmd in enumerate(commands):
            if(isinstance(cmd,list)):
                cmd=self.unificar(cmd)
                
            await self.execute_cmd([mothur_dir,f"#set.logfile(name=myCollectLogfile2,append=T);{cmd}"],evento_error,evento_warning)
            if(evento_error.is_set()):
                #print(f"$$$$$44$$$$$$$$$$$ ERROR DETECTADO {index}$$$$$$$$$$$$$$$$$$$$$$$")
                return(index)
            else:
                if(evento_warning.is_set()):
                    evento_warning.clear()
                    #print(f"########### Alerta detectada en comando numero {index} ###########")
        return True

    async def execute_cmd(self,cmd,eventE,eventW):
        loop = asyncio.get_running_loop()
        #writer = asyncio.StreamWriter()
        # Create the subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )


        # Read from stdout and stderr asynchronously
        async def read_stream_stdout(stream,eventE,eventW):
            async for line in stream:
                texto=line.decode().rstrip()
                self.logger.debug("%s", texto)
                self.check_problem(texto,eventE,eventW)
                
                # Trigger the event upon receiving a new line
                
        async def read_stream_stderr(stream):
            async for line in stream:
                self.logger.debug("%s", line.decode().rstrip())

        # Gather reading from stdout and stderr and waiting for the subprocess to finish

        await asyncio.gather(
            read_stream_stdout(process.stdout,eventE,eventW),
            #read_stream_stderr(process.stderr),
            process.wait()
        )

    # Rest of your code remains the same
    def unificar(self,lista_comandos):
        command=""
        for item in lista_comandos:
            if(command!=""):
                command=command+";"+item
            else:
                command=command+item
        return command

    def check_problem(self,text,eventE,eventW):
        # Search for [WARNING] or [ERROR] from the end of the text
        warning_detected=re.search(r'\[WARNING\]', text)
        error_detected= re.search(r'\[ERROR\]', text)
        if warning_detected:
            eventW.set()
            print("Warning found!")
        elif error_detected:
            eventE.set()
            print("error found")
            
    

    #asyncio.run(run_mothur_commands())
