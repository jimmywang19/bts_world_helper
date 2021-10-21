import shelve
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("BTS Mini-Tool v2.0")
window.iconbitmap("bts.ico")


def create_window():
    x = window.winfo_x()
    y = window.winfo_y()

    new_win = Toplevel(window)
    new_win.iconbitmap("bts.ico")
    new_win.geometry("+%d+%d" % (x + 500, y))

    return new_win


def close_window():
    window.destroy()


def print_cards(lb):
    lb.delete(0, END)
    # Insert cards into list box
    shelf = shelve.open("shelf_file")
    in_list = 0
    #         print(entry_box.get())
    for card in sorted(shelf):
        lb.insert(END, card)
        lb.insert(END, "Empathy : {}".format(shelf[card]['empathy']))
        lb.insert(END, "Passion : {}".format(shelf[card]['passion']))
        lb.insert(END, "Stamina : {}".format(shelf[card]['stamina']))
        lb.insert(END, "Wisdom : {}".format(shelf[card]['wisdom']))
        lb.insert(END, "\n")
        in_list += 1
    shelf.close()

    shelf = shelve.open('agency_stats')
    for card in sorted(shelf):
        lb.insert(END, card)
        lb.insert(END, "Empathy : {}".format(shelf[card]['empathy']))
        lb.insert(END, "Passion : {}".format(shelf[card]['passion']))
        lb.insert(END, "Stamina : {}".format(shelf[card]['stamina']))
        lb.insert(END, "Wisdom : {}".format(shelf[card]['wisdom']))
        lb.insert(END, "\n")
    shelf.close()

    num_cards_label.config(text="Number of cards: {}".format(in_list))


def set_info():
    stats_dict = {}
    name = name_entry.get()
    empathy = empathy_entry.get()
    passion = passion_entry.get()
    stamina = stamina_entry.get()
    wisdom = wisdom_entry.get()
    affinity = affinity_entry.get()

    if ((name_entry.get() != "") and
            (empathy_entry.get() != "") and
            (passion_entry.get() != "") and
            (stamina_entry.get() != "") and
            (wisdom_entry.get() != "") and
            (affinity_entry.get() != "")):
        stats_dict["empathy"] = empathy
        stats_dict["passion"] = passion
        stats_dict["stamina"] = stamina
        stats_dict["wisdom"] = wisdom
        stats_dict["type"] = affinity

        shelf = shelve.open('shelf_file')
        shelf[name] = stats_dict
        shelf.close()
        # Clear entries after submitting
        name_entry.delete(0, END)
        empathy_entry.delete(0, END)
        passion_entry.delete(0, END)
        stamina_entry.delete(0, END)
        wisdom_entry.delete(0, END)
        affinity_entry.delete(0, END)
    else:
        messagebox.showinfo("Error", "Please fill out all the boxes")


def add_edit_card():
    global name_entry, empathy_entry, passion_entry, stamina_entry, wisdom_entry, affinity_entry

    new_win = create_window()
    name_entry = Entry(new_win)
    empathy_entry = Entry(new_win)
    passion_entry = Entry(new_win)
    stamina_entry = Entry(new_win)
    wisdom_entry = Entry(new_win)
    affinity_entry = Entry(new_win)

    name_label = Label(new_win, text="Enter new card name ")
    empathy_label = Label(new_win, text="Empathy: ")
    passion_label = Label(new_win, text="Passion: ")
    stamina_label = Label(new_win, text="Stamina: ")
    wisdom_label = Label(new_win, text="Wisdom: ")
    affinity_label = Label(new_win, text="Affinity: ")

    submit_button = Button(new_win, text="Submit", borderwidth=1, relief="solid", command=set_info)

    name_label.grid(row=0, column=1, columnspan=2, pady=10)
    name_entry.grid(row=0, column=2, columnspan=3, pady=10)

    empathy_label.grid(row=1, column=1, pady=(0, 10))
    empathy_entry.grid(row=1, column=2, padx=(0, 20), pady=(0, 10))
    passion_label.grid(row=1, column=3, pady=(0, 10))
    passion_entry.grid(row=1, column=4, padx=(0, 20), pady=(0, 10))
    stamina_label.grid(row=2, column=1, pady=(0, 10))
    stamina_entry.grid(row=2, column=2, padx=(0, 20), pady=(0, 10))
    wisdom_label.grid(row=2, column=3, pady=(0, 10))
    wisdom_entry.grid(row=2, column=4, padx=(0, 20), pady=(0, 10))
    affinity_label.grid(row=3, column=1, columnspan=2, pady=10)
    affinity_entry.grid(row=3, column=2, columnspan=3, pady=10)

    submit_button.grid(row=4, column=2, padx=(0, 20), pady=(0, 10), columnspan=3, sticky="ew")


