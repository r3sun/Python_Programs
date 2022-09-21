from tkinter import *
from tkinter import font
import tkinter as tk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import exceptions


from pprint import pprint

NORMAL_PADDING = 3


cred = credentials.Certificate('firebase_cms/cred.json')
firebase_admin.initialize_app(cred)
DB = firestore.client()
POSTS_COL = DB.collection("posts")


class AllPages(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.font = font.Font(family='JetBrains Mono', name='jbm', size=12, weight='normal')

        self.posts = self.get_post_list()

        self.posts_container = tk.Frame()

        for post in self.posts:
            postf = tk.Frame(self.posts_container, bg="#ffffff", borderwidth=1, relief="solid")
            post_t = tk.Label(postf, text=post["title"], borderwidth=0)
            post_edit = tk.Button(postf, text="Edit", bg="#ffffff", borderwidth=0, relief="solid", highlightbackground="#ffffff", highlightcolor="#ffffff", highlightthickness=1, font=self.font, command= lambda: self.modify_post_form(post))
            post_t.pack(side="left")
            post_edit.pack(side="right")
            postf.pack(anchor=W, fill='x', pady=NORMAL_PADDING)
        
        self.posts_container.pack(fill='both', ipadx=NORMAL_PADDING, padx=NORMAL_PADDING)

    
    def get_dict(self, doc):
        return doc.to_dict()

    def get_post_list(self, count=20, start_after=None):
        if start_after:
            db_stream = POSTS_COL.order_by("timestamp").start_after(start_after).limit(count).stream()
        else:
            db_stream = POSTS_COL.order_by("timestamp").limit(count).stream()

        return list(map(self.get_dict, db_stream))

    def modify_post_form(self, post):
        newW = Toplevel()
        app = CreatePostForm(newW)
        app.pack()



class CreatePostForm(tk.Frame):
    def __init__(self, master, post=None):
        super().__init__(master)
        self.pack()
        if not ("jbm" in font.names()):
            self.font = font.Font(family='JetBrains Mono', name='jbm', size=12, weight='normal')
        else:
            self.font = font.nametofont("jbm")

        self.label_width = 20
        self.input_width = 40

        self.title_container = tk.Frame()
        self.title_label = tk.Label(self.title_container, text="Title:", font=self.font, width=self.label_width, anchor=W)
        self.title_input = tk.Entry(self.title_container, width=self.input_width, borderwidth=1, relief="solid", font=self.font)
        
        self.category_container = tk.Frame()
        self.category_label = tk.Label(self.category_container, text="Category:", font=self.font, width=self.label_width, anchor=W)
        self.category_input = tk.Entry(self.category_container, width=self.input_width, borderwidth=1, relief="solid", font=self.font)

        self.meta_keyword_container = tk.Frame()
        self.meta_keyword_label = tk.Label(self.meta_keyword_container, text="Meta Keyword:", font=self.font, width=self.label_width, anchor=W)
        self.meta_keyword_input = tk.Entry(self.meta_keyword_container, width=self.input_width, borderwidth=1, relief="solid", font=self.font)

        self.meta_description_container = tk.Frame()
        self.meta_description_label = tk.Label(self.meta_description_container, text="Meta Description:", font=self.font, width=self.label_width, anchor=W)
        self.meta_description_input = tk.Entry(self.meta_description_container, width=self.input_width, borderwidth=1, relief="solid", font=self.font)


        self.content_container = tk.Frame()
        self.content_label = tk.Label(self.content_container, text="Content:", font=self.font, width=self.label_width, anchor=W)
        self.content_input = tk.Text(self.content_container, width=100, wrap='none', borderwidth=1, relief="solid", font=self.font)

        self.submit_button = tk.Button(text="Submit", state="disabled", bg="#1e90ff", activebackground="#cd2027", width=self.label_width, borderwidth=0, relief="solid", command=self.sumbit_content)

        self.submit_button.pack(anchor=E, pady=NORMAL_PADDING)
        
        self.title_label.pack(side="left")
        self.title_input.pack(side="right")
        self.title_container.pack(anchor=W, pady=NORMAL_PADDING)

        self.category_label.pack(side="left")
        self.category_input.pack(side="right")
        self.category_container.pack(anchor=W, pady=NORMAL_PADDING)


        self.meta_keyword_label.pack(side="left")
        self.meta_keyword_input.pack(side="right")
        self.meta_keyword_container.pack(anchor=W, pady=NORMAL_PADDING)

        self.meta_description_label.pack(side="left")
        self.meta_description_input.pack(side="right")
        self.meta_description_container.pack(anchor=W, pady=NORMAL_PADDING)

        ys = tk.Scrollbar(self.content_container, orient = 'vertical', command = self.content_input.yview)
        xs = tk.Scrollbar(self.content_container, orient = 'horizontal', command = self.content_input.xview)
        self.content_input['yscrollcommand'] = ys.set
        self.content_input['xscrollcommand'] = xs.set
        ys.pack(side="right", fill="y")
        xs.pack(side="bottom", fill="x")

        self.content_input.see(END)

        self.content_label.pack(side="top", anchor=W, pady=NORMAL_PADDING)
        self.content_input.pack(side="left", fill='both', expand=1)
        self.content_container.pack(anchor=W, fill='both', expand=1)


        # Create the application variable.
        self.title = tk.StringVar()
        self.category = tk.StringVar()
        self.meta_keyword = tk.StringVar()
        self.meta_description = tk.StringVar()


        # Tell the entry widget to watch this variable.
        self.title_input["textvariable"] = self.title
        self.category_input["textvariable"] = self.category
        self.meta_keyword_input["textvariable"] = self.meta_keyword
        self.meta_description_input["textvariable"] = self.meta_description

        self.title.trace_add("write", self.content_submitable)
        self.category.trace_add("write", self.content_submitable)
        self.meta_keyword.trace_add("write", self.content_submitable)
        self.meta_description.trace_add("write", self.content_submitable)
        self.content_input.bind("<KeyPress>", self.content_submitable)


        # Define a callback for when the user hits return.
        # It prints the current value of the variable.

    def content_submitable(self, *args):
        if (len(self.title.get()) > 5) and (len(self.category.get()) > 5) and (len(self.meta_keyword.get()) > 5) and (len(self.meta_description.get()) > 5) and (len(self.content_input.get("1.0", "end")) > 200):
            self.submit_button["state"] = "normal"
        else:
            self.submit_button["state"] = "disabled"

    def sumbit_content(self):
        data = {
            "title": self.title.get(),
            "category": self.category.get(),
            "meta_keyword": self.meta_keyword.get(),
            "meta_descriptiont": self.meta_description.get(),
            "content": self.content_input.get("1.0", "end")
        }
        pprint(data)
        self.submit_button["state"] = "disabled"

root = tk.Tk()
myapp = AllPages(root)
myapp.pack()
myapp.mainloop()
