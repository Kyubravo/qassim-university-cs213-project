'''
    This Project is by:

    Name: Muhammad Abdullah Alhomed
    ID: 391107963
    
    Name:  ABDULLAH MOHAMMED A. ALOLAYQI
    ID: 391108011

'''

import re
import csv 
import matplotlib.pyplot as plt # For graphs
import tkinter as tk # for GUI

""" import pandas as pd
import matplotlib.pyplot as plt
import numpy as np """

class Book:
    ListOfBooks = []
    __indexList = []
    
    # using regex
    """ # Must be used first to set the catagory Index csv file
    @classmethod
    def openCatagoryIndexFile(cls, csvFilePath):
        indexFile = open(csvFilePath)
        indexReturn = indexFile.read()
        catagoryRegex = re.compile(r'(\d), (\w*)')
        cls.__indexList = catagoryRegex.findall(indexReturn)
        indexFile.close() """
    
    # using csv library
    # Must be used first to set the catagory Index csv file
    @classmethod
    def CatagoryIndexFile(cls, csvFilePath):
        
        csvIndexFile = open(csvFilePath)
        indexReader = csv.DictReader(csvIndexFile) # import the csv file as a dictionary with the row names as the keys
        for row in indexReader:
            cls.__indexList.append((int(row['index']),row['catagory']))
        csvIndexFile.close()

    @classmethod
    def importFromCSVfile(cls,csvFilePath):
           
        csvIndexFile = open(csvFilePath)
        indexReader = csv.DictReader(csvIndexFile) # import the csv file as a dictionary with the row names as the keys
        
        for row in indexReader:
            Book(row['index'],row['title'],row['numberOfPages'],row['catagoryIndex'])
        csvIndexFile.close()
        return cls.ListOfBooks # return a list of Book objects

    @classmethod
    def getBookByIndex(cls,bookIndex):
        for book in Book.ListOfBooks:
            if book.getIndex() == bookIndex:
                return book

    @classmethod
    def getBookByTitle(cls,bookTitle):
        for book in Book.ListOfBooks:
            if book.getTitle() == bookTitle:
                return book

    @classmethod
    def getCatagoryByIndex(cls,catagoryIndex):
        for catagoryListing in Book.__indexList:
            if catagoryListing[0] == catagoryIndex:
                return catagoryListing[1]

    def __init__(self, bookIndex, title, pageNum, catagoryIndex):
        self.__bookIndex = bookIndex
        self.__title = title
        self.__pageNum = pageNum
        self.__catagoryIndex = catagoryIndex

        Book.ListOfBooks.append(self) # add to the list to look it up if needed using getBookByIndex()
    
    def getIndex(self):
       return self.__bookIndex

    def getTitle(self):
       return self.__title
       
    def getpageNum(self):
       return int(self.__pageNum)

    def getCatagoryIndex(self):
       return int(self.__catagoryIndex)
       
    def getCatagoryName(self):
        for i in Book.__indexList:
            if int(i[0]) == self.__catagoryIndex: # check the Indice
                return i[1] # if it's true, then return the catagory