def display_card_list_box(lb, entry_box):
    lb.delete(0, END)
    if entry_box.get() == "":
        lb.insert(END, "Please enter card name into the search bar")
        num_cards_label.config(text="Number of cards: 0")
    else:
        # Insert cards into list box
        shelf = shelve.open("shelf_file")
        in_list = 0
        #         print(entry_box.get())
        for card in sorted(shelf):
            if entry_box.get().lower() in card.lower():
                lb.insert(END, card)
                lb.insert(END, "Empathy : {}".format(shelf[card]['empathy']))
                lb.insert(END, "Passion : {}".format(shelf[card]['passion']))
                lb.insert(END, "Stamina : {}".format(shelf[card]['stamina']))
                lb.insert(END, "Wisdom : {}".format(shelf[card]['wisdom']))
                lb.insert(END, "\n")
                in_list += 1
        shelf.close()

        num_cards_label.config(text="Number of cards: {}".format(in_list))

        if in_list == 0:
            lb.insert(END, "Sorry the item is not in the list")


def delete_card(lb, dele):
    if lb.size() == 0 and dele.get() == "":
        lb.delete(0, END)
        lb.insert(END, "There is nothing to delete")
    else:
        index = lb.get(0, "end").index(lb.get(ANCHOR))
        shelf = shelve.open('shelf_file')
        if index % 6 == 0:
            del (shelf[lb.get(lb.curselection())])
            lb.delete(index, index + 5)
        else:
            messagebox.showinfo("Error",
                                "Please click the NAME of the card (NOT the empathy, passion, stamina, wisdom)")
        shelf.close()


def add_agency(em, pas, stam, wisd):
    stats_dict = {}
    empathy = em.get()
    passion = pas.get()
    stamina = stam.get()
    wisdom = wisd.get()

    if ((empathy != "") and
            (passion != "") and
            (stamina != "") and
            (wisdom != "")):
        stats_dict["empathy"] = empathy
        stats_dict["passion"] = passion
        stats_dict["stamina"] = stamina
        stats_dict["wisdom"] = wisdom

        shelf = shelve.open('agency_stats')
        shelf["Group Stats"] = stats_dict
        shelf.close()
    else:
        messagebox.showinfo("Error", "Please fill out all the boxes")

    em.delete(0, END)
    pas.delete(0, END)
    stam.delete(0, END)
    wisd.delete(0, END)


def agency_display():
    new_win = create_window()
    # Top frame
    top_frame = Frame(new_win)
    top_frame.pack()
    # Bottom frame
    bottom_frame = Frame(new_win)
    bottom_frame.pack(pady=(0, 10))

    # Labels
    text_label = Label(top_frame, text="Please enter your Agency Stats")
    empathy_label = Label(top_frame, text="Empathy : ")
    passion_label = Label(top_frame, text="Passion : ")
    stamina_label = Label(bottom_frame, text="Stamina : ")
    wisdom_label = Label(bottom_frame, text="Wisdom : ")

    # Entries
    empathy_entry = Entry(top_frame)
    passion_entry = Entry(top_frame)
    stamina_entry = Entry(bottom_frame)
    wisdom_entry = Entry(bottom_frame)

    submit_button = Button(new_win, text="Submit", width=25, borderwidth=1, relief="solid"
                           , command=lambda: add_agency(empathy_entry, passion_entry, stamina_entry, wisdom_entry))

    text_label.pack(pady=10)
    empathy_label.pack(side=LEFT, padx=10, pady=10)
    empathy_entry.pack(side=LEFT, padx=(0, 10), pady=10)
    passion_label.pack(side=LEFT, padx=10, pady=10)
    passion_entry.pack(side=LEFT, padx=(5, 20), pady=10)
    stamina_label.pack(side=LEFT, padx=10, pady=10)
    stamina_entry.pack(side=LEFT, padx=(5, 10), pady=10)
    wisdom_label.pack(side=LEFT, padx=10, pady=10)
    wisdom_entry.pack(side=LEFT, padx=(0, 20), pady=10)
    submit_button.pack(side=BOTTOM, pady=10)


