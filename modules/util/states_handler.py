
#######################
## HANDLER OF STATES ##
#######################

ongoing_processes = {} # Dictionary of dictionarys of NextStep objects (chat : user : NextStep instance)

class NextStep(object):
    def __init__(self, data, next_function, last_step = True):
        self.data = data
        self.next_function = next_function
        self.last_step = last_step
        self.add_ongoing_process()


    def add_ongoing_process(self):
        """
        Adds an ongoing process to the list.
        """
        if not (self.data['chat'] in ongoing_processes.keys()):
            ongoing_processes[self.data['chat']] = {}
        ongoing_processes[self.data['chat']][self.data['user']] = self


    def finish_ongoing_process(self):
        """
        Finish the ongoing process for an user.
        """
        del ongoing_processes[self.data['chat']][self.data['user']]


    def run(self, arguments):
        """
        Runs next function and merge new arguments with the previous arguments.
        If a step is the last one, conclude the execution in steps.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        for key, value in arguments.items():
            self.data[key] = value
        self.next_function(self.data)
        if self.last_step:
            self.finish_ongoing_process()