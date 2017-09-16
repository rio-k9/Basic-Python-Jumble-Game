import random, string, glob, shelve, time
from compile_words import default_list#demonstrating I can import my own modules and have all modules variables work properly



def startup_menu():      
    i=True
    while i:  #startup menu used with while loop to show variation in knowledge of loops
        print("Select From The Following Options")
        print("-------------------------")
        print("0. Exit")
        print("1. Start Game")
        print("2. Browse Words")
        print("3. Add Words")
        print("4. Delete Words")
        print("5. Saved Scores")
        print("-------------------------")
        choice=input("\n\nWhat will it be?:  ")

        if choice=="1":
            
            play_game()


        elif choice=="2":
            print("\nYou have selected 'Browse Words' ")
            browse()
              
        elif choice=="3":
            print("\nYou have selected 'Add Words' ")
            try:
                newfile=input("\n\nPlease enter the name of your text file, with '.txt' included:  ")
                new_list(newfile)
            except FileNotFoundError: #Error Exception used multiple times throughout coursework
                print("\nFile Not Found, Try Again.")
                new_list(newfile)

        elif choice=="4":
            print("\nYou have selected 'Delete Words' ")
            global shelf
            delete_list()

        elif choice=="5":
            print("\nYou have selected 'Saved Scores' ")
            try:
                scorekeep()
            except TypeError:
                print("Demonstrating a TypeError exception. Restart the game, and please press 5 again!")  
                startup_menu()
             #I had a bit of trouble with starting up the scorekeep function after a game had been played, may be due to missing open on shelves after game is played?
        elif choice=="0":
            print("\n\nGoodbye.\n")
            exit()

        elif choice!="":
            print("\nThat is not a valid option. \nPlease choose and integer from [1, 2, 3 or 4].\n  ")
            return startup_menu()


#def wordlist():
    #with open("hope_words.txt") as afile:
        #global the_list
        #the_list = [word.strip(",") for line in afile for word in line.split()]
    #print(the_list)
#Incase I wanted to create list variable instead of using shelve
    

#I had trouble with browse() function. I spent some time playing around with additional for and while loops, but my input at variable is only able to delete the wordset
#at the bottom of the list, or the menu option. I used a hotfix of additional elif statements

    #Could be a minor syntax problem as my start menu works fine.
def browse():
    print("Downloading words....")
    shelf = shelve.open("Game Words")
    print("Scanning for words....")
    print("-------------------------")
    print("Menu")
    for i in shelf.keys():
        print(i)
    print("-------------------------")
    global name
    name = str(input("\n\nPlease enter your choice:  "))
    
    if name =="Menu":
        startup_menu()
    elif name == "Amazement":
        print("Your words: {}".format(shelf["Amazement"]))
    elif name == "Hope":
        print("Your words: {}".format(shelf["Hope"]))
    elif name == "Sad":
        print("Your words: {}".format(shelf["Sad"]))
    elif name == "Merry":
        print("Your words: {}".format(shelf["Merry"]))
    elif name == i in shelf.keys():
        print("Your words: {}".format(shelf[name]))
    else:
        print("\nThat is not a valid option. Remember this program is Case Sensitive.\nBrowsing....")
        return browse()

    
def new_list(newfile):
    print("\nSearching....")
    with open(newfile) as afile:
        the_list = [word.strip(",") for line in afile for word in line.split()]
    print("\nFormatting....")
    shelf = shelve.open("Game Words")
    name=input("\n\nWhat would you like to call your wordset?:  ")
    shelf[name] = the_list
    print("\nSynchronising....")
    shelf.sync()
    print("\nClosing")
    shelf.close()
    print("\nDone.")
    print("\nLoading word sets....\n")
    browse()



#I had trouble with delete_list function the same as browse(). Only able to delete from bottom of list or enter a delete_words="Hope" etc. 
def delete_list():
 
    print("Scanning for words....")
    shelf = shelve.open("Game Words")
    print("-------------------------")
    print("Menu")
    for i in shelf.keys():
        print(i)
    print("-------------------------")
    global delete_words
    delete_words = input("\nPlease enter the name of the words you want to delete, or 'Menu' to return:  ")
    if delete_words == i in shelf.keys():
        del shelf[delete_words]
        shelf.sync()
        shelf.close()
        print("\nDeleted")
    elif delete_words =="Menu":
        return startup_menu()
        return delete_list()
    elif delete_words!="":
        print("\nNot valid option, remember the program is Case Sensitive\n")
        return delete_list()
    
def get_jumble():  #demonstrating my use of Functions, infact most of my code is designing functions
    global word
    global correct
    global jumble  #global variables
    jumble =""
    word=random.choice(wordlist)
    correct=word
    while word:
        position = random.randrange(len(word))
        jumble += word[position]
        word = word[:position] + word[(position + 1):]
        
#Main gameplay function
def play_game():
    shelf = shelve.open("Game Words")
    local_time = time.asctime(time.localtime(time.time())) #demonstrate use of local time module
    print("\nLoading word categories....\n")
    print("-------------------------")
    for i in shelf.keys(): #further use of for loops
        print(i)
    print("-------------------------")
    x=True
    while x: #further use of while loops
        try:
            word_set = input("\nPlease select a word set:  ")
            global wordlist
            global score
            wordlist = shelf[word_set]
            score = 0
            get_jumble()
            for i in range(9): #range of 9 to create 10 jumble words (index 0 - 9)
                get_jumble()
                print("\nThe jumble word is: {}".format(jumble))
                print("\nFor you Coral, here is the answer:{}".format(correct))

                guess = input("\nEnter your guess: ").lower()

                if(guess == correct):
                    print("\nCongratulations! You guessed it")
                    score += 1
                    print("\nYour score is {}".format(score))

                else:
                    print("Sorry, wrong guess. Next word. \n")
            x=False
        except KeyError:
            print("\nNot a valid option, remember the program is case sensitive!")

    player_name=input("Please enter your name:  ")
    print("\nYou got {} out of 10, {}.".format(score, player_name))
    shelf = shelve.open("Saved Scores")
    savedgame=["<<<Score:{} Name:{}, Date:{}>>>".format(str(score), player_name, str(local_time))] #demonstrate knowledge of formatting
    try:
        
        shelf["Scores"] = shelf["Scores"] + savedgame
        shelf.sync()
        shelf.close()
    except KeyError: #error exception for the way the data is shelved. if no DAT file exists yet an error was thrown and scores = the first saved game
        shelf["Scores"]=savedgame
    return startup_menu()

def scorekeep():
    shelf = shelve.open("Saved Scores")
    for i in shelf.keys():
        print(shelf[i]) #I feel the use otf my for loop may be linked to the browse() and delete_list() problems. as scorekeep only loads if the game hasn't been played yet, bu
    shelf.close()#but does always save to shelve
    startup_menu()
        
default_list()
startup_menu()

#Was not able to sort scores with the local time included, but demonstrating that I was able to do it with the comments alone.
#In my full code I made it to include the users name, score and the date and time, but I could not find a way to sort with strings included , without using sort() inbuilt function.

#import shelve
#shelf = shelve.open("Test")
#scores= [10,2,4,1,2,4,6,7]
#shelf["Scores"] = scores
#shelf.sync()
#shelf.close()

#shelf = shelve.open("Test")
#scores = shelf["Scores"]


#sortedscore=[]
#while scores:
    #smallest = min(scores)
    #index = scores.index(smallest)
    #sortedscore.append(scores.pop(index))

#print(sortedscore)