def calc_score(em, pas, stam, wisd, chpt, story):
    global best_card_win
    try:
        best_card_win.deiconify()
    except:
        best_card_win = create_window()
        best_card_win.geometry("750x225")

    shelf = shelve.open('shelf_file')
    score_dict = {}
    score_list = []
    num = 0
    if story.lower() == "bts":
        for card in shelf:
            num += 1
            total = 0
            total += int(int(shelf[card]["empathy"]) * float(em))
            total += int(int(shelf[card]["passion"]) * float(pas))
            total += int(int(shelf[card]["stamina"]) * float(stam))
            total += int(int(shelf[card]["wisdom"]) * float(wisd))
            score_dict[card] = total
            score_list.append(total)
    else:
        for card in shelf:
            if ((story.lower() in card.lower().split()) or (
                    (story.lower() == "jhope") and ("j-hope" in card.lower().split()))
                    or ((story.lower() == "jungkook") and ("jk" in card.lower().split()))):
                num += 1
                total = 0
                total += int(int(shelf[card]["empathy"]) * float(em))
                total += int(int(shelf[card]["passion"]) * float(pas))
                total += int(int(shelf[card]["stamina"]) * float(stam))
                total += int(int(shelf[card]["wisdom"]) * float(wisd))
                score_dict[card] = total
                score_list.append(total)

    #         print(card, "---", total)
    shelf.close()

    sorted_dict = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    #   print(sorted_dict)
    level = chpt.split("-")
    #     print(level)
    if story.lower() == "bts":
        if level[0] == "1" and (int(level[1]) < 10):
            highest_score = sorted_dict[0][1]
            highest_card = sorted_dict[0][0]

        elif (level[0] == "1" and (int(level[1]) >= 10) or level[0] == "2"):
            score1 = sorted_dict[0][1]
            card1 = sorted_dict[0][0]
            score2 = sorted_dict[1][1]
            card2 = sorted_dict[1][0]
            #       print("Score 1 : ", score1, " Score 2 : ", score2)
            highest_score = score1 + score2
            highest_card = card1 + " // " + card2
    else:
        if level[0] == "1":
            highest_score = sorted_dict[0][1]
            highest_card = sorted_dict[0][0]

        elif level[0] == "2":
            score1 = sorted_dict[0][1]
            card1 = sorted_dict[0][0]
            score2 = sorted_dict[1][1]
            card2 = sorted_dict[1][0]
            #       print("Score 1 : ", score1, " Score 2 : ", score2)
            highest_score = score1 + score2
            highest_card = card1 + " // " + card2

    if level[0] == "3" or level[0] == "4":
        score1 = sorted_dict[0][1]
        card1 = sorted_dict[0][0]
        score2 = sorted_dict[1][1]
        card2 = sorted_dict[1][0]
        score3 = sorted_dict[2][1]
        card3 = sorted_dict[2][0]
        #       print("Score 1 : ", score1, " Score 2 : ", score2)
        highest_score = score1 + score2 + score3
        highest_card = card1 + " // " + card2 + " // " + card3
    elif level[0] == "5" or level[0] == "6":
        score1 = sorted_dict[0][1]
        card1 = sorted_dict[0][0]
        score2 = sorted_dict[1][1]
        card2 = sorted_dict[1][0]
        score3 = sorted_dict[2][1]
        card3 = sorted_dict[2][0]
        score4 = sorted_dict[3][1]
        card4 = sorted_dict[3][0]
        #       print("Score 1 : ", score1, " Score 2 : ", score2)
        highest_score = score1 + score2 + score3 + score4
        highest_card = card1 + " // " + card2 + " // " + card3 + " // " + card4
    elif level[0] == "7":
        score1 = sorted_dict[0][1]
        card1 = sorted_dict[0][0]
        score2 = sorted_dict[1][1]
        card2 = sorted_dict[1][0]
        score3 = sorted_dict[2][1]
        card3 = sorted_dict[2][0]
        score4 = sorted_dict[3][1]
        card4 = sorted_dict[3][0]
        score5 = sorted_dict[4][1]
        card5 = sorted_dict[4][0]
        highest_score = score1 + score2 + score3 + score4 + score5
        highest_card = (card1 + " // " + card2 + " // " + card3 + " // " + card4
                        + " // " + card5)
    agency = shelve.open("agency_stats")
    for card in agency:
        highest_score += int(int(agency[card]["empathy"]) * float(em))
        highest_score += int(int(agency[card]["passion"]) * float(pas))
        highest_score += int(int(agency[card]["stamina"]) * float(stam))
        highest_score += int(int(agency[card]["wisdom"]) * float(wisd))
    #     print(highest_card, "-----", highest_score)
    #             print(num)
    agency.close()

    best_card_display(best_card_win, highest_card, highest_score)


def best_card_display(win, best_card, best_score):
    # Display chosen card at bottom
    for item in win.grid_slaves():
        if int(item.grid_info()["row"]) > 0:
            item.grid_forget()

    shelf = shelve.open("shelf_file")
    cards = best_card.split(" // ")
    card_column = 0
    #     for widget in win.winfo_children():
    #         widget.destroy()

    chosen_label = Label(win, text="CHOOSE THESE CARDS FOR HIGHEST SCORE\n\n {}".format(best_score))
    chosen_label.grid(row=0, column=0, columnspan=6, pady=(20, 30), sticky="nsew")
    chosen_label.config(font=("Arial", 12))

    Grid.rowconfigure(win, 0, weight=1)
    Grid.columnconfigure(win, 0, weight=1)

    for card in cards:
        name = Label(win, text=card)
        empathy = Label(win, text="Empathy : {}".format(shelf[card]["empathy"]))
        passion = Label(win, text="Passion : {}".format(shelf[card]["passion"]))
        stamina = Label(win, text="Stamina : {}".format(shelf[card]["stamina"]))
        wisdom = Label(win, text="Wisdom : {}".format(shelf[card]["wisdom"]))

        name.grid(row=1, column=card_column, ipadx=50, sticky="nsew")
        empathy.grid(row=2, column=card_column, sticky="nsew")
        passion.grid(row=3, column=card_column, sticky="nsew")
        stamina.grid(row=4, column=card_column, sticky="nsew")
        wisdom.grid(row=5, column=card_column, sticky="nsew")
        card_column += 1
    shelf.close()

    for x in range(6):
        Grid.columnconfigure(win, x, weight=1)
    for y in range(6):
        Grid.rowconfigure(win, y, weight=1)


