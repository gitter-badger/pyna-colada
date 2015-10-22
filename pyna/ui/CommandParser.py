from pyna.base.Parser import Parser
from pyna.core.Manager import Manager
from pyna.ui.PynaDisplay import PynaDisplay
from pyna.ui.CommandInterpreter import CommandInterpreter

class CommandParser(Parser):
    def __init__(self, manager,dispatcher):
        self.bindings = manager.getBindings()
        self.interpreter = CommandInterpreter(manager, dispatcher)


    def parse(self, line):
        '''Master method; figures out what was typed by the user'''
        command, remainder = self.determineCommandAndMessage(line)
        
        # Attempt to ascertain the desired command; default to chat
        command = self.parseCommand(command)
        if command is '':
            command = 'chat'
            remainder = line

        # Get the correct method and invoke it
        method_type = 'typed_{0}'.format(command)
        method = getattr(self.interpreter,method_type)
        method(remainder)


    def parseCommand(self,command):
        ''' Attempts to figure out what the user's command was'''
        if command in [self.bindings[key] for key in self.bindings]:
            return [key for key in self.bindings if self.bindings[key] == command][0]
        return ''


    def determineCommandAndMessage(self,line):
        '''Checks to see how to parse the line; specifically deals with 1-word situations'''
        results = line.split(' ',1)
        if len(results) > 1:
            return results[0], results[1]

        # If it's only one, check to see if it is in our bindings
        if results[0] in [self.bindings[key] for key in self.bindings]:
            return results[0], ''

        # Default to Chat
        return 'chat', results[0]
