# TV Show and Movie Dashboard

Created an interactive dashboard to provide movies and tv shows information. 
Enter the movie or tv show name in the search bar and it loads all the revlevant tv shows and movies titles with that name n the form of clickable buttons. By clicking on any one of the button loads the deatils of the movie or tv shows like cast, runtime, year, rating, writer, director, plot awards, reviews, episode list etc. 

### Video

![App Screenshot](https://github.com/bharathngowda/tv_show_and_movie_dashboard/blob/main/video.gif)
### Screenshots

![App Screenshot](https://github.com/bharathngowda/tv_show_and_movie_dashboard/blob/main/Screenshots/Picture1.png)

###### Note: The dashboard takes 20-30 secs to load info for the search performed. This is because the Imdb package used scraps the Imdb website realtime and takes time to scrape the info. Also active internet connection is required.

### Programming Language and Packages

The dashboard is built using Python 3.6+.

The main Packages used are -

- Plotly - to make the charts
- Dash - to build the interactive dashboard
- Imdb - to ge movies and tv shows information
- Pandas & Numpy - to process the data and convert it into a format that is required by the dashboard.


### Installation
To run this notebook interactively:

 1. Download this repository in a zip file by clicking on this [link](https://github.com/bharathngowda/tv_show_and_movie_dashboard/archive/refs/heads/main.zip) or execute this from the terminal: 
 `git clone https://github.com/bharathngowda/tv_show_and_movie_dashboard.git`

 2. Install virtualenv.

 3. Navigate to the directory where you unzipped or cloned the repo and create a virtual environment with virtualenv env.

 4. Activate the environment with source env/bin/activate

 5. Install the required dependencies with pip install -r requirements.txt.

 6. Execute `python Movies_TV_Shows_Dashboard.py` from the command line or terminal.

 7. Copy the link `http://localhost:8888` from command prompt and paste in browser and the dashboard will load.

 8. When you're done deactivate the virtual environment with deactivate.`.