def another_story_display(win, lvl_l, lvl_m, story):
    for widget in win.winfo_children():
        if widget.winfo_class() == "Frame":
            widget.destroy()

    top_frame = Frame(win)
    top_frame.pack()
    Grid.rowconfigure(win, 0, weight=1)
    Grid.columnconfigure(win, 0, weight=1)

    story_label = Label(top_frame, text="Story : {}".format(story.upper()))
    story_label.grid(row=0, column=0, columnspan=15, pady=10, sticky="nsew")

    chapter = 1
    level = 0
    total = 0

    for i in range(len(lvl_l)):
        if (lvl_l[i] == " "):
            level = 0
            chapter += 1
            continue
        else:
            btn = Button(top_frame, text=lvl_l[i], padx=20, pady=20
                         , command=lambda i=i: calc_score(lvl_m[i][0], lvl_m[i][1], lvl_m[i][2]
                                                          , lvl_m[i][3], lvl_l[i], story))
            btn.grid(column=level, row=chapter, sticky="nsew")
            level += 1
        total += 1

    for x in range(15):
        Grid.columnconfigure(top_frame, x, weight=1)
    for y in range(8):
        Grid.rowconfigure(top_frame, y, weight=1)


def level_display():
    new_win = create_window()

    another_story = Menu(new_win)
    new_win.config(menu=another_story)

    rm = Menu(another_story)
    another_story.add_command(label="RM", command=lambda: another_story_display(new_win, rm_l, rm_m, "rm"))

    jin = Menu(another_story)
    another_story.add_command(label="JIN", command=lambda: another_story_display(new_win, jin_l, jin_m, "jin"))

    suga = Menu(another_story)
    another_story.add_command(label="SUGA", command=lambda: another_story_display(new_win, suga_l, suga_m, "suga"))

    jhope = Menu(another_story)
    another_story.add_command(label="JHOPE", command=lambda: another_story_display(new_win, jhope_l, jhope_m, "jhope"))

    jimin = Menu(another_story)
    another_story.add_command(label="JIMIN", command=lambda: another_story_display(new_win, jimin_l, jimin_m, "jimin"))

    v = Menu(another_story)
    another_story.add_command(label="V", command=lambda: another_story_display(new_win, v_l, v_m, "v"))

    jungkook = Menu(another_story)
    another_story.add_command(label="Jungkook", command=lambda: another_story_display(new_win, jk_l, jk_m, "jungkook"))

    bts = Menu(another_story)
    another_story.add_command(label="BTS", command=lambda: another_story_display(new_win, bts_l, bts_m, "bts"))

    top_frame = Frame(new_win)
    top_frame.pack()
    Grid.rowconfigure(new_win, 0, weight=1)
    Grid.columnconfigure(new_win, 0, weight=1)

    story_label = Label(top_frame, text="Story : BTS World")
    story_label.grid(row=0, column=5, columnspan=5, pady=10, sticky="nsew")

    chapter = 1
    level = 0
    total = 0

    for i in range(len(bts_l)):
        if (bts_l[i] == " "):
            level = 0
            chapter += 1
            continue
        else:
            btn = Button(top_frame, text=bts_l[i], padx=20, pady=20
                         , command=lambda i=i: calc_score(bts_m[i][0], bts_m[i][1], bts_m[i][2]
                                                          , bts_m[i][3], bts_l[i], "bts"))
            btn.grid(column=level, row=chapter, sticky="nsew")
            level += 1
        total += 1

    for x in range(15):
        Grid.columnconfigure(top_frame, x, weight=1)
    for y in range(8):
        Grid.rowconfigure(top_frame, y, weight=1)


bts_l = ["1-2", "1-4", "1-6", "1-8", "1-10", "1-12", "1-14", "1-17", "1-18", "1-20"
    , " ", "2-2", "2-4", "2-5", "2-7", "2-8", "2-10", "2-12", "2-15", "2-17", "2-19"
    , " ", "3-1", "3-2", "3-5", "3-6", "3-8", "3-10", "3-11", "3-13", "3-14", "3-16"
    , "3-17", "3-19", " ", "4-1", "4-2", "4-4", "4-5", "4-6", "4-8", "4-10"
    , "4-11", "4-12", "4-14", "4-16", "4-18", "4-20", " ", "5-1", "5-2", "5-4", "5-5"
    , "5-7", "5-8", "5-9", "5-11", "5-12", "5-14", "5-16", "5-18", "5-19", "5-20"
    , " ", "6-1", "6-2", "6-4", "6-5", "6-7", "6-8", "6-9", "6-11", "6-12", "6-14"
    , "6-15", "6-17", "6-18", "6-19", " ", "7-2", "7-3", "7-4", "7-6", "7-7", "7-8"
    , "7-10", "7-11", "7-13", "7-14", "7-15", "7-17", "7-19"]
