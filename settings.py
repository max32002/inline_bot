#!/usr/bin/env python
#encoding=utf-8

try:
    # for Python2
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox

import os
import sys
import json

app_version = "MaxinlineBot (2022.10.22)"

config_filepath = None
config_dict = None

window = None

btn_save = None
btn_exit = None

def load_json():
    # 讀取檔案裡的參數值
    basis = ""
    if hasattr(sys, 'frozen'):
        basis = sys.executable
    else:
        basis = sys.argv[0]
    app_root = os.path.dirname(basis)

    global config_filepath
    config_filepath = os.path.join(app_root, 'settings.json')

    global config_dict
    config_dict = None
    if os.path.isfile(config_filepath):
        with open(config_filepath) as json_data:
            config_dict = json.load(json_data)

def btn_save_clicked():
    btn_save_act()

def btn_save_act(slience_mode=False):

    is_all_data_correct = True

    global config_filepath

    global config_dict
    if not config_dict is None:
        # read user input

        #global combo_homepage
        global txt_homepage

        global txt_adult_picker
        global txt_book_now_time
        global txt_book_now_time_alt

        global txt_user_name
        global combo_user_gender
        global txt_user_phone
        global txt_user_email

        global txt_cardholder_name
        global txt_cardholder_email
        global txt_cc_number
        global txt_cc_exp
        global txt_cc_ccv

        global chk_state_cc_auto_submit

        if is_all_data_correct:
            #if combo_homepage.get().strip()=="":
            if txt_homepage.get().strip()=="":
                is_all_data_correct = False
                messagebox.showerror("Error", "Please enter homepage")
            else:
                #config_dict["homepage"] = combo_homepage.get().strip()
                config_dict["homepage"] = txt_homepage.get().strip()

        if is_all_data_correct:
            if txt_adult_picker.get().strip()=="":
                is_all_data_correct = False
                messagebox.showerror("Error", "Please enter party size")
            else:
                config_dict["adult_picker"] = txt_adult_picker.get().strip()

        if is_all_data_correct:
            if txt_book_now_time.get().strip()=="":
                is_all_data_correct = False
                messagebox.showerror("Error", "Please enter booking time")
            else:
                config_dict["book_now_time"] = txt_book_now_time.get().strip()
    
        if is_all_data_correct:
            if txt_user_name.get().strip()=="":
                is_all_data_correct = False
                messagebox.showerror("Error", "Please enter user name")
            else:
                config_dict["user_name"] = txt_user_name.get().strip()

        if is_all_data_correct:
            if txt_user_phone.get().strip()=="":
                is_all_data_correct = False
                messagebox.showerror("Error", "Please enter user phone")
            else:
                config_dict["user_phone"] = txt_user_phone.get().strip()

        if is_all_data_correct:
            if txt_user_email.get().strip()=="":
                is_all_data_correct = False
                messagebox.showerror("Error", "Please enter user email")
            else:
                config_dict["user_email"] = txt_user_email.get().strip()

        if is_all_data_correct:
            config_dict["book_now_time_alt"] = txt_book_now_time_alt.get().strip()

            config_dict["user_gender"] = combo_user_gender.get().strip()

            config_dict["cardholder_name"] = txt_cardholder_name.get().strip()
            config_dict["cardholder_email"] = txt_cardholder_email.get().strip()
            config_dict["cc_number"] = txt_cc_number.get().strip()
            config_dict["cc_exp"] = txt_cc_exp.get().strip()
            config_dict["cc_ccv"] = txt_cc_ccv.get().strip()

            config_dict["cc_auto_submit"] = bool(chk_state_cc_auto_submit.get())

        # save config.
        if is_all_data_correct:
            import json
            with open(config_filepath, 'w') as outfile:
                json.dump(config_dict, outfile)

            if slience_mode==False:
                messagebox.showinfo("File Save", "Done ^_^")

    return is_all_data_correct

