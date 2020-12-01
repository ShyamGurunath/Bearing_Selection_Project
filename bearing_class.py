from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import math
import altair as alt
import numpy as np
from PIL import Image

@st.cache()
def load_data():
    bearing = pd.read_excel("Book2.xlsx")
    bearing.d = bearing.d.fillna(method="ffill")
    bearing.C = bearing.C * 1000
    bearing.C0 = bearing.C0 * 1000
    bearing['dia_mean'] = (bearing.d+bearing.D)/2
    cleaniliness  = pd.read_excel("Book1.xlsx")
    askf = pd.read_excel("askf.xlsx")
    askf.columns = ['hcPup',0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.8,1,"un",1.5,2,3,4]
    askf.drop("un",axis=1,inplace=True)
    askf.fillna(0,inplace=True)
    askf = askf.melt(id_vars=['hcPup'], var_name='K', value_name='askf')
    new1_df = pd.read_excel("new1.xlsx",header=1)
    e = pd.read_excel("equilent_load.xlsx")
    e = e.T.set_index(0).T
    e = e.astype(float)
    return (bearing, e,cleaniliness,new1_df,askf)


def show_data(bearing, e):
    # original data frame
    return st.dataframe(bearing)


def user_selection(bearing):
    dia = st.selectbox("Select the diameter", bearing.d.unique())
    new_dia_values = bearing[bearing.d == dia]
    l = st.radio("Select the designation",
                             list(new_dia_values.Designation))
    new_dia_values = new_dia_values[new_dia_values.Designation == l]
    dD_mean = (new_dia_values.d + new_dia_values.D)/2

    st.dataframe(new_dia_values.T)
    # choose_designation = int(input("Select designation from above: "))
    # new_dia_values = bearing[bearing.Designation==choose_designation]
    return new_dia_values,dD_mean


def selection_type():
    iso = pd.read_excel("Book3.xlsx")
    l = st.selectbox("Select the Oil Type",
                             list(iso.ISO))
    value = iso[iso.ISO == l]['Y']
    return st.text(float(value)), float(value)

def find_askf(dD_mean,N,new_df):
    chhosen = new_df[new_df['N']==N]
    dD_mean = round(dD_mean)
    dD_mean = int(dD_mean)
    if dD_mean >= 30 and dD_mean <= 39:
        filter_value = float(chhosen[chhosen.mean_dia.between(30,39)]['new_1'])
        return filter_value
    elif dD_mean >= 40 and dD_mean <= 49:
        filter_value = float(chhosen[chhosen.mean_dia.between(40,49)]['new_1'])
        return filter_value
    elif dD_mean>=50 and dD_mean<=59:
        filter_value = float(chhosen[chhosen.mean_dia.between(50,59)]['new_1'])
        return filter_value
    elif dD_mean>=60 and dD_mean<=69:
        filter_value = float(chhosen[chhosen.mean_dia.between(60,69)]['new_1'])
        return filter_value
    elif dD_mean>=70 and dD_mean<=79:
        filter_value = float(chhosen[chhosen.mean_dia.between(70,79)]['new_1'])
        return filter_value
    elif dD_mean>=80 and dD_mean<=89:
        filter_value = float(chhosen[chhosen.mean_dia.between(80,89)]['new_1'])
        return filter_value
    elif dD_mean>=90 and dD_mean<=99:
        filter_value = float(chhosen[chhosen.mean_dia.between(90,99)]['new_1'])
        return filter_value
    elif dD_mean>=100 and dD_mean<=109:
        filter_value = float(chhosen[chhosen.mean_dia.between(100,109)]['new_1'])
        return filter_value
    elif dD_mean>=110 and dD_mean<=119:
        filter_value = float(chhosen[chhosen.mean_dia.between(110,119)]['new_1'])
        return filter_value
    elif dD_mean>=120 and dD_mean<=12:
        filter_value = float(chhosen[chhosen.mean_dia.between(120,129)]['new_1'])
        return filter_value
    elif dD_mean>=130 and dD_mean<=139:
        filter_value = float(chhosen[chhosen.mean_dia.between(130,139)]['new_1'])
        return filter_value
    elif dD_mean>=140 and dD_mean<=149:
        filter_value = float(chhosen[chhosen.mean_dia.between(140,149)]['new_1'])
        return filter_value
    elif dD_mean>=150 and dD_mean<=159:
        filter_value = float(chhosen[chhosen.mean_dia.between(150,159)]['new_1'])
        return filter_value
    else:
        filter_value = float(chhosen[chhosen.mean_dia.between(160,169)]['new_1'])
        return filter_value