bts_m = [[1, 1.5, 1, 1], [1, 1, 1.5, 1], [1.5, 1, 1, 1], [1, 1.5, 1.5, 1]
    , [1, 1.5, 1, 1.5], [1.5, 1, 1, 1.5], [1.5, 1.5, 1, 1], [1.5, 1, 1.5, 1]
    , [1, 1.5, 1.5, 1], [1.5, 1, 1, 1.5], [], [1.8, 1, 0.5, 1.5], [1, 1.5, 1.8, 0.5]
    , [1.8, 0.5, 1.5, 1], [1.5, 1, 0.5, 1.8], [0.5, 1.8, 1, 1.5], [1.8, 0.5, 1, 1.5]
    , [1.5, 1.8, 1, 0.5], [1.5, 1, 0.5, 1.8], [0.5, 1, 1.8, 1.5], [1, 1.8, 1.5, 0.5]
    , [], [0.5, 1.5, 1.8, 0.8], [1.8, 1.5, 0.5, 0.8], [1.8, 0.5, 1.5, 0.8], [1.5, 0.8, 0.5, 1.8]
    , [0.5, 1.5, 0.8, 1.8], [1.8, 0.5, 0.8, 1.5], [0.5, 0.8, 1.8, 1.5], [1.5, 1.8, 0.8, 0.5]
    , [0.5, 1.5, 1.8, 0.8], [0.8, 0.5, 1.5, 1.8], [1.5, 1.8, 0.8, 0.5], [0.5, 1.5, 1.8, 0.8]
    , [], [0.5, 2, 1.5, 0.5], [2, 0.5, 0.5, 1.5], [0.5, 1.5, 0.5, 2], [0.5, 1.5, 2, 0.5]
    , [0.5, 1.5, 0.5, 2], [2, 0.5, 1.5, 0.5], [0.5, 2, 0.5, 1.5], [1.5, 0.5, 2, 0.5]
    , [0.5, 1.5, 0.5, 2], [0.5, 0.5, 1.5, 2], [2, 1.5, 0.5, 0.5], [1.5, 0.5, 0.5, 2]
    , [0.5, 2, 1.5, 0.5], [], [2, 0.3, 0.7, 1.5], [1.5, 2, 0.3, 0.7], [1.5, 0.7, 2, 0.3]
    , [0.3, 1.5, 0.7, 2], [2, 0.3, 1.5, 0.7], [0.3, 0.7, 2, 1.5], [1.5, 0.3, 0.7, 2]
    , [0.7, 2, 0.3, 1.5], [0.3, 1.5, 2, 0.7], [2, 0.7, 1.5, 0.3], [0.7, 0.3, 1.5, 2]
    , [1.5, 2, 0.3, 0.7], [0.3, 1.5, 0.7, 2], [0.7, 0.3, 2, 1.5], [], [2, 0.5, 1.5, 0.5]
    , [1.5, 0.5, 0.5, 2], [0.5, 2, 1.5, 0.5], [1.5, 0.5, 2, 0.5], [2, 0.5, 0.5, 1.5]
    , [1.5, 2, 0.5, 0.5], [1.5, 0.5, 2, 0.5], [0.5, 1.5, 0.5, 2], [0.5, 2, 0.5, 1.5]
    , [0.5, 0.5, 2, 1.5], [2, 0.5, 1.5, 0.5], [1.5, 2, 0.5, 0.5], [1.5, 0.5, 2, 0.5]
    , [0.5, 1.5, 0.5, 2], [], [2.2, 1.8, 0.3, 0.2], [0.2, 1.8, 0.3, 2.2], [1.8, 0.2, 0.3, 2.2]
    , [2.2, 0.3, 0.2, 1.8], [0.2, 2.2, 0.3, 1.8], [0.3, 0.2, 1.8, 2.2], [0.2, 0.3, 2.2, 1.8]
    , [1.8, 2.2, 0.2, 0.3], [0.3, 0.2, 1.8, 2.2], [1.8, 0.3, 2.2, 0.2], [0.2, 1.8, 2.2, 0.3]
    , [0.3, 1.8, 2.2, 0.2], [2.2, 0.2, 1.8, 0.3]]

rm_l = ["1-3", "1-5", "1-7", "1-9", "1-11", " ", "2-2", "2-4", "2-6", "2-9"
    , "2-11", " ", "3-2", "3-4", "3-6", "3-8", "3-11", " ", "4-2", "4-4"
    , "4-6", "4-9", "4-11", " ", "5-1", "5-3", "5-5", "5-7", "5-10"]