class Member:
    
    listOfMembers = [] # list of all members, static

    @classmethod
    def importFromCSVfile(cls,csvFilePath):
           
        csvIndexFile = open(csvFilePath)
        indexReader = csv.DictReader(csvIndexFile) # import the csv file as a dictionary with the row names as the keys

        readBooksIndexRegex = re.compile(r'(\d+)') # this takes separated numbers in any format and turns them into a list.

        memberObjectList = []
        for row in indexReader:
            readBooksIndexList = readBooksIndexRegex.findall(row['readBooksIndex'])
            member = Member(row['index'],row['name'],row['phoneNumber'],row['email'])
            for bookIndex in readBooksIndexList:
                member.addReadBook(Book.getBookByIndex(bookIndex)) # add all the read books to the member's readbooks list
            memberObjectList.append(member)
        csvIndexFile.close()
        return memberObjectList # return a list of all imported members

    @classmethod
    def getMemberByIndex(cls,memberIndex):
        for member in Member.listOfMembers:
            if member.getIndex() == memberIndex:
                return member

    def __init__(self,index, name, phoneNumber, email):
        self.__index = index
        self.__name = name
        self.__phoneNumber = phoneNumber
        self.__email = email
        self.__numberOfReadPages = 0 # the pages the member read
        
        self.readBooks = [] # keep track of books that read books for the preson
    
        Member.listOfMembers.append(self) # add the instance of the Member class to listOfMembers which is static
    
    def getIndex(self):
       return int(self.__index) 
       
    def getName(self):
       return self.__name 
       
    def getPhoneNumber(self):
       return self.__phoneNumber
       
    def getEmail(self):
       return self.__email
       
    def getNumberOfReadPages(self):
        return int(self.__numberOfReadPages)
        
    def addReadBook(self,bookClassList): # NOTE: the format addReadBook(book1,book2,...) is not supported
        if(type(bookClassList) == list): # if it's a list in format addReadBook([book1,book2,...])
            for book in bookClassList:
                self.readBooks.append(book) # add the book to the list of the member 
                self.__numberOfReadPages += book.getpageNum() # count read pages for the member

        elif(type(bookClassList) == Book): # if it's a Book object in format addReadBook(book1)
            self.readBooks.append(bookClassList) # add the book to the list of the member 
            self.__numberOfReadPages += bookClassList.getpageNum() # count read pages for the member

        elif(type(bookClassList) == int): # if it's an index of a book in format addReadbook(1)
            book = Book.getBookByIndex(bookClassList) # get the book object using the index
            self.readBooks.append(book) # add the book to the list of the member 
            self.__numberOfReadPages += book.getpageNum() # count read pages for the member


def catagoryRanking(): #ranking catagory, format [[book1,count1],[book2,count2],...]
    rawCatagoryList = [] #list every Catagory "with" repeating 
    
    for member in Member.listOfMembers: # list every get Catagory Index read book "with" repeating 
       for book in member.readBooks:
           rawCatagoryList.append(book.getCatagoryIndex())
       
    IndexList = [] # list every Catagory Index "without" repeating 
    for i in rawCatagoryList:
        if IndexList.count(i) == 0 :
            IndexList.append(i)

    catCount = [] # catagory rank count the read 
    for i in IndexList: # count how many times the catagory his been read 
        catCount.append(rawCatagoryList.count(i)) 
        
    sortedCat = [] # final list that will be returned   
    for i in range(len(IndexList)): # formats the catagories in the format [[book1,count1],[book2,count2],...]
        sortedCat.append((IndexList[i],catCount[i]))
    sortedCat.sort(reverse=True ,key=lambda sortedCat: sortedCat[1]) # sort the list and the key lambda is telling the sort function to sort depending on the second element on the tuple
    return sortedCat
    
        
def memberRankingBooks():
    rawRankList= [] 
    for member in Member.listOfMembers:
        rawRankList.append((member.getName(), len(member.readBooks))) # save the length with the name of the member in one tuple in the list 
    rawRankList.sort(reverse=True ,key=lambda rawRankList: rawRankList[1]) # sort the list and the key lambda is telling the sort function to sort depending on the second element on the tuple 
    return rawRankList
    
def memberRankingPages():
    rawRankList= [] 
    for member in Member.listOfMembers:
        rawRankList.append((member.getName(), member.getNumberOfReadPages())) # save the number of read pages of the member with the name of the member in one tuple in the list 
    rawRankList.sort(reverse=True ,key=lambda rawRankList: rawRankList[1]) # sort the list and the key lambda is telling the sort function to sort depending on the second element on the tuple 
    return rawRankList