def btn_run_clicked():
    if btn_save_act(slience_mode=True):
        import subprocess
        if hasattr(sys, 'frozen'):
            print("execute in frozen mode")
            import platform

            # check platform here.
            # for windows.
            if platform.system() == 'Darwin':
                 subprocess.Popen("./inline_bot.py", shell=True)
            if platform.system() == 'Windows':
                subprocess.Popen("inline_bot.exe", shell=True)
        else:
            #print("execute in shell mode")
            working_dir = os.path.dirname(os.path.realpath(__file__))
            #print("script path:", working_dir)
            #messagebox.showinfo(title="Debug0", message=working_dir)
            try:
                s=subprocess.Popen(['python3', 'inline_bot.py'], cwd=working_dir)
                #s=subprocess.Popen(['./chrome_tixcraft'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir)
                #s=subprocess.run(['python3', 'chrome_tixcraft.py'], cwd=working_dir)
                #messagebox.showinfo(title="Debug1", message=str(s))
            except Exception as exc:
                try:
                    s=subprocess.Popen(['python', 'inline_bot.py'], cwd=working_dir)
                except Exception as exc:
                    msg=str(exc)
                    messagebox.showinfo(title="Debug2", message=msg)
                    pass


def btn_exit_clicked():
    root.destroy()

# PS: nothing need to do, at current process.
def callbackUserGenderOnChange(event):
    showHideBlocks()

# PS: nothing need to do, at current process.
def callbackHomepageOnChange(event):
    showHideBlocks()

def showHideBlocks(all_layout_visible=False):
    pass