rm_m = [[1.5, 0.3, 2, 0.3, 1], [2, 1.5, 0.3, 0.3, 1], [0.3, 0.3, 1.5, 2, 1]
    , [0.3, 2, 0.3, 1.5, 1], [1.5, 0.3, 2, 0.3, 1], [], [2, 1.7, 0.1, 0.3, 2]
    , [0.3, 0.1, 1.7, 2, 2], [0.1, 1.7, 2, 0.3, 2], [0.3, 2, 0.1, 1.7, 2]
    , [0.3, 0.1, 1.7, 2, 2], [], [2, 0.2, 1.8, 0.2, 3], [0.2, 2, 1.8, 0.2, 3]
    , [1.8, 0.2, 0.2, 2, 3], [0.2, 2, 0.2, 1.8, 3], [0.2, 1.8, 2, 0.2], []
    , [1.8, 2, 0.2, 0.1, 4], [1.8, 0.2, 0.1, 2, 4], [0.2, 1.8, 2, 0.1, 4]
    , [0.1, 2, 0.2, 1.8, 4], [2, 0.1, 1.8, 0.2, 4], [], [0.1, 0.1, 2, 2, 5]
    , [2, 0.1, 0.1, 2, 5], [0.1, 2, 0.1, 2, 5], [0.1, 2, 2, 0.1, 5], [2, 0.1, 0.1, 2, 5]]

jin_l = ["1-2", "1-4", "1-7", "1-9", "1-12", " ", "2-2", "2-5", "2-7", "2-9"
    , "2-11", " ", "3-1", "3-3", "3-5", "3-7", "3-10", " ", "4-1", "4-4"
    , "4-6", "4-9", "4-12", " ", "5-2", "5-4", "5-6", "5-8", "5-10"]
jin_m = [[2, 0.3, 0.3, 1.5], [0.3, 2, 0.3, 1.5], [1.5, 0.3, 2, 0.3], [0.3, 1.5, 0.3, 2]
    , [0.3, 2, 1.5, 0.3], [], [0.3, 1.7, 0.1, 2], [0.1, 0.3, 1.7, 2]
    , [0.3, 2, 0.1, 1.7], [1.7, 0.1, 0.3, 2], [2, 0.3, 1.7, 0.1], []
    , [2, 0.2, 0.2, 1.8], [0.2, 2, 1.8, 0.2], [2, 1.8, 0.2, 0.2], [1.8, 0.2, 2, 0.2]
    , [0.2, 1.8, 2, 0.2, 3], [], [2, 0.2, 1.8, 0.1], [1.8, 2, 0.1, 0.2], [1.8, 0.2, 2, 0.1]
    , [0.2, 0.1, 1.8, 2], [2, 1.8, 0.1, 0.2], [], [0.1, 0.1, 2, 2], [0.1, 2, 2, 0.1]
    , [0.1, 2, 0.1, 2], [0.1, 0.1, 2, 2], [0.1, 2, 2, 0.1]]

suga_l = ["1-2", "1-5", "1-8", "1-10", "1-12", " ", "2-3", "2-5", "2-7", "2-9"
    , "2-11", " ", "3-1", "3-3", "3-6", "3-8", "3-10", " ", "4-1", "4-5"
    , "4-7", "4-9", "4-12", " ", "5-3", "5-5", "5-7", "5-9", "5-12"]
suga_m = [[0.3, 0.3, 1.5, 2], [2, 0.3, 0.3, 1.5], [0.3, 2, 1.5, 0.3]
    , [2, 0.3, 0.3, 1.5], [1.5, 0.3, 2, 0.3], [], [2, 1.7, 0.1, 0.3]
    , [0.1, 2, 0.3, 1.7], [1.7, 0.3, 0.1, 2], [0.3, 1.7, 2, 0.1]
    , [2, 0.1, 0.3, 1.7], [], [0.2, 2, 1.8, 0.2], [1.8, 0.2, 0.2, 2]
    , [0.2, 2, 1.8, 0.2], [2, 0.2, 1.8, 0.2], [1.8, 0.2, 0.2, 2], []
    , [1.8, 2, 0.2, 0.1], [0.1, 0.2, 2, 1.8], [0.2, 2, 1.8, 0.1]
    , [2, 0.1, 1.8, 0.2], [0.2, 1.8, 0.1, 2], [], [2, 0.1, 2, 0.1]
    , [2, 2, 0.1, 0.1], [0.1, 2, 0.1, 2], [0.1, 0.1, 2, 2], [0.1, 2, 2, 0.1]]

jhope_l = ["1-3", "1-5", "1-7", "1-9", "1-11", " ", "2-2", "2-4", "2-6", "2-10"
    , "2-12", " ", "3-3", "3-5", "3-7", "3-9", "3-11", " ", "4-2", "4-4"
    , "4-7", "4-9", "4-11", " ", "5-3", "5-6", "5-8", "5-10", "5-12"]
