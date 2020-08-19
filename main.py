from requests_html import HTMLSession
import re
import pandas as pd
import time
import os
import subprocess

#                              NEED HTTP OF THE PAGE TO SCRAPE AND A HTML FILE TO WRITE TO
class Prepare:
    def __init__(self,URL:str, Directory:str,write_html = False,New_path = False):
        self.url = URL
        self.w_html = write_html
        self.directory = Directory
        self.new_path = New_path

    def Scraping(self): #Scraping(url='https://github.com/pyppeteer/pyppeteer/tree/dev/pyppeteer')
        session = HTMLSession()
        r = session.get(self.url)
        r.html.render()
        full_text = [r.html.html]
        #print(type(full_text[0]))
        #print(type(full_text))
        file_path = os.path.join(self.directory,'git.html')
        if self.w_html:
            with open(file = file_path, mode='w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                # for row in full_text
                try:
                    writer.writerow(full_text)
                except Exception as e:
                    print(e)

        return full_text , file_path


    #                          NEED GIT.HTML FROM REQUEST-HTML TO CREATE DATAFRAME

    def HalfTable(self):
        start_time = time.time()
        now, html_directory = self.Scraping()

        head = re.findall(''' title="([.\w]+.py)" ''', now[0])
        body = re.findall(''' <a data-pjax="true" title="([-.,*\[\]>_#\w\s]+)''', now[0])
        body = body[1:]
        table = pd.DataFrame(columns=['Filename', 'Content'])
        table.Filename = head
        table.Content = body
        print('this is the table: ')
        print(table)
        print(table['Filename'].values.tolist())
        end_time = time.time()
        print('Process finished in {} seconds '.format(start_time - end_time))
        # table.to_excel('content-pyppepeer.xlsx')
        return table

    def Cloning(self):
        git_repository = self.url[:self.url.rfind('/tree/')] +'.git'

        try:
            if self.new_path:
                os.chdir(self.directory[:self.directory.rfind('//')])  # change direction to the path direction
                os.mkdir(self.directory[self.directory.rfind('//') + 1:])  # path[path.rfind('//')+1:] Folder name
                os.system('cd ' + self.directory[self.directory.rfind('//') + 1:])
                clone_st = 'git clone -- ' + git_repository
                subprocess.run(clone_st, shell=True)
            else:
                os.chdir(self.directory)
                clone_st = 'git clone -- ' + git_repository
                subprocess.run(clone_st, shell=True)
        except Exception as e:
            print(e)
        else:
            print('Cloning Successfully, waiting to finish...')

    ###################################################################################################################
    ###################################################################################################################

    #data = pd.read_excel(r'E:\Coding 1 Project\Pycharm 101\content-pyppepeer.xlsx')
    #data = HalfTable()
    # print('This is data',data['Filename'].values.tolist())
    ''' Although the new file created have no end, it is still treated as a csv'''

    def makecopy(self,directory: str):  # directory of the file to be copied
        try:
            f = open(file=directory, mode='r')
            nopy = directory[:directory.rfind('.')]
            filename = nopy[nopy.rfind('\\') + 1:]
            with open(
                    file=os.path.join(
                        directory[:directory.rfind('\\')], filename
                    )
                    , mode='w') as file:  # Open new file
                for obj in f.read():
                    # print(obj)
                    file.write(obj)
        except Exception as e:
            print("makecopy Error, ", e)
        else:
            print(f'Making copy {filename} done, waiting to be completed...')

    # makecopy(directory=r'E:\Coding 1 Project\Pycharm 101\main - Copy.py')

    ''' Search for the directory of the folder that contain all the .py find from the packages we need'''

    def find_dir(self,current_directory: str,
                 Filename) -> str:  # Not actually current direction but direction which contain the files
        try:
            # print([Filename])
            os.chdir(current_directory)
            extraction = str()
            # print("this is: ", Filename)
            for root, dirs, files in os.walk(".", topdown=False):
                # print(files)
                n = 0
                for x in Filename:
                    if x in files:
                        n += 1
                        if n == len(Filename):
                            # print('This is x:',x)
                            # print('this is file',files)
                            extraction = os.path.join(os.getcwd(), root)
        except Exception as e:
            print('find_dir Error,', e)
        else:
            print('Getting Extraction done, returning Extraction...')
            # print(extraction)
            return extraction

    # curr_dir = os.getcwd() #Not actually gonna use current direction but direction of the files
    # print(find_dir(curr_dir))

    ''' list of files' name --> If in search for root of Files --> use root to make copies of files '''

    def MakeCopies(self):  # Direction which contain the Folder that has all the files
        global path
        global Filename
        Filename = self.HalfTable()
        Filename = Filename['Filename'].values.tolist()
        path = self.find_dir(current_directory=self.directory, Filename=Filename)  # Not actually curr direction
        for file in Filename:
            self.makecopy(directory=os.path.join(path, file))
    # work = data['Filename'].values.tolist()
    # print(work)
    # print([{*work}])

    def RemoveCopies(self):
        try:
            print(path)
            nopy = [x[:x.rfind('.')] for x in Filename]
            print(nopy)
            os.chdir(path)
            for file in nopy:
                os.remove(file)
                print(f'{file} has been remove successfully!')
        # except FileNotFoundError as e:
        #    print('File Does Not Exist: ',e)
        # except NameError as e1:
        #    print('Copies have')
        except Exception as e:
            print('Error: ', e)

    # RemoveCopies(direction=curr_dir)


obj = Prepare(URL=r'https://github.com/pyppeteer/pyppeteer/tree/dev/pyppeteer',
              Directory=r'E:\Coding 1 Project\Pycharm 101',write_html = False)

obj.RemoveCopies()
#obj.Cloning()
#url = r'https://github.com/pyppeteer/pyppeteer/tree/dev/pyppeteer'
#print(url[:url.rfind('/tree/')])
