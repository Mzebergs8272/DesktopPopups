'''
    programme description: 
        Build a terminal/console application that allows a user to manage a
        collection of contacts. A user should be able to search for a contact by name, and
        find their details - first name, surname, email address, phone number and address.
        The application must allow users to create new contacts and store them in a file. It
        must also be able to load existing contacts from a file on start-up. Requirements:
        Must create / read simple text-based files. Must be able to store at least 100
        contacts. Potential Enhancements: Order the contacts by surname, allow the user to
        search for contacts according to email address, provide a mail-to link that will open a
        new email window with a contacts email address.
    
    'TODO create the option for a more verbose cli experience if the program is run without arguments/flags
    'TODO if the program is run with arguments/flags, only run code associated with them arguments/flags.
    'TODO required arguments: -search -create -print -help
    'TODO ensure that some arguments such as -help or -search cannot be paired with other arguments like -print or -create
    

'''

import json, sys

    

class ContactBook:
    def __init__(self, program_name: str):
        self.args: list[str] = sys.argv[1:]
        self.program_name = program_name or "Contactbook.py"
        
        all_args = {
            "-help": self.print_help,
            "-print": self.print
        }


        self.help_statement = "Use -help | -h | --help to view accepted arguments."

        self.print = {
            "-print": ""
        }
    
    def welcome(self):
        print(f"\nWelcome to {self.program_name}. Create, view and remove contacts in your contact list.")
        print(self.help_statement + "\n")

    def arg_doesnt_exist(self, erroneous_arg: str):
        print("\n" + f"The command you entered {erroneous_arg} does not exist.")
        print("\n" + self.help_statement)

    def check_args(self) -> bool:
        for arg in self.args:
            try:
                self.help[arg]()
            
            except:
                self.arg_doesnt_exist(arg)
                return True
            
        return False
    
    def print(self, args: str):
        pass
    
    def print_help(self):
        print(

    '''
    try using these arguments:

        prints help text                  : -help | -h | --help                                                                      
        prints all your contacts          : -print                                                                                                                    
        search for users by name or email : -search : -name <full name> | -email <email address>                                     
        create a contact                  : -create : <first name> <last name> [ <email address> ] [ <mobile number> ] [ <address> ] 

    '''

             )
        return True

    def cmd_loop(self):
        self.welcome()



if __name__ == "__main__":
    contactbook = ContactBook("Contactbook.py")

    if not contactbook.check_args():
        contactbook.cmd_loop()


