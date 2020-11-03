import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image


@st.cache
def load_data():
    bearing = pd.read_excel("Book2.xlsx")
    bearing.d = bearing.d.fillna(method="ffill")
    bearing.C = bearing.C * 1000
    bearing.C0 = bearing.C0 * 1000
    e = pd.read_excel("equilent_load.xlsx")
    e = e.T.set_index(0).T
    e = e.astype(float)
    return (bearing, e)


def show_data(bearing, e):
    st.title("Bearing Selection & Life Capacity")
    st.subheader("20-100mm Diameter")
    # original data frame
    return st.dataframe(bearing)


def user_input():
    N = st.number_input("What is the N(RPM)?")
    fr = st.number_input("Enter the Radial Load in Newton ")
    fa = st.number_input("Enter the Axial Load in Newton ")
    years_to_run = st.number_input("How much years should the bearing run?  ")
    per_day_run = st.number_input("How much hours should the bearing run? ")
    total_life = per_day_run * years_to_run * 365
    di = {"N": N, "Fr": fr, "Fa": fa, "years_to run": years_to_run,
          "per_day_to_run": per_day_run, "Life": total_life}
    user = pd.DataFrame(di, index=[0])
    user_input = pd.DataFrame(di, index=[0]).T
    user_input.columns = ["InputValues"]
    st.sidebar.markdown("## User Inputs")
    st.sidebar.dataframe(user_input)
    return user


def user_selection(bearing):
    st.sidebar.markdown("## User Selection")
    dia = st.sidebar.selectbox("Select the diameter", bearing.d.unique())
    new_dia_values = bearing[bearing.d == dia]
    l = st.sidebar.selectbox("Select the designation",
                             list(new_dia_values.Designation))
    new_dia_values = new_dia_values[new_dia_values.Designation == l]
    st.sidebar.dataframe(new_dia_values.T)
    return new_dia_values
    # choose_designation = int(input("Select designation from above: "))
    # new_dia_values = bearing[bearing.Designation==choose_designation]


def calculate(bearing, user, new_dia_values, e):
    C0 = tuple(new_dia_values.C0)[0]
    fac0 = (user['Fa'] / C0)[0]
    fac0 = round(fac0, 2)
    st.markdown(f"**Fa/C0 value is {fac0}**")
    fafr = (user['Fa'] / user['Fr'])[0]
    st.markdown(f"**Fa/Fr value is {fafr}**")
    X = float()
    Y = float()
    if st.checkbox("Show Fa/Fr & Fa/C0 Data"):
        st.dataframe(e)
    if fafr <= 0.44:
        X = 1
        Y = 0
        st.markdown(f"**The X & Y Values are {X,Y}**")
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
        st.markdown(f"**The X & Y Values are {X,Y}**")
    return fafr, fac0, X, Y


def equilent_load(X, Y, user, new_dia_values):
    Img = Image.open("cp.jpg")
    st.markdown("### Loading Ratio Graph:")
    st.image(Img, width=850)
    st.info(
        f"Search in x-axis N = {user['N'][0]} & in y-axis Life In Hours = {user['Life'][0]}")
    cpratio = st.number_input("Enter C/P Ratio from the Graph")
    l = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    st.info(f"Factor of Safety for Recprocating Motion {l}")
    s = st.selectbox("Select Fos", l)
    if st.button("calculate EquilentLoad (P)"):
        st.text(f"Factor of Safety for {s}")
        P = ((X * user['Fr'][0]) + (Y * user['Fa'][0])) * s
        cfind = P * cpratio
        st.success(f"#### EquilentLoad P is **{P}** N")
        # C = new_dia_values.C[0]
        # lf = pd.DataFrame({"EquilentLoad(P)": P, "FOS": s,
        #                    "Capacity[Found]": cfind, "CapacityC[Actual]": new_dia_values.C}, index=[0])
        # st.table(lf.T)
        return P, cfind


def design_safe_or_not(cfind, new_dia_values):
    if cfind < float(new_dia_values.C):
        return st.success(f"Bearing is safe since the Capacity[found] = {cfind} is lesser than actual Capacity C[actual] = {float(new_dia_values.C)}")
    elif cfind > float(new_dia_values.C):
        st.warning(
            f"Bearing Design is Not safe since the Capacity[found] = {cfind} is greater than the actual Capacity C[actual] = {float(new_dia_values.C)} ")
        return st.warning(f"Select a greater diamter")


bearing, e = load_data()
show_data(bearing, e)
user = user_input()
new_dia_values = user_selection(bearing)

fafr, fac0, X, Y = calculate(bearing, user, new_dia_values, e)
try:
    p, cfind = equilent_load(X, Y, user, new_dia_values)
    design_safe_or_not(cfind, new_dia_values)
except:
    st.error("Enter the parameters")
