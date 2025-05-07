import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk




class Gallery(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gallery art piece infosystem")
        self.geometry("1920x1080")
        self.attributes("-fullscreen", True)
        self.configure(bg="white")
        self._init_data()

        self.create_styles()
        self.create_widgets()


    def _init_data(self):
        raw_data = [
            ("Monalisa", "Da Vinci", 1503, "Reserved", "Paris",
                "images/mona.png",
                "Portrait of Lisa Gherardini painted by Leonardo da Vinci circa 1503–1506.",
                "Leonardo da Vinci was an Italian polymath of the High Renaissance."),
            ("Starry Night", "Van Gogh", 1889, "For sale", "London",
                "images/starry_night.png",
                "A depiction of the view from the east-facing window of his asylum room.",
                "Vincent van Gogh was a Dutch post-impressionist painter."),
            ("Guernica", "Picasso", 1937, "Not for Sale", "Berlin",
             "images/guernica.png",
             "A depiction of the view from the pierre of a very screaming person.",
             "Piccaso was a cubistic, abstract post-modern artist."),
            ("The Scream", "Picasso", 1893, "Not for Sale", "Oslo",
                "images/Scream.png",
                "A depiction of the view from the pierre of a very screaming person.",
                "Edvard Munch was a  expressionist painter."
             ),
            ("The Anatomy of Painting", "Saville", 2009, "Not for Sale", "Oslo",
             "images/anatomy.png",
             "A depiction of the view from the pierre of a very screaming person.",
             "Edvard Munch was a  expressionist painter."
             ),
            ("Dove of Peace", "Picasso", 1949, "Not for Sale", "Berlin",
             "images/dove.png",
             "A depiction of the view from the pierre of a very screaming person.",
             "Piccaso was a cubistic, abstract post-modern artist."),
            ("women of Avignon", "Picasso", 1907, "Not for Sale", "Madrid",
             "images/avignon.png",
             "A depiction of the view from the pierre of a very screaming person.",
             "Piccaso was a cubistic, abstract post-modern artist."),
            ("Sunset", "Monet", 1867, "Not for Sale", "Paris",
             "images/sunset.png",
             "A depiction of the view from the pierre of a very screaming person.",
             "Edvard Munch was a  expressionist painter."),
            ("Lorem ipsum dolor sit amet, consectetuer", "Lorem ipsum dolor sit amet, consect", 1867, "Not for Sale", "Lorem ipsum dolor sit amet, consectetuer",
             "images/sunset.png",
             "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec qu",
             "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec qu")
        ]

        self.data = []
        self.current_edit_id = None
        self.next_id = 1

        for item in raw_data:
            # pad to length 8
            title, author, year, availability, location, *rest = item
            img_path = rest[0] if len(rest) > 0 else None
            art_info = rest[1] if len(rest) > 1 else ""
            author_info = rest[2] if len(rest) > 2 else ""

            full_entry = (
                self.next_id,
                title, author, year, availability, location,
                img_path, art_info, author_info
            )
            self.data.append(full_entry)
            self.next_id += 1


# validating inputs
    def _is_alpha(self, value):
        return value.isalpha() or value == ""

    def _is_digit(self, value):
        return value.isdigit() or value == ""

    def _validate_text_length(self, value, max_len):
        # delka
        if len(value) > int(max_len):
            return False
        # valid znaky
        for ch in value:
            if not (ch.isalpha() or ch in (" ", "-")):
                return False
        return True

    def _validate_year(self, value):
        return (value.isdigit() or value == "") and len(value) <= 4

    def _limit_text_widget(self, event, widget, max_len):
        content = widget.get("1.0", "end-1c")
        if len(content) > max_len:
            widget.delete(f"1.0 + {max_len}c", "end")


    def create_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("White.TFrame", background="#F0F8FF")
        style.configure("TCombobox",
                        foreground="#2F4F4F",
                        fieldbackground="white",
                        background="white")
        style.map("TCombobox",
                  fieldbackground=[("readonly", "white")],
                  background=[("readonly", "white")])

        style.configure('TNotebook', background='white', borderwidth=0, tabmargins=[10, 5, 10, 0])
        style.configure('TNotebook.Tab',
                        background='lightblue',
                        foreground='white',
                        font=('Helvetica', 13, 'bold'),
                        padding=[10, 10])


        style.map("TNotebook.Tab",
                  background=[("selected", "#F0F8FF")],
                  foreground=[("selected", "#2F4F4F")]
                  )

        style.configure("Treeview",
                        font=("Helvetica", 10 ),
                        rowheight=20)
        style.configure("Treeview.Heading",
                        background="lightblue",
                        foreground="white",
                        borderwidth=4,
                        relief="flat",
                        font=("Helvetica", 13, "bold"))

    def create_widgets(self):

        self.main_frame = tk.Frame(self, bg="white",
                                   highlightbackground="lightblue",
                                  # highlightthickness=6,
                                   highlightcolor="lightblue")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)


        self.create_menu()
        self.create_notebook()

        self.status_bar = tk.Label(self, text="Status bar: active",
                                   bd=1,
                                   relief="sunken",
                                   anchor="center",
                                   bg="lightblue",
                                   font=('Helvetica', 14))
        self.status_bar.pack(side="bottom", fill="both", ipady=10)
        self.status_bar.config(text="No selection")

    def create_menu(self):
        # main menu
        bar_menu = tk.Menu(self,
                           bg="lightblue",
                           fg="#2F4F4F",
                           activebackground="#F0F8FF",
                           activeforeground="#2F4F4F",
                           font=('Helvetica', 11, 'bold'))
        self.config(menu=bar_menu)

        # File
        file_menu = tk.Menu(bar_menu, tearoff=0,
                            bg="lightblue", fg="#2F4F4F",
                            activebackground="#F0F8FF",
                            activeforeground="#2F4F4F",
                           font=('Helvetica', 11, 'bold'))
        file_menu.add_command(
            label="New record",
            command=lambda: self.notebook.select(self.new_record_tab)
        )
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.destroy)
        bar_menu.add_cascade(label="File", menu=file_menu)

        # Edit
        edit_menu = tk.Menu(bar_menu, tearoff=0,
                            bg="lightblue", fg="#2F4F4F",
                            activebackground="#F0F8FF",
                            activeforeground="#2F4F4F",
                           font=('Helvetica', 11, 'bold'))
        edit_menu.add_command(label="Delete", command=self._delete_current)
        bar_menu.add_cascade(label="Edit", menu=edit_menu)

        # About
        about_menu = tk.Menu(bar_menu, tearoff=0,
                             bg="lightblue", fg="#2F4F4F",
                             activebackground="#F0F8FF",
                             activeforeground="#2F4F4F",
                           font=('Helvetica', 11, 'bold'))
        about_menu.add_command(label="About", command=self.show_about)
        bar_menu.add_cascade(label="About", menu=about_menu)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)

        self.overview_tab = ttk.Frame(self.notebook, style="White.TFrame")
        self.search_tab = ttk.Frame(self.notebook, style="White.TFrame")
        self.detail_tab = ttk.Frame(self.notebook, style="White.TFrame")
        self.new_record_tab = ttk.Frame(self.notebook, style="White.TFrame")

        self.notebook.add(self.overview_tab, text="Overview")
        self.notebook.add(self.detail_tab, text="Detail")
        self.notebook.add(self.search_tab, text="Search")
        self.notebook.add(self.new_record_tab, text="New record")

        self.create_overview_tab()
        self.crate_search_tab()
        self.create_new_record_tab()
        self.create_detail_tab()

    def create_overview_tab(self):
        # overview now -> treeView later
        overview_label = tk.Label(self.overview_tab,
                                  text="Catalogue of art",
                                  fg="#696969",
                                  bg="#F0F8FF",
                                  font=('Helvetica', 13))
        overview_label.pack(fill="x", pady=10) # smaz potom pre

        self.overview_tree = ttk.Treeview(self.overview_tab,
                                          columns=("ID", "Title", "Author", "Year", "Availability", "Location"),
                                          show="headings",
                                          height=10
                                          )
        for col in self.overview_tree["columns"]:
            self.overview_tree.heading(col, text=col)
            self.overview_tree.column(col, anchor="center", width=50)

        self.overview_tree.pack(fill="both",
                                expand=True,
                                padx=10,
                                pady=10)


        for row in self.data:
            self.overview_tree.insert("", "end", values=row)

    def _refresh_overview_tree(self):
        for item in self.overview_tree.get_children():
            self.overview_tree.delete(item)
        for row in self.data:
            self.overview_tree.insert("", "end", values=row[:6])

    def crate_search_tab(self):
        search_frame = ttk.Frame(self.search_tab, style="White.TFrame")
        search_frame.pack( padx=10, pady=10)

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)

        # Combobox pro dostupnost
        self.availability_filter = ttk.Combobox(search_frame, state="readonly", width=20)
        self.availability_filter["values"] = ["All", "For sale", "Reserved", "Not for Sale", "Free for display"]
        self.availability_filter.current(0)
        self.availability_filter.pack(side="left", padx=5)

        search_button = tk.Button(search_frame, fg="#2F4F4F", bg="#F0F8FF", text="Search", command=self._perform_search)
        search_button.pack(side="left", padx=5)

        self.search_results = ttk.Treeview(self.search_tab,
                                           columns=("ID", "Title", "Author", "Year", "Availability", "Location"),
                                           show="headings",
                                           height=10)
        self.search_results.pack(fill="both",  expand=True, padx=10, pady=10)

        for col in self.overview_tree["columns"]:
            self.search_results.heading(col, text=col)
            self.search_results.column(col, width=100, anchor="center")

        self.search_results.bind("<<TreeviewSelect>>", self._on_treeview_select)  # -> pak otvre detail -> impl on_search_select

    def _perform_search(self):
        query = self.search_entry.get().lower()
        availability_filter = self.availability_filter.get()

        for item in self.search_results.get_children():
            self.search_results.delete(item)

        for entry in self.data:
            title = entry[1]
            author = entry[2]
            availability = entry[4]

            matches_query = query in title.lower() or query in author.lower()
            matches_filter = (availability_filter == "All") or (availability == availability_filter)

            if matches_query and matches_filter:
                self.search_results.insert("", "end", values=entry[:6])

    def create_new_record_tab(self):
        self.new_record_form = {}
        self.selected_image_path = None

        maxlens = {
            "Title": 40,
            "Author surname": 35,
            "Location": 40,
            "ArtInfo": 200,
            "AuthorInfo": 200,
        }

        wrapper_frame = tk.Frame(self.new_record_tab, bg="#F0F8FF")
        wrapper_frame.pack(fill="both", expand=True, padx=60, pady=60)

        form_frame = tk.Frame(wrapper_frame, bg="#F0F8FF")
        form_frame.grid(row=0, column=0, sticky="nw")

        # canvas zarovnany k poli
        self.new_record_canvas = tk.Canvas(wrapper_frame, width=800, height=600, bg="#F0F8FF", bd=1, relief="solid")
        self.new_record_canvas.grid(row=0, column=1, sticky="nw", padx=(300, 300), pady=(10, 10))

        labels = ["Title", "Author surname", "Year", "Availability", "Location"]
        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, fg="#2F4F4F", bg="#F0F8FF", font=('Helvetica', 12))
            label.grid(row=i, column=0, sticky="e", padx=5, pady=8)

            if label_text in ["Title","Author surname", "Location"]:
                entry = ttk.Entry(form_frame, validate="key", width=40)
                vcmd = (self.register(self._validate_text_length), "%P", str(maxlens[label_text]))
                entry.configure(validatecommand=vcmd)
            elif label_text == "Year":
                entry = ttk.Entry(form_frame, validate="key", width=40)
                entry.configure(validatecommand=(self.register(self._validate_year), "%P"))
            elif label_text == "Availability":
                entry = ttk.Combobox(form_frame, values=["For sale", "Not for sale", "Free for display", "Reserved"],
                                     state="readonly", width=37, style="TCombobox")

            else:
                entry = ttk.Entry(form_frame, width=40)

            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.new_record_form[label_text] = entry

        # Additional info – Art
        art_info_label = tk.Label(form_frame, text="Art Info", fg="#2F4F4F", bg="#F0F8FF", font=('Helvetica', 11))
        art_info_label.grid(row=len(labels), column=0, sticky="ne", padx=5, pady=(15, 5))
        art_info_text = tk.Text(form_frame, width=50, height=4, font=('Helvetica', 10))
        art_info_text.grid(row=len(labels), column=1, padx=5, pady=(15, 5))
        art_info_text.bind(
            "<KeyRelease>",
            lambda e, w=art_info_text, m=maxlens["ArtInfo"]:
            self._limit_text_widget(e, w, m)
        )
        self.new_record_form["ArtInfo"] = art_info_text

        # Additional info – Author
        author_info_label = tk.Label(form_frame, text="Author Info",fg="#2F4F4F", bg="#F0F8FF", font=('Helvetica', 11))
        author_info_label.grid(row=len(labels) + 1, column=0, sticky="ne", padx=5, pady=5)
        author_info_text = tk.Text(form_frame, width=50, height=4, font=('Helvetica', 10))
        author_info_text.grid(row=len(labels) + 1, column=1, padx=5, pady=5)
        author_info_text.bind(
            "<KeyRelease>",
            lambda e, w=author_info_text, m=maxlens["AuthorInfo"]:
            self._limit_text_widget(e, w, m)
        )
        self.new_record_form["AuthorInfo"] = author_info_text

        # Add button
        add_button = tk.Button(form_frame, text="Add", bg="#F0F8FF", fg="#2F4F4F", font=('Helvetica', 11, 'bold'),
                               command=self._add_new_record)
        add_button.grid(row=len(labels) + 2, column=1, sticky="e", padx=5, pady=20)

        # button upload image
        image_button = tk.Button(form_frame, text="Upload image", bg="#F0F8FF", fg="#2F4F4F", font=('Helvetica', 11, 'bold'),
                                 command=self._select_image)
        image_button.grid(row=len(labels) + 2, column=0, sticky="w", padx=5, pady=20)

        # Clear button
        clear_button = tk.Button(form_frame, text="Clear", bg="#F0F8FF", fg="#2F4F4F", font=('Helvetica', 11, 'bold'),
                                 command=self._clear_form)
        clear_button.grid(row=len(labels) + 3, column=1, sticky="e", padx=5, pady=5)

    def _add_new_record(self):
        data = [self.new_record_form[key].get() for key in ["Title", "Author surname", "Year", "Availability", "Location"]]
        art_info = self.new_record_form["ArtInfo"].get("1.0", "end").strip()
        author_info = self.new_record_form["AuthorInfo"].get("1.0", "end").strip()
        image_path = self.selected_image_path

        if self.current_edit_id:
            record_id = self.current_edit_id
            self.data = [e if e[0] != record_id else (record_id, *data, image_path, art_info, author_info) for e in
                         self.data]
            self.current_edit_id = None
            self.status_bar.config(text=f"Updated record ID: {record_id}")
            self._refresh_overview_tree()

            # Vyber dany záznam v treeview
            for item in self.overview_tree.get_children():
                if self.overview_tree.item(item)["values"][0] == record_id:
                    self.overview_tree.selection_set(item)
                    self.overview_tree.focus(item)
                    self._show_detail(next(e for e in self.data if e[0] == record_id))
                    self.notebook.select(self.detail_tab)
                    break

            # erase input fields
            self._clear_form()

        else:
            record_id = self.next_id
            self.next_id += 1
            new_entry = (record_id, *data, image_path, art_info, author_info)
            self.data.append(new_entry)
            self.status_bar.config(text=f"Added: title: {data[0]} (ID: {record_id})")
  
            item_id = self.overview_tree.insert("", "end", values=new_entry[:6])
            self.notebook.select(self.overview_tab)
            self.overview_tree.selection_set(item_id)
            self.overview_tree.focus(item_id)

        self.status_bar.config(text=f"Added: title: {data[0]} (ID: {record_id})")

        # erase input fields
        self._clear_form()




    def _select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if path:
            self.selected_image_path = path
            self.status_bar.config(text=f"Selected image: {path.split('/')[-1]}")

            try:
                canvas_width = 800
                canvas_height = 600

                img = Image.open(path)
                img_ratio = img.width / img.height
                canvas_ratio = canvas_width / canvas_height

                if img_ratio > canvas_ratio:
                    new_width = canvas_width
                    new_height = int(canvas_width / img_ratio)
                else:
                    new_height = canvas_height
                    new_width = int(canvas_height * img_ratio)

                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.new_record_image = ImageTk.PhotoImage(img)
                self.new_record_canvas.delete("all")
                self.new_record_canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.new_record_image)
            except Exception as e:
                self.status_bar.config(text=f"Failed to load image: {e}")
                self.new_record_canvas.delete("all")

    def create_detail_tab(self):
        self.detail_canvas = tk.Canvas(self.detail_tab, width=800, height=600, bg="#F0F8FF")
        self.detail_canvas.pack(pady=20)

        self.detail_title = tk.Label(self.detail_tab, text="", font=('Helvetica', 16, 'bold'), bg="#F0F8FF")
        self.detail_title.pack(pady=5)

        self.detail_author = tk.Label(self.detail_tab, text="", font=('Helvetica', 12), bg="#F0F8FF")
        self.detail_author.pack(pady=5)

        self.detail_art_info = tk.Label(self.detail_tab, text="", wraplength=600, justify="center", bg="#F0F8FF")
        self.detail_art_info.pack(pady=5)

        self.detail_author_info = tk.Label(self.detail_tab, text="", wraplength=600, justify="center", bg="#F0F8FF")
        self.detail_author_info.pack(pady=5)

        self.detail_image = None

        self.overview_tree.bind("<<TreeviewSelect>>", self._on_treeview_select)

        clear_sel_btn = tk.Button(self.detail_tab,
                                  text="Clear selection",
                                  command=self._clear_selection,
                                  bg="#F0F8FF",
                                  fg="#2F4F4F",
                                  font=('Helvetica', 11, 'bold'))
        clear_sel_btn.pack(side="right", padx=10, pady=10)

        modify_btn = tk.Button(self.detail_tab,
                               text="Modify",
                               command=self._modify_current,
                               bg="#F0F8FF",
                               fg="#2F4F4F",
                               font=('Helvetica', 11, 'bold'))
        modify_btn.pack(side="right", padx=10, pady=10)

        delete_btn = tk.Button(self.detail_tab,
                               text="Delete",
                               command=self._delete_current,
                               bg="#F0F8FF",
                               fg="#2F4F4F",
                               font=('Helvetica', 11, 'bold'))
        delete_btn.pack(side="right", padx=20, pady=10)




    def _on_treeview_select(self, event):
        treeview = event.widget
        selected = treeview.selection()
        if not selected:
            self.status_bar.config(text="No selection")
            return
        item = treeview.item(selected[0])
        record_id = item["values"][0]

        for entry in self.data:
            if entry[0] == record_id:
                self._show_detail(entry)
                self.notebook.select(self.detail_tab)
                break

    def _show_detail(self, entry):
        title = entry[1]
        author = entry[2]
        image_path = entry[6]
        art_info = entry[7]
        author_info = entry[8]

        self.detail_title.config(text=f"Title: {title}")
        self.detail_author.config(text=f"Author: {author}")
        self.detail_art_info.config(text=f"About the Art:\n{art_info}")
        self.detail_author_info.config(text=f"About the Author:\n{author_info}")

        self.status_bar.config(text=f"Selected: ID:{entry[0]} – {title}")

        if image_path:
            try:
                canvas_width = 800
                canvas_height = 600

                img = Image.open(image_path)
                img_ratio = img.width / img.height
                canvas_ratio = canvas_width / canvas_height

                if img_ratio > canvas_ratio:
                    new_width = canvas_width
                    new_height = int(canvas_width / img_ratio)
                else:
                    new_height = canvas_height
                    new_width = int(canvas_height * img_ratio)

                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.detail_image = ImageTk.PhotoImage(img)
                self.detail_canvas.delete("all")
                self.detail_canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.detail_image)
            except Exception as e:
                self.status_bar.config(text=f"Failed to load image: {e}")
                self.detail_canvas.delete("all")
        else:
            self.detail_canvas.delete("all")

    def _clear_form(self):
        for key in ["Title", "Author surname", "Year", "Availability", "Location"]:
            if key in self.new_record_form:
                widget = self.new_record_form[key]
                if isinstance(widget, ttk.Combobox):
                    widget.set("")  # nebo widget.set("For sale") jako vychozi
                else:
                    widget.delete(0, "end")

        self.new_record_form["ArtInfo"].delete("1.0", "end")
        self.new_record_form["AuthorInfo"].delete("1.0", "end")
        self.selected_image_path = None
        self.new_record_canvas.delete("all")

    def _clear_selection(self):
        for tree in [self.overview_tree, self.search_results]:
            tree.selection_remove(tree.selection())
        for lbl in (self.detail_title,
                    self.detail_author,
                    self.detail_art_info,
                    self.detail_author_info):
            lbl.config(text="")
        self.detail_canvas.delete("all")
        self.status_bar.config(text="No selection")
        self.notebook.select(self.overview_tab)

    def show_about(self):
        messagebox.showinfo(
            "About Gallery",
            "Gallery Art Piece Infosystem\n"
            "Verze 1.0\n"
            "© 2025 Premysl Polas\n\n"
            "Jednoducha aplikace pro evidenci uměleckych del."
        )

    def _modify_current(self):
        sel = self.overview_tree.selection()
        if not sel:
            self.status_bar.config(text="No record selected to modify")
            return

        item = sel[0]
        record_id = self.overview_tree.item(item)["values"][0]
        entry = next((e for e in self.data if e[0] == record_id), None)

        if entry:
            self.current_edit_id = record_id
            keys = ["Title", "Author surname", "Year", "Availability", "Location"]
            for i, key in enumerate(keys, start=1):
                widget = self.new_record_form[key]
                if isinstance(widget, ttk.Combobox):
                    widget.set(entry[i])
                else:
                    widget.delete(0, "end")
                    widget.insert(0, entry[i])

            self.new_record_form["ArtInfo"].delete("1.0", "end")
            self.new_record_form["ArtInfo"].insert("1.0", entry[7])

            self.new_record_form["AuthorInfo"].delete("1.0", "end")
            self.new_record_form["AuthorInfo"].insert("1.0", entry[8])

            self.selected_image_path = entry[6]

            # Přepni na New record tab
            self.notebook.select(self.new_record_tab)

            # Zobraz obrázek
            if self.selected_image_path:
                try:
                    canvas_width = 800
                    canvas_height = 600
                    img = Image.open(self.selected_image_path)
                    img_ratio = img.width / img.height
                    canvas_ratio = canvas_width / canvas_height

                    if img_ratio > canvas_ratio:
                        new_width = canvas_width
                        new_height = int(canvas_width / img_ratio)
                    else:
                        new_height = canvas_height
                        new_width = int(canvas_height * img_ratio)

                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    self.new_record_image = ImageTk.PhotoImage(img)
                    self.new_record_canvas.delete("all")
                    self.new_record_canvas.create_image(canvas_width // 2, canvas_height // 2,
                                                        image=self.new_record_image)
                except Exception as e:
                    self.status_bar.config(text=f"Image preview failed: {e}")
                    self.new_record_canvas.delete("all")

    def _delete_current(self):
        sel = self.overview_tree.selection()
        if not sel:
            self.status_bar.config(text="No record selected to delete")
            return

        item = sel[0]
        record_id = self.overview_tree.item(item)["values"][0]
        self.overview_tree.delete(item)
        self.data = [e for e in self.data if e[0] != record_id]

        for tv in (self.overview_tree, getattr(self, 'search_results', None)):
            if tv:
                tv.selection_remove(tv.selection())

        self.detail_canvas.delete("all")
        for lbl in (self.detail_title,
                    self.detail_author,
                    self.detail_art_info,
                    self.detail_author_info):
            lbl.config(text="")

        self.status_bar.config(text=f"Deleted record ID:{record_id}")


if __name__=="__main__":
    app = Gallery()
    app.mainloop()