def relaiblity():
    relaiblity_df = pd.read_excel("Book2 1.xlsx")
    l = st.selectbox("Select the Relablity Percent",
                             list(relaiblity_df['Reliability']))
    value = relaiblity_df[relaiblity_df['Reliability'] == l]['a1']
    st.text(float(value))
    return value

def contamination_factor(new_dia_values,cleaniliness):
    if float(new_dia_values['dia_mean']) > 100:
        cleaniliness1 = cleaniliness.loc[:,['CONDTION','nc_dm>100']]
        clean_choose = st.radio("Select the Condition",list(cleaniliness1.CONDTION))
        ηc = cleaniliness1[cleaniliness1.CONDTION == clean_choose]['nc_dm>100']
        st.text(float(ηc))
        return float(ηc)
    elif float(new_dia_values['dia_mean']) < 100:
        cleaniliness1 = cleaniliness.loc[:,['CONDTION','nc_dm<100']]
        clean_choose = st.radio("Select the Condition",list(cleaniliness1.CONDTION))
        ηc = cleaniliness1[cleaniliness1.CONDTION == clean_choose]['nc_dm<100']
        st.text(float(ηc))
        return float(ηc)
    else:
        pass

def find_life_rating(a1,y,y1,ηc,new_dia_values,di,askf,N,user):
    if st.checkbox("Askf Graph:"):
        C = float(new_dia_values['C'])
        P = float(di['P'])
        cp = C/P
        k = y/y1
        ηcpup = ηc * (float(new_dia_values['Pu'])/P)
        data = {"C":C,"P":P,"k":k,"ηcpu/p":ηcpup,"c/p":cp}
        c = alt.Chart(askf).mark_circle().encode(
       x='hcPup', y='askf',color='K',tooltip=['hcPup', 'askf','K'])
        st.info(" Graph Indicates the **askf** values for all **ηcPu/P** with respect to their visocity K! Hover over the Graph & find out the value of askf")
        st.info(f"For ηcpu/p - {ηcpup} on xaxis ,find askf in yaxis by using k - {k} (is colored) ")
        st.altair_chart(c, use_container_width=True)
        st.json(data)
        askf = st.number_input("Enter the value for askf")
        if st.checkbox("Find Life Rating"):
            cp1 = float(pow(cp,3))
            Lnm = a1 * askf * cp1
            Lnmh = float(((pow(10,6))/(60*N))) * Lnm
            data = {"C":C,"P":P,"k":k,"ηcpu/p":ηcpup,"c/p":cp,"askf":askf,"Lnm":float(Lnm),"Lnmh":float(Lnmh)}
            st.json(data)
            if float(user['Life']) < float(data['Lnmh']):
                st.success(f"The design is safe!,Since the Life rating {round(data['Lnmh'],2)} is greater than actual Life {user['Life'][0]}  ")
                st.balloons()
            elif float(user['Life']) > float(data['Lnmh']):
                st.warning(f"The design is not safe!, Since the Since the Life rating {round(data['Lnmh'],2)} is lesser than actual Life {user['Life'][0]}, Try changing the Designation to {[new_dia_values.Designation]}")

            return data