def MainMenu(root):
    global UI_PADDING_X
    UI_PADDING_X = 15
    global UI_PADDING_Y
    UI_PADDING_Y = 10

    homepage_default = u"https://inline.app/"
    homepage_list = (homepage_default
        )

    gender_default = '小姐'
    gender_list = (gender_default, '先生')

    lbl_homepage = None
    lbl_user_id = None
    lbl_user_name = None
    lbl_user_tel = None
    lbl_user_birthday = None
    lbl_user_gender = None
    lbl_visit_time = None
    lbl_dr_name = None

    homepage = None

    adult_picker = ""
    book_now_time = ""
    book_now_time_alt = ""

    user_name = ""
    user_gender = ""
    user_phone = ""
    user_email = ""

    cardholder_name=""
    cardholder_email = ""
    cc_number = ""
    cc_exp = ""
    cc_ccv = ""

    global config_dict
    if not config_dict is None:
        # output config:
        print("homepage", config_dict["homepage"])
        print("adult_picker", config_dict["adult_picker"])
        print("book_now_time", config_dict["book_now_time"])
        print("book_now_time_alt", config_dict["book_now_time_alt"])
        print("user_name", config_dict["user_name"])
        print("user_gender", config_dict["user_gender"])
        print("user_phone", config_dict["user_phone"])
        print("user_email", config_dict["user_email"])

        print("cardholder_name", config_dict["cardholder_name"])
        print("cardholder_email", config_dict["cardholder_email"])
        print("cc_number", config_dict["cc_number"])
        print("cc_exp", config_dict["cc_exp"])
        print("cc_ccv", config_dict["cc_ccv"])

        if 'cc_auto_submit' in config_dict:
            print("cc_auto_submit", config_dict["cc_auto_submit"])

    else:
        print('config is none')
        config_dict = {}
        config_dict["homepage"] = homepage_default
        config_dict["adult_picker"] = ""
        config_dict["book_now_time"] = ""
        config_dict["book_now_time_alt"] = ""
        config_dict["user_name"] = ""
        config_dict["user_gender"] = gender_default
        config_dict["user_phone"] = ""
        config_dict["user_email"] = ""

        config_dict["cardholder_name"] = ""
        config_dict["cardholder_email"] = ""
        config_dict["cc_number"] = ""
        config_dict["cc_exp"] = ""
        config_dict["cc_ccv"] = ""

    # load default values.
    if homepage is None:
        homepage = homepage_default

    if user_gender == "":
        user_gender = gender_default

    # output to GUI.
    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    # first row need padding Y
    lbl_homepage = Label(frame_group_header, text="Homepage", pady = UI_PADDING_Y)
    lbl_homepage.grid(column=0, row=group_row_count, sticky = E)

    '''
    global combo_homepage
    combo_homepage = ttk.Combobox(frame_group_header, state="readonly")
    combo_homepage['values']= homepage_list
    combo_homepage.set(homepage)
    # PS: nothing need to do when on change event at this time.
    combo_homepage.bind("<<ComboboxSelected>>", callbackHomepageOnChange)
    combo_homepage.grid(column=1, row=group_row_count, sticky = W)
    '''

    global txt_homepage
    global txt_homepage_value
    txt_homepage_value = StringVar(frame_group_header, value=config_dict["homepage"])
    txt_homepage = Entry(frame_group_header, width=20, textvariable = txt_homepage_value)
    txt_homepage.grid(column=1, row=group_row_count, sticky = W)

    group_row_count+=1

    # party size
    lbl_adult_picker = Label(frame_group_header, text="Party size")
    lbl_adult_picker.grid(column=0, row=group_row_count, sticky = E)

    global txt_adult_picker
    global txt_adult_picker_value
    txt_adult_picker_value = StringVar(frame_group_header, value=config_dict["adult_picker"])
    txt_adult_picker = Entry(frame_group_header, width=20, textvariable = txt_adult_picker_value)
    txt_adult_picker.grid(column=1, row=group_row_count, sticky = W)

    group_row_count+=1

    # Time
    lbl_book_now_time = Label(frame_group_header, text="Time")
    lbl_book_now_time.grid(column=0, row=group_row_count, sticky = E)

    global txt_book_now_time
    global txt_book_now_time_value
    txt_book_now_time_value = StringVar(frame_group_header, value=config_dict["book_now_time"])
    txt_book_now_time = Entry(frame_group_header, width=20, textvariable = txt_book_now_time_value)
    txt_book_now_time.grid(column=1, row=group_row_count, sticky = W)

    group_row_count+=1

    # Time
    lbl_book_now_time_alt = Label(frame_group_header, text="Time (Alternative)")
    lbl_book_now_time_alt.grid(column=0, row=group_row_count, sticky = E)

    global txt_book_now_time_alt
    global txt_book_now_time_alt_value
    txt_book_now_time_alt_value = StringVar(frame_group_header, value=config_dict["book_now_time_alt"])
    txt_book_now_time_alt = Entry(frame_group_header, width=20, textvariable = txt_book_now_time_alt_value)
    txt_book_now_time_alt.grid(column=1, row=group_row_count, sticky = W)

    group_row_count+=1

    # add first block to UI.
    frame_group_header.grid(column=0, row=row_count, sticky = W, padx=UI_PADDING_X)
    row_count+=1

    '''
    lbl_hr = Label(root, text="")
    lbl_hr.grid(column=0, row=row_count)

    row_count+=1
    '''

    # frame - user profile
    global frame_user_profile
    frame_user_profile = Frame(root)
    user_profile_row_count = 0

    lbl_user_profile = Label(frame_user_profile, text="User Info")
    lbl_user_profile.grid(column=0, row=user_profile_row_count)

    user_profile_row_count+=1

    # User Name
    lbl_user_name = Label(frame_user_profile, text="Name")
    lbl_user_name.grid(column=0, row=user_profile_row_count, sticky = E)

    global txt_user_name
    global txt_user_name_value
    txt_user_name_value = StringVar(frame_user_profile, value=config_dict["user_name"])
    txt_user_name = Entry(frame_user_profile, width=20, textvariable = txt_user_name_value)
    txt_user_name.grid(column=1, row=user_profile_row_count, sticky = W)

    user_profile_row_count+=1

    # User Gender
    lbl_user_gender = Label(frame_user_profile, text="Gender")
    lbl_user_gender.grid(column=0, row=user_profile_row_count, sticky = E)

    global txt_user_gender
    global txt_user_gender_value
    txt_user_gender_value = StringVar(frame_user_profile, value=config_dict["user_name"])
    txt_user_gender = Entry(frame_user_profile, width=20, textvariable = txt_user_name_value)
    txt_user_gender.grid(column=1, row=user_profile_row_count, sticky = W)

    global combo_user_gender
    combo_user_gender = ttk.Combobox(frame_user_profile, state="readonly")
    combo_user_gender['values']= gender_list
    combo_user_gender.set(config_dict["user_gender"])
    # PS: nothing need to do when on change event at this time.
    combo_user_gender.bind("<<ComboboxSelected>>", callbackUserGenderOnChange)
    combo_user_gender.grid(column=1, row=user_profile_row_count, sticky = W)

    user_profile_row_count+=1

    # User Tel
    lbl_user_phone = Label(frame_user_profile, text="Tel")
    lbl_user_phone.grid(column=0, row=user_profile_row_count, sticky = E)

    global txt_user_phone
    global txt_user_phone_value
    txt_user_phone_value = StringVar(frame_user_profile, value=config_dict["user_phone"])
    txt_user_phone = Entry(frame_user_profile, width=20, textvariable = txt_user_phone_value)
    txt_user_phone.grid(column=1, row=user_profile_row_count, sticky = W)

    user_profile_row_count+=1

    # User Email
    lbl_user_email = Label(frame_user_profile, text="Email")
    lbl_user_email.grid(column=0, row=user_profile_row_count, sticky = E)

    global txt_user_email
    global txt_user_email_value
    txt_user_email_value = StringVar(frame_user_profile, value=config_dict["user_email"])
    txt_user_email = Entry(frame_user_profile, width=20, textvariable = txt_user_email_value)
    txt_user_email.grid(column=1, row=user_profile_row_count, sticky = W)

    user_profile_row_count+=1


    # add second block to UI.
    frame_user_profile.grid(column=0, row=row_count, sticky = W, padx=UI_PADDING_X)
    row_count+=1

    '''
    lbl_hr = Label(root, text="")
    lbl_hr.grid(column=0, row=row_count)

    row_count+=1
    '''

    # frame - credit card
    global frame_cc
    frame_cc = Frame(root)
    cc_row_count = 0

    lbl_cc = Label(frame_cc, text="Credit Card Holder")
    lbl_cc.grid(column=0, row=cc_row_count)

    cc_row_count+=1

    lbl_cardholder_name = Label(frame_cc, text="Name")
    lbl_cardholder_name.grid(column=0, row=cc_row_count, sticky = E)

    global txt_cardholder_name
    global txt_cardholder_name_value
    txt_cardholder_name_value = StringVar(frame_cc, value=config_dict["cardholder_name"])
    txt_cardholder_name = Entry(frame_cc, width=20, textvariable = txt_cardholder_name_value)
    txt_cardholder_name.grid(column=1, row=cc_row_count, sticky = W)

    cc_row_count+=1

    lbl_cardholder_email = Label(frame_cc, text="Email")
    lbl_cardholder_email.grid(column=0, row=cc_row_count, sticky = E)

    global txt_cardholder_email
    global txt_cardholder_email_value
    txt_cardholder_email_value = StringVar(frame_cc, value=config_dict["cardholder_email"])
    txt_cardholder_email = Entry(frame_cc, width=20, textvariable = txt_cardholder_email_value)
    txt_cardholder_email.grid(column=1, row=cc_row_count, sticky = W)

    cc_row_count+=1

    lbl_cc_number = Label(frame_cc, text="Number")
    lbl_cc_number.grid(column=0, row=cc_row_count, sticky = E)

    global txt_cc_number
    global txt_cc_number_value
    txt_cc_number_value = StringVar(frame_cc, value=config_dict["cc_number"])
    txt_cc_number = Entry(frame_cc, width=20, textvariable = txt_cc_number_value)
    txt_cc_number.grid(column=1, row=cc_row_count, sticky = W)

    cc_row_count+=1

    lbl_cc_exp = Label(frame_cc, text="Exp (MM/YY)")
    lbl_cc_exp.grid(column=0, row=cc_row_count, sticky = E)

    global txt_cc_exp
    global txt_cc_exp_value
    txt_cc_exp_value = StringVar(frame_cc, value=config_dict["cc_exp"])
    txt_cc_exp = Entry(frame_cc, width=20, textvariable = txt_cc_exp_value)
    txt_cc_exp.grid(column=1, row=cc_row_count, sticky = W)

    cc_row_count+=1

    lbl_cc_ccv = Label(frame_cc, text="ccv")
    lbl_cc_ccv.grid(column=0, row=cc_row_count, sticky = E)

    global txt_cc_ccv
    global txt_cc_ccv_value
    txt_cc_ccv_value = StringVar(frame_cc, value=config_dict["cc_ccv"])
    txt_cc_ccv = Entry(frame_cc, width=20, textvariable = txt_cc_ccv_value)
    txt_cc_ccv.grid(column=1, row=cc_row_count, sticky = W)

    cc_row_count+=1

    cc_auto_submit_local = False
    if 'cc_auto_submit' in config_dict:
        cc_auto_submit_local = config_dict['cc_auto_submit']

    lbl_cc_auto_submit = Label(frame_cc, text="Auto submit")
    lbl_cc_auto_submit.grid(column=0, row=cc_row_count, sticky = E)

    global chk_state_cc_auto_submit
    chk_state_cc_auto_submit = BooleanVar()
    chk_state_cc_auto_submit.set(cc_auto_submit_local)

    global chk_cc_auto_submit
    chk_cc_auto_submit = Checkbutton(frame_cc, text='Enable', variable=chk_state_cc_auto_submit)
    chk_cc_auto_submit.grid(column=1, row=cc_row_count, sticky = W)

    cc_row_count+=1


    # add third block to UI.
    frame_cc.grid(column=0, row=row_count, sticky = W, padx=UI_PADDING_X)
    row_count+=1

    lbl_hr = Label(root, text="")
    lbl_hr.grid(column=0, row=row_count)

    row_count+=1


    frame_action = Frame(root)

    btn_run = ttk.Button(frame_action, text="Run", command=btn_run_clicked)
    btn_run.grid(column=0, row=0)

    btn_save = ttk.Button(frame_action, text="Save", command=btn_save_clicked)
    btn_save.grid(column=1, row=0)

    btn_exit = ttk.Button(frame_action, text="Exit", command=btn_exit_clicked)
    btn_exit.grid(column=2, row=0)

    frame_action.grid(column=0, row=row_count)

def main():
    load_json()

    global root
    root = Tk()
    root.title(app_version)

    #style = ttk.Style(root)
    #style.theme_use('aqua')

    #root.configure(background='lightgray')
    # style configuration
    #style = Style(root)
    #style.configure('TLabel', background='lightgray', foreground='black')
    #style.configure('TFrame', background='lightgray')

    GUI = MainMenu(root)
    GUI_SIZE_WIDTH = 420
    GUI_SIZE_HEIGHT = 510
    GUI_SIZE_MACOS = str(GUI_SIZE_WIDTH) + 'x' + str(GUI_SIZE_HEIGHT)
    GUI_SIZE_WINDOWS=str(GUI_SIZE_WIDTH-60) + 'x' + str(GUI_SIZE_HEIGHT-20)

    GUI_SIZE =GUI_SIZE_MACOS
    import platform
    if platform.system() == 'Windows':
        GUI_SIZE =GUI_SIZE_WINDOWS
    root.geometry(GUI_SIZE)
    root.mainloop()

if __name__ == "__main__":
    main()