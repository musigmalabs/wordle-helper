import cmd

from wordle_helper import Result, Wordle, yellow, grey, green

class WordleShell(cmd.Cmd):
    intro = 'Welcome to wordle shell'
    prompt = '[wordle] '

    def do_start(self, args):
        self.wordle = Wordle()
        self.last_guess = self.wordle.next_guess()

        print ('Try', self.last_guess)
    
    def do_result(self, colors):
        result = []

        for i, col in enumerate(colors):
            if col == 'y':
                result.append(yellow(self.last_guess[i]))
            if col == 'b':
                result.append(grey(self.last_guess[i]))
            if col == 'g':
                result.append(green(self.last_guess[i]))
        
        self.wordle.submit_result(Result(result))
        
        self.last_guess = self.wordle.next_guess()
        print ('Try', self.last_guess)

    def do_block(self, args):
        self.wordle.add_to_blocklist(args.strip())

        self.last_guess = self.wordle.next_guess()
        print ('Try', self.last_guess)


if __name__ == '__main__':
    WordleShell().cmdloop()