jhope_m = [[0.3, 0.3, 1.5, 2], [1.5, 0.3, 2, 0.3], [2, 1.5, 0.3, 0.3], [0.3, 0.3, 2, 1.5]
    , [2, 1.5, 0.3, 0.3], [], [0.1, 2, 0.3, 1.7], [0.3, 0.1, 2, 1.7]
    , [2, 1.7, 0.1, 0.3], [1.7, 0.3, 0.1, 2], [1.7, 2, 0.3, 0.1], []
    , [0.2, 0.2, 2, 1.8], [2, 0.2, 1.8, 0.2], [0.2, 0.2, 1.8, 2]
    , [0.2, 1.8, 2, 0.2], [1.8, 2, 0.2, 0.2], [], [0.1, 0.2, 1.8, 2]
    , [1.8, 0.1, 2, 0.2], [0.2, 2, 1.8, 0.1], [0.1, 1.8, 0.2, 2]
    , [2, 0.2, 0.1, 1.8], [], [0.1, 2, 2, 0.1], [2, 2, 0.1, 0.1]
    , [2, 0.1, 2, 0.1], [0.1, 2, 0.1, 2], [0.1, 0.1, 2, 2]]

jimin_l = ["1-2", "1-5", "1-7", "1-9", "1-11", " ", "2-1", "2-4", "2-7", "2-9"
    , "2-11", " ", "3-1", "3-3", "3-5", "3-9", "3-11", " ", "4-2", "4-4"
    , "4-7", "4-9", "4-11", " ", "5-1", "5-3", "5-6", "5-8", "5-11"]
jimin_m = [[0.3, 1.5, 2, 0.3], [0.3, 1.5, 0.3, 2], [2, 0.3, 1.5, 0.3]
    , [0.3, 2, 0.3, 1.5], [1.5, 0.3, 2, 0.3], [], [0.1, 2, 1.7, 0.3]
    , [0.3, 1.7, 0.3, 2], [0.1, 0.3, 2, 1.7], [2, 0.3, 1.7, 0.1]
    , [0.3, 2, 1.7, 0.1], [], [0.2, 1.8, 0.2, 2], [2, 0.2, 0.2, 1.8]
    , [1.8, 0.2, 2, 0.2], [2, 0.2, 0.2, 1.8], [0.2, 0.2, 1.8, 2]
    , [], [1.8, 0.2, 2, 0.1], [0.1, 2, 1.8, 0.2], [1.8, 0.1, 0.2, 2]
    , [0.2, 2, 0.1, 1.8], [2, 0.1, 0.2, 1.8], [], [2, 2, 0.1, 0.1]
    , [2, 0.1, 2, 0.1], [0.1, 2, 0.1, 2], [0.1, 2, 2, 0.1], [2, 0.1, 0.1, 2]]

v_l = ["1-2", "1-5", "1-7", "1-10", "1-12", " ", "2-2", "2-4", "2-6", "2-8", "2-10"
    , " ", "3-1", "3-5", "3-7", "3-9", "3-11", " ", "4-2", "4-4", "4-6", "4-8"
    , "4-10", " ", "5-1", "5-5", "5-7", "5-9", "5-11", " ", "6-2", "6-5", "6-7"
    , "6-9", "6-11"]
v_m = [[0.3, 1.5, 0.3, 2], [0.3, 2, 1.5, 0.3], [2, 0.3, 0.3, 1.5], [1.5, 0.3, 2, 0.3]
    , [1.5, 2, 0.3, 0.3], [], [0.1, 0.3, 2, 1.7], [0.3, 2, 1.7, 0.1], [2, 0.1, 1.7, 0.3]
    , [0.1, 1.7, 0.3, 2], [0.1, 0.3, 2, 1.7], [], [1.8, 0.2, 2, 0.2]
    , [2, 1.8, 0.2, 0.2], [0.2, 2, 0.2, 1.8], [2, 1.8, 0.2, 0.2], [0.2, 0.2, 1.8, 2]
    , [], [1.8, 0.2, 2, 0.1], [1.8, 0.2, 0.1, 2], [0.1, 0.2, 2, 1.8]
    , [0.1, 2, 1.8, 0.2], [0.2, 1.8, 0.1, 2], [], [2, 0.1, 2, 0.1]
    , [2, 0.1, 0.1, 2], [0.1, 2, 2, 0.1], [0.1, 0.1, 2, 2], [0.1, 2, 0.1, 2], []
    , [2, 2, 0.05, 0.2], [0.05, 2, 0.2, 2], [2, 0.2, 0.05, 2], [2, 2, 0.2, 0.05]
    , [2, 0.05, 2, 0.2]]

jk_l = ["1-2", "1-4", "1-6", "1-9", "1-11", " ", "2-3", "2-5", "2-8", "2-10"
    , "2-12", " ", "3-2", "3-4", "3-7", "3-9", "3-11", " ", "4-1", "4-3"
    , "4-6", "4-8", "4-11", " ", "5-1", "5-4", "5-7", "5-9", "5-11", " "
    , "6-1", "6-3", "6-5", "6-9", "6-11"]