def pltCatRank():
    catRankRaw, catPlace, catCount = [], [], []
    catRankRaw = catagoryRanking() # formats the catagories in the format [[book1,count1],[book2,count2],...]
    catOrder = []  
    i = 0
    while(i < len(catRankRaw)): # Splitting the values
        catPlace.append(catRankRaw[i][0])
        catCount.append(catRankRaw[i][1])
        i+= 1
    for i in catPlace: # covert the catagory indice to the name of the catagory
        catOrder.append((Book.getCatagoryByIndex(i)))
    
    # make the plot
    plt.bar(catOrder,catCount) # (x, y)
    plt.xticks(rotation=30,size=8)
    plt.xlabel('Catagory Name')
    plt.ylabel('Number of read catagories')
    plt.show()

def pltMemberRankBook(): # plt the rank of the members dependenig on how many book have been read 
    memberRankRaw, memberPlace, memberCount = [], [], []
    memberRankRaw = memberRankingBooks()

    i = 0
    while(i < len(memberRankRaw)): # Splitting the values
        memberPlace.append(memberRankRaw[i][0])
        memberCount.append(memberRankRaw[i][1])
        i += 1

    plt.bar(memberPlace,memberCount) # (x, y)
    plt.xticks(rotation=30,size=8)
    plt.xlabel('member Name')
    plt.ylabel('Number of read books')
    plt.show()

def pltMemberRankPages():
    memberRankRaw, memberPlace, memberCount = [], [], []
    memberRankRaw = memberRankingPages()

    i = 0
    while(i < len(memberRankRaw)): # Splitting the values
        memberPlace.append(memberRankRaw[i][0])
        memberCount.append(memberRankRaw[i][1])
        i += 1

    plt.bar(memberPlace,memberCount) # (x, y)
    plt.xticks(rotation=30,size=8)
    plt.xlabel('Member name')
    plt.ylabel('Number of read pages')
    plt.show()


# ============ GUI ============#
def openBooksWindow(books):
    window = tk.Toplevel()
    window.title('Books')

    mainFrame = tk.Frame(window,width=400,height=300)
    mainFrame.pack(fill='both',padx=10, pady=10)

    leftFrame = tk.Frame(mainFrame,width=200)
    leftFrame.pack(side='left',fill='y',padx=10, pady=10)

    rightFrame = tk.Frame(mainFrame,width=200)
    rightFrame.pack(side='right',fill='y',padx=10, pady=10)
    
    # left frame
    lb = tk.Listbox(leftFrame, selectmode='browse')
    for book in books:
        lb.insert(book.getIndex(), book.getTitle())
    lb.pack(fill='both')
    lb.select_set(0)


    #right frame
    lbSelectedIndex = lb.curselection()[0]
    label = tk.Label(rightFrame,text='Book index: {}\nBook title: {}\nPages: {}\n'.format(lbSelectedIndex, \
                                                                                books[lbSelectedIndex].getTitle(), \
                                                                                books[lbSelectedIndex].getpageNum() \
                                                                              ), \
                    justify='left',anchor='nw'
                    )
    label.pack(fill='both')


    def showInfo(): # Show info button, updating label from simply selecting something else in the listbox is impossible with tkinter library, this is a work around by using showButton and a function
        lbSelectedIndex = lb.curselection()[0]
        label.config(text='Book index: {}\nBook title: {}\nPages: {}\n'.format(lbSelectedIndex, \
                                                                                books[lbSelectedIndex].getTitle(), \
                                                                                books[lbSelectedIndex].getpageNum() \
                                                                              )
                    )
    showButton = tk.Button(rightFrame,text='Show Book Info',command=lambda: showInfo())
    showButton.pack(side='bottom')

    window.mainloop()


