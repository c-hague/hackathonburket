import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime,date
from service.SysCalibration import Calibrate_System
import smtplib
import requests
import time
import random


sysCalibration = Calibrate_System()
#c
# Functions for saving and loading scheduler data
def read_save(f):
    f = open(f, 'r')
    inputs = dict()
    for ln in f.readlines():
        if ln.strip() and not ln.strip().startswith('!'):
            # read the file line by line and only take non-blank lines
            # that don't start with !
            # also throw away comments that use !
            kv = ln.split(':')
            v = kv[1].split('!')[0].strip()
            kv = kv[0].strip()
        inputs[kv] = v
    f.close()
    return inputs
def write_save(f,dict):
    if not f.endswith('.flow'):
        f = f + '.flow'
    f = open(f, 'w')
    for k in dict:
        f.writelines([str(k),' : ',str(dict[k]),'\n'])
    f.close()
def cleanimport(imp):
    imp.pop("total time (sec)")
    x = np.zeros(len(imp))
    y = np.zeros(len(imp))


    for ii,kk in enumerate(imp):
        x[ii] = float(kk)
        y[ii] = float(imp[kk])

    sort_ind = np.argsort(x)
    x = x[sort_ind]
    y = y[sort_ind]
    
    return x,y
def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

#checks to make sure the profile is valid
def checkdatasave(x,y,totaltime, maxflow):
    x = np.array(x)
    y = np.array(y)

    sort_ind = np.argsort(x)
    x = x[sort_ind]
    y = y[sort_ind]

    #initialize the error catches
    err_ind = []
    err = False

    #check to make sure that the volume doesn't go down
    for vv in range(0,len(y)-2):
        if (y[vv] < y[vv+1] and y[vv+1] > y[vv+2]  ):

            #y[vv+1] = (y[vv]+y[vv+2])/2
            err = True

            err_ind.append(x[vv])
   

    #check to see if the flow is possible
    t0 = 0
    vol_start = 0

    errtype = ''
    for vv in range(0,len(y)-1):
        dt = x[vv]*totaltime/100 - t0

        vol_end = vol_start + dt*maxflow
        # st.write("volume end " + str(vol_end))
        # st.write("requested value " + str(y[vv]))

        if (vol_end < y[vv]):
            err = True
            err_ind.append(x[vv])

    
    if err == True:
        errtype = 'Cannot achieve the setpoints ' + str(err_ind)
            

    dataout = {k : v for k,v in zip(x,y)}

    dataout['total time (sec)'] = totaltime
    


    return dataout, err, errtype



#email notifications
def sendemailfinish(sendto):
    gmail_user = 'hackerthonburket@gmail.com'
    gmail_password = 'hackhack'

    sent_from = gmail_user
    to = sendto
    subject = 'Filling Finished'
    body = "'The filling cycle has finished'"

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        st.sidebar.write('Email sent!')


    except:

        st.sidebar.write('Something went wrong...')

def sendemailstart(sendto):
    sendto = sendto.replace(" ","")
    gmail_user = 'hackerthonburket@gmail.com'
    gmail_password = 'hackhack'

    sent_from = gmail_user
    to = [sendto]
    subject = 'Filling Started'
    body = "The filling cycle started at " + str(datetime.today()) 



    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        
        st.sidebar.write('Email sent!')

    except:
        st.sidebar.write('Something went wrong...')



#for the dual axis plotting
def time_percent(x):
    return x
def time_seconds(x):
    return x*total_time/100


#set some header stuff
st.header('Burket Hackathon: Team UNCC')
st.sidebar.header('Flow Scheduler')

#init some variables
max_flow = 10
total_time = 0


#init the buttons
ct_bttn = False
ld_bttn = False


