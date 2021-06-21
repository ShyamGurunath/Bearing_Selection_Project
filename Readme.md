### Bearing Selection System

Check out thr project : https://share.streamlit.io/shyamgurunath/bearing_selection/bearing_class.py

##### Problem Statement
- The issue for engineers in today's technological world is the manual efforts, which makes really tough to pace up the speed within a given time period, specifically when it comes to the bearing selection process. Therefore, there is a lot of manual calculation which needs to be done in selecting a bearing & determining its life expectancy.

##### Solution
- So, we have developed a web application using python & streamlit to automate the boring stuff for engineers and also help them to create great new stuff, without spending too much time in the math behind the scenes. Our Bearing Selection & Life expectancy web app helps users to Select only a Single deep groove ball bearing & know its life expectancy by solving the math behind it. The app expects the user to input their impeller design parameters, choose the diameter, reliability factor, contamination factor & ISO VG (International Standards Organisation Viscosity Grade). After that, you just need to follow the given steps in the app to find the life expectancy of the bearing you’ve selected determining whether the chosen ball bearing is safe for the given impeller design or not.

##### METHODLOGY 

Step 1: Selection of bearing.
Step 2: Calculate the radial load, axial load, and equivalent load.
Step 3: Calculate the bearing Life rating.


##### Step by step procedure

    - User can give the input of impeller in radial and axial load.
    - User can select a bearing of 6th series in first designation.
    - User can mention the estimation year and hours bearing will be run.
    - After given the all data of bearing and then radial load and axial load are calculated.
    - Front bearing is locked after find out the radial and axial load.
    - Then radial load will be changed after front bearing are locked but axial load remains same.
    - To find out the equivalent load of the bearing and then find out the life rating factor of bearing.
    - The life rating is more than the user recommendation bearing will safe other than that that user can change the designation and series of bearing that’s also failed another designation and series are used.
    - If Bearing will be failure after four designation are used. User can change the impeller design or change the diameter of bearing