def openMembersWindow(members,books):
    window = tk.Toplevel()
    window.title('Members')

    mainFrame = tk.Frame(window)
    mainFrame.pack(fill='both',padx=10, pady=10)

    leftFrame = tk.Frame(mainFrame)
    leftFrame.grid(row=0,column=0,padx=10, pady=10,)

    midFrame = tk.Frame(mainFrame)
    midFrame.grid(row=0,column=1,padx=10, pady=10)

    rightFrame = tk.Frame(mainFrame)
    rightFrame.grid(row=0,column=2,padx=10, pady=10)
    


    # left frame
    leftlabel = tk.Label(leftFrame,text='Members')
    leftlabel.pack(side = 'top',anchor='n')
    leftlb = tk.Listbox(leftFrame)
    for member in members:
        leftlb.insert(member.getIndex(), member.getName())
    leftlb.pack(fill='both',anchor='n')
    leftlb.select_set(0)

    # middle frame
    midlabel = tk.Label(midFrame,text='Read books by the member')
    midlabel.pack(side = 'top')
    midlb = tk.Listbox(midFrame)
    for book in books:
        midlb.insert(book.getIndex(), book.getTitle())
    midlb.pack(fill='both',side='top',expand=1)
    midlb.select_set(0)

    #right frame
    member = Member.getMemberByIndex(midlb.curselection()[0])
    label = tk.Label(rightFrame,text='Member index: {}\nName: {}\nPhone: {}\nEmail: {}'.format(member.getIndex(), \
                                                                                member.getName(), \
                                                                                member.getPhoneNumber(), \
                                                                                member.getEmail() \
                                                                              ), \
                    justify='left',anchor='nw'
                    )
    label.pack(fill='both')


    # mainframe again
    def showMemberInfo(memberIndex): # Show info button, updating label from simply selecting something else in the listbox is impossible with tkinter library, this is a work around by using showButton and a function
        member = Member.getMemberByIndex(memberIndex)
        
        midlb.delete(0,tk.constants.END) # Delete all items

        for book in member.readBooks: #add member's read books to the midlb
            midlb.insert(book.getIndex(), book.getTitle())
        
        label.config(text='Member index: {}\nName: {}\nPhone: {}\nEmail: {}'.format(member.getIndex(), \
                                                                                member.getName(), \
                                                                                member.getPhoneNumber(), \
                                                                                member.getEmail() \
                                                                                )
                    )

    showMemberInfoButton = tk.Button(mainFrame,text='Show Member Info',command=lambda: showMemberInfo(leftlb.curselection()[0]))
    showMemberInfoButton.grid(row=1,column=0)

    window.mainloop()

def openGraphsWindow():
    window = tk.Toplevel()
    window.title('Graphs')
    button1 = tk.Button(window,width=30, text='Catagory ranking',command=lambda: pltCatRank()).pack(padx=10,pady=5)
    button2 = tk.Button(window,width=30,text='Books read by each member ranking',command=lambda: pltMemberRankBook()).pack(padx=10,pady=5)
    button3 = tk.Button(window,width=30,text='Pages read by each member ranking',command=lambda: pltMemberRankPages()).pack(padx=10,pady=5)

## ================ MAIN ================ ##

### IMPORTANT!!!!!
Book.CatagoryIndexFile('catagoryIndex.csv')
Book.importFromCSVfile('bookIndex.csv')
Member.importFromCSVfile('memberIndex.csv')
###

# Gui Setup
root = tk.Tk()
root.title('Library program!')
root.maxsize(300,80)
root.minsize(300,80)

frame = tk.Frame(root,width=300, height=80, padx=10, pady=5)
frame.pack()

button = tk.Button(frame,text='Books',width=20,command=lambda: openBooksWindow(Book.ListOfBooks)).pack(side='left')

button2 = tk.Button(frame,text='Members',width=20,command=lambda: openMembersWindow(Member.listOfMembers, Book.ListOfBooks)).pack(side='right')

button3 = tk.Button(root,text='Graphs',width=25,command=lambda: openGraphsWindow()).pack(pady=10)

root.mainloop()

""" 
# Data input in run-time
a = Member(10,"ahmed", '050505' ,'xyz@xyz')
b = Member(11,"naif", '050505' ,'xyz@xyz')
c = Member(12,"khalid", '050505' ,'xyz@xyz')

        # (bookIndex, title, pageNum, catagoryIndex)
booka = Book(1,'', 69, 1)
bookb = Book(2,'', 125, 2)
bookc = Book(3,'', 125, 2)
a.addReadBook(1)
b.addReadBook([bookb])
c.addReadBook([booka,bookb])
"""
pltCatRank()
pltMemberRankBook()
pltMemberRankPages()