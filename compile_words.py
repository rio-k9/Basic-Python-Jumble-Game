import shelve

def default_list():
    print("Finding default word categories....")
    with open("hope_words.txt") as afile, open("amazement_words.txt") as bfile, open("sad_words.txt") as cfile, open("merry_words.txt") as dfile:  
        hop_list = [word.strip(",") for line in afile for word in line.split()]
        ama_list = [word.strip(",") for line in bfile for word in line.split()]#multiple with statements to create multiple variables simaltaneously
        sad_list = [word.strip(",") for line in cfile for word in line.split()]
        mer_list = [word.strip(",") for line in dfile for word in line.split()]
    print("Finding saved word categories....") 
    shelf = shelve.open("Game Words")
    print("Synchronising....")
    shelf["Hope"] = hop_list
    shelf["Amazement"] = ama_list
    shelf["Sad"] = sad_list
    shelf["Merry"] = mer_list
    shelf.sync()
    shelf.close()
    print("Done.")