def user_input():
    N = st.selectbox("What is the N(RPM)?", [1500,3000])
    Life = st.number_input("How much life should the bearing withstand?  ")
    # Radial Loading
    Hbep = st.number_input("Enter the Hbep")

    Qbep = st.number_input("Enter the discharge")
    d2 = st.number_input("Enter the d2 (m)")
    b2 = st.number_input("Enter the b2 (m)")
    dwr = st.number_input("Enter dwr (m)")

    dsh = st.number_input("Enter dsh (m)")

    L1 = st.number_input("Enter L1 (m)")
    L2 = st.number_input("Enter L2 (m)")


    gamma = 9.81 * pow(10, 3)
    di = {"N": N, "Life": Life, "Hbep": Hbep,
          "Qbep": Qbep, "d2": d2, "b2": b2, "dwr": dwr, "dsh": dsh, "L1": L1, "L2": L2, "g": 9.81, "gamma": gamma}

    user = pd.DataFrame(di, index=[0])
    user_input = pd.DataFrame(di, index=[0]).T
    user_input.columns = ["InputValues"]
    return user,N



def frfa(user, kr,new_dia_values,ηc):
    Awr = 0.785 * pow(user['dwr'], 2)
    Ash = 0.785 * pow(user['dsh'], 2)
    U2 = (3.14 * user['d2'] * user['N']) / 60
    Uwr = (3.14 * user['dwr'] * user['N']) / 60
    Ush = (3.14 * user['dsh'] * user['N']) / 60

    nh = 0.85
    nh1 = 0.90
    g = 9.81
    Hth = user['Hbep'] / nh
    Hp = nh1 * (1 - ((g * Hth) / (2 * pow(U2, 2)))) * user['Hbep']
    Fa_1 = user['gamma'] * (Awr - Ash)
    fa2 = (((pow(U2, 2)) / g))
    fa3 = ((pow(Uwr, 2)) + (pow(Ush, 2))) / 2
    Fa = Fa_1 * (Hp - (1 / 8) * (fa2 - fa3))
    H0 = 1.17 * user['Hbep']
    gamma = 9.81 * pow(10, 3)
    P0 = gamma * H0
    nsh = float((pow(10, 3)) * (user['N'] / 60) * \
            ((math.sqrt(user['Qbep'] / 1000)) /
             (pow(9.81 * user['Hbep'], 0.75))))
    if (nsh >= 30) and (nsh <= 110):
        kr['check'] = kr['nsh'].apply(lambda x: x - nsh)
        for i, y in enumerate(kr.check):
            if (kr.check[i] < 0) and (kr.check[i + 1] > 0):
                new_kr1 = kr[kr.check == y]
                index = new_kr1.index[0] + 1
                new_kr2 = kr[kr.index == index]
                kr1 = new_kr1.iloc[0][1]
                kr2 = new_kr2.iloc[0][1]
                nsh1 = new_kr1.iloc[0][0]
                nsh2 = new_kr2.iloc[0][0]
                kr_real = kr1 + (((kr1 - kr2) / (nsh1 - nsh2)) * (nsh - nsh1))
                Fr = kr_real * P0 * user['d2'] * user['b2'][0]
                di = {"Fr":Fr,"Fa":Fa}
                C0 = np.array(new_dia_values.C0)[0]
                fac0 = (di['Fa'] / C0)[0]
                fac0 = round(fac0, 2)
                fafr = (di['Fa'] / di['Fr'])[0]
                if fafr <= 0.44:
                    X = 1
                    Y = 0
                elif fafr > 0.44:
                    X = 0.56
                    if fac0 >= e['Fa/C0'][1] and fac0 <= e['Fa/C0'][2]:
                        Y = 1.9
                    elif fac0 >= e['Fa/C0'][2] and fac0 <= e['Fa/C0'][3]:
                        Y = 1.7
                    elif fac0 >= e['Fa/C0'][3] and fac0 <= e['Fa/C0'][4]:
                        Y = 1.5
                    elif fac0 >= e['Fa/C0'][4] and fac0 <= e['Fa/C0'][5]:
                        Y = 1.3
                    elif fac0 >= e['Fa/C0'][5] and fac0 <= e['Fa/C0'][6]:
                        Y = 1.1
                l = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
                s = st.selectbox("Select Fos", l)
                if st.checkbox("Show Fa/Fr & Fa/C0 Data"):
                    st.dataframe(e)
                if st.checkbox("Calculate EquilentLoad (P)"):
                    P = ((X * di['Fr']) + (Y * di['Fa'])) * s
                    Pu = float(new_dia_values['Pu'])
                    st.success(f"#### EquilentLoad P is **{round(P[0],2)}** N")
                    di1 = {"fac0":fac0,"fafr":fafr,"P":P[0],"X":X,"Y":Y,"Fr":Fr[0],"Fa":Fa[0]}
                    st.json(di1)
                    return di1
    else:
        st.warning("The parameters you've entered is not suitable for this program,Please change the paramaters!")