jk_m = [[0.3, 2, 0.3, 1.5], [1.5, 0.3, 0.3, 2], [0.3, 1.5, 2, 0.3]
    , [2, 0.3, 1.5, 0.3], [0.3, 2, 0.3, 1.5], [], [0.3, 0.1, 1.7, 2]
    , [1.7, 2, 0.1, 0.3], [0.1, 1.7, 0.3, 2], [2, 0.3, 0.1, 1.7]
    , [0.3, 1.7, 2, 0.1], [], [0.2, 0.2, 2, 1.8], [2, 1.8, 0.2, 0.2]
    , [0.2, 2, 0.2, 1.8], [2, 1.8, 0.2, 0.2], [1.8, 0.2, 2, 0.2], []
    , [0.1, 2, 0.2, 1.8], [2, 0.2, 0.1, 1.8], [0.2, 0.1, 1.8, 2]
    , [1.8, 0.2, 2, 0.1], [1.8, 2, 0.1, 0.2], [], [0.1, 2, 2, 0.1]
    , [2, 0.1, 2, 0.1], [2, 2, 0.1, 0.1], [0.1, 0.1, 2, 2]
    , [0.1, 2, 0.1, 2], [], [2, 0.2, 2, 0.05], [0.05, 2, 2, 0.2]
    , [0.2, 0.05, 2, 2], [2, 0.2, 0.05, 2], [2, 0.05, 2, 0.2]]

beach_m = [[0.9, 0.9, 1.1, 1.1], [0.9, 1.1, 0.9, 1.1], [1.1, 0.9, 0.9, 1.1], [1.1, 1.1, 0.9, 0.9], [0.9, 0.9, 1.1, 1.1]]


def event_score():
    new_win = create_window()

    top_frame = Frame(new_win)
    top_frame.pack()
    Grid.rowconfigure(new_win, 0, weight=1)
    Grid.columnconfigure(new_win, 0, weight=1)

    story_label = Label(top_frame, text="Event : Chuseok")
    story_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")
    level = 0
    total = 0

    for i in range(5):
        btn = Button(top_frame, text="Stage {}".format(i + 2), padx=20, pady=20
                     , command=lambda i=i: calc_score(beach_m[i][0], beach_m[i][1], beach_m[i][2]
                                                      , beach_m[i][3], "3", "bts"))
        btn.grid(column=level, row=1, sticky="nsew")
        level += 1
        total += 1

    for x in range(5):
        Grid.columnconfigure(top_frame, x, weight=1)
    for y in range(1):
        Grid.rowconfigure(top_frame, y, weight=1)


Grid.rowconfigure(window, 0, weight=1)
Grid.columnconfigure(window, 0, weight=1)

for x in range(5):
    Grid.columnconfigure(window, x, weight=1)

for y in range(10):
    Grid.rowconfigure(window, y, weight=1)

# BTS World Label
search_label = Label(window, text="BTS World Helper\n\n Enter card name to search for below")
search_label.grid(row=0, column=0, columnspan=5, sticky="nsew")

# Search Entry
card_text = StringVar()
card_text.trace("w", lambda name, index, mode, card_text=card_text: display_card_list_box(list1, card_entry))

card_entry = Entry(window, textvariable=card_text)
card_entry.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=20, pady=20)

# Number of cards matching search criteria
num_cards_label = Label(window, text="No cards yet. Please search first.", pady=10)
num_cards_label.grid(row=2, column=0, columnspan=3, sticky='nsew')

# Define Listbox
list1 = Listbox(window, height=6, width=35)
list1.grid(row=3, column=0, rowspan=6, columnspan=3, sticky="nsew", padx=(10, 0))

# Attach Scrollbar to the list
scrollbar = Scrollbar(window)
scrollbar.grid(row=3, column=3, rowspan=6, sticky="nsw")

list1.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list1.yview)

# Define buttons
b1 = Button(window, text="Print All Cards", command=lambda x=list1: print_cards(x))
b1.grid(row=3, column=4, sticky='nsew', padx=(10, 0))

b2 = Button(window, text="Add/Change Card", command=add_edit_card)
b2.grid(row=4, column=4, sticky='nsew', padx=(10, 0))

b3 = Button(window, text="Delete Card", command=lambda x=list1: delete_card(x, card_entry))
b3.grid(row=5, column=4, sticky='nsew', padx=(10, 0))

b4 = Button(window, text="Add/Change Agency", command=agency_display)
b4.grid(row=6, column=4, sticky='nsew', padx=(10, 0))

b5 = Button(window, text="Calculate Total Score", command=level_display)
b5.grid(row=7, column=4, sticky='nsew', padx=(10, 0))

b6 = Button(window, text="Chuseok Event Calculate Score", command=event_score)
b6.grid(row=8, column=4, sticky='nsew', padx=(10, 0))

b7 = Button(window, text="Quit", command=close_window)
b7.grid(row=9, column=4, sticky='nsew', padx=(10, 0))

window.mainloop()