#create job
if (ld_bttn != True):
    #if the load button hasn't been pressed then show the create button
    ct_bttn = st.sidebar.checkbox('Create Job')

    if ct_bttn:
        #init the plot
        fig, ax = plt.subplots()
        total_time = st.sidebar.number_input('Target Time (seconds)')

        #start the dual columns for data entry
        col1, col2 = st.sidebar.columns(2)

        #make two arrays the store the data
        time_percentage = []
        fill_volume = []

        #see how many points the user wants to use
        n = st.sidebar.number_input('Job Sequences',2)

        #iterate through making the input boxes
        for i in range(int(n)):

            if i == n-1 and i != 0:
                x = col1.number_input('% Time',value=100,min_value=100,max_value=100)
                y = col2.number_input('Volume ml',min_value=fill_volume[i-1])
            elif (i == 0):
                x = col1.number_input('% Time' + str(0),min_value=0,max_value=0)
                y = col2.number_input('Volume ml' + str(0),min_value=0,max_value=0)              
            else:
                x = col1.number_input('% Time' + str(i),min_value=time_percentage[i-1])
                y = col2.number_input('Volume ml' + str(i),min_value=fill_volume[i-1])

            #add the values to the storage array
            time_percentage.append(x)
            fill_volume.append(y)

        #check to see if the user has previewed the job
        if st.sidebar.button('Preview Job'):
            #plot some stuff
            ax.plot(time_percentage,fill_volume)
            ax.scatter(time_percentage, fill_volume)
            secax = ax.secondary_xaxis('top', functions=(time_seconds, time_percent))
            secax.set_xlabel('Processing Time (seconds)')
            ax.set_xlabel('% of Target Time')
            ax.set_ylabel('Volume ml')
            st.pyplot(fig)

        #make an enetry box for the user to save the profile into a csv
        filename_save = st.sidebar.text_input("Enter Filename for your job", 'flow_job.flow')
        if st.sidebar.button('Save Job'):
            #feed the data into a checking function for simple profile errors
            [job_data,error_save, error_savetype] = checkdatasave(time_percentage,fill_volume,total_time,max_flow)
            #job_data = dict with organized profile data
            #error_save = trigger if there was an error in the file
            #error_savetype = error message on where the error is
            if error_save == False:
                st.sidebar.write('Flow Profile Saved')
                write_save(filename_save,job_data)
            else:
                st.sidebar.write("Error in data cannot save due to invalid profile.")
                st.sidebar.write(error_savetype)


#load job
if (ct_bttn != True):
    ld_bttn = st.sidebar.checkbox('Load Job')

    if ld_bttn:
        fig, ax = plt.subplots()

        time_percentage = []
        fill_volume = []

        fileloadname = file_selector()
        if st.sidebar.button('Load file function here'):
            
            imp = read_save(fileloadname) # load the data

            tot_time = imp['total time (sec)']

            [x_in,y_in] = cleanimport(imp) #basic clean

            #add the columns and time
            total_time = st.sidebar.number_input('Target Time (seconds)',value=float(tot_time))
            col1, col2 = st.sidebar.columns(2)

            n = len(x_in)

            for i in range(int(n)):

                if (i > 0):

                    x = col1.number_input('% Time' + str(i),value=x_in[i])
                    y = col2.number_input('Volume ml' + str(i),value=y_in[i])

                else:
                    x = col1.number_input('% Time' + str(i),value=x_in[i])
                    y = col2.number_input('Volume ml' + str(i),value=y_in[i])

                #load the data into arrays for use
                time_percentage.append(x)
                fill_volume.append(y)

            #feed the data into a checking function for simple profile errors
            [job_data,error_save, error_savetype] = checkdatasave(time_percentage,fill_volume,total_time,max_flow)
            #job_data = dict with organized profile data
            #error_save = trigger if there was an error in the file
            #error_savetype = error message on where the error is
            if error_save == False:
                st.sidebar.write('No Errors in Profile')
            else:
                st.sidebar.write("Error in data cannot save due to invalid profile.")
                st.sidebar.write(error_savetype)

       # if st.sidebar.button('Preview Job'):
            ax.plot(time_percentage,fill_volume)
            ax.scatter(time_percentage, fill_volume)
            secax = ax.secondary_xaxis('top', functions=(time_seconds, time_percent))
            secax.set_xlabel('Processing Time (seconds)')
            ax.set_xlabel('% of Target Time')
            ax.set_ylabel('Volume ml')
            st.pyplot(fig)

#send email
email_bttn = st.sidebar.checkbox("Send Email When Finished")

if email_bttn:
    email_recp = st.sidebar.text_input("Enter Email for Notificaiton when Finished")

    #if send_bttn:
       # sendemailstart(email_recp)


calibrate_button = st.sidebar.button('Auto Calibrate')
if calibrate_button:
    try:
        response = requests.post('http://localhost:5000/v1/calibrate')
        constants = response.json()
        print('a', constants['a'], 'b', constants['b'])
    except:
        st.sidebar('Error Communicating')

run_button = st.button('Run Job')
if ct_bttn == True or ld_bttn == True:
    run_button = st.sidebar.button('Run Job')
    if run_button:           
        for volume in fill_volume:
            try:
                response = requests.post('http://localhost:5000/v1/dose?amount={0}'.format(volume))
                if not response.ok:
                    st.sidebar.write('Error Communicating')
                actual = response.json()
                print(actual['amount'])
            except:
                st.sidebar.write('Error Communicating')