x = st.sidebar.selectbox("Bearing Selction System",['App','About',"Team details"])
if x=="App":
    st.title("Bearing Selection & Life Capacity")
    st.subheader("20-100mm Diameter")
    col1,col2,col3 = st.beta_columns([8,1,7])
    with col3:
        kr = pd.read_excel("kr.xlsx", header=1)
        bearing, e,cleaniliness,new1_df,askf = load_data()
        st.subheader("Select the Oil Type")
        mark, y = selection_type()
        st.subheader("Select the Reliability Factor")
        a1 = relaiblity()
        st.subheader("Selct the bearing Diameter")
        new_dia_values,dD_mean = user_selection(bearing)

        st.subheader("Select Conatmination Factor")
        ηc = contamination_factor(new_dia_values,cleaniliness)



    with col1:
        if st.checkbox("Show SKF bearing data"):
            show_data(bearing, e)
        st.subheader("Design Parameters")
        user,N = user_input()
        st.markdown("## User Inputs")
        st.table(user.T)
    y1 = find_askf(dD_mean,N,new1_df)

    di = frfa(user,kr,new_dia_values,cleaniliness)



    life_rating = find_life_rating(a1,y,y1,ηc,new_dia_values,di,askf,N,user)
elif x=="Team details":
    st.title("Our Team details")
    st.markdown("BEARING Selction system PROJECT REPORT")
    st.markdown("SUBMITTED BY")
    st.markdown("SHYAM GURUNATH.R K-17BAU027")
    st.markdown("DHINAKARAN.M - 18BAU315")
    st.markdown("KESAVAN.A-18BAU326")
    st.subheader("UNDER THE GUIDANCE OF")
    st.markdown("Dr. SR. Sunil Gangolli")
    st.markdown("LECTURER, HEAD OF THE DEPARTMENT/AUTOMOBILE ENGINEERING")
    st.markdown("in partial fulfillment for the award of the degree of")
    st.markdown("BACHELOR OF ENGINEERING In Automobile Engineering ")
    st.markdown("Dr. Mahalingam College of Engineering and Technology Pollachi – 642003 ")
    st.markdown("An Autonomous Institution Affiliated to Anna University")
    st.markdown("Chennai – 600 025 September 2020")
elif x=='About':
    st.title("Bearing Selection System")
    st.markdown("[Project Github Link!](https://github.com/ShyamGurunath/bearing_selection.git)")
    st.subheader("Abstract")
    st.markdown("In a deep groove ball bearing first of all to select a bearing and to find out the radial load, axial load, equivalent load and then find out the life ratting factor of bearing. Designer can design a good life of bearing by using this calculation.")
    st.markdown(" Designer are design a 100% of bearing but only 90% of bearing will be successful and 10% of bearing will be failure. The manufacture recommendation is to design a 100% of bearing to 99% of bearing will be successful to ask to designer. This one not easy for designer it’s very difficult to given output 99% of bearing become succeed and then given to user. The lots of steps involved to calculate and give good reliability given to the user this takes more time. That’s why we are plan to create a software by using python programmed in a method of web application to easy to expand bearing life time.")
    st.markdown("In this project the user can directly use this software. User will install this software and then easily to find out the capacity of bearing by user. That’s the advantage of this software.")
    st.markdown("After software will install by user then user can put all input data of bearing. And then automatically calculated and find out the capacity of bearing for user recommendation.")




