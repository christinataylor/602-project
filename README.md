# Semester Project Description

User agents are short strings browsers or applications send to web server to identify themselves - for example, what platform or device is used, what the OS or browser is. The device data is of keen interest to my employer and clients, as it helps analyze ads impressions distribution, monitor usage of network, and target device types accordingly. For this project, I took 300 user agent strings with the most number of ad impressions (sorted in descending order) from the ad server. See query.csv for raw input. 

My program uses two methods - 1) Python's built-in user_agents library, and 2) WURFL, ScientiaMobile's cloud-based device detection service to parse user agent strings. The output are two excel files that contain the raw user agent strings, associated volume of ads impressions, whether the user agent is mobile, tablet, desktop based, or a web crawler, as well as the devices' capabilities (such as brand and family). See ua_map.py for the script. 

I created Tableau visualizations to compare the results. I then made the business case to use WURFL for its accuracy and performance at reasonable cost. Based on WURFL's output, I plotted ad volume by platform, device, and by device within platform. See ua_analysis.pdf for the Tableau export. 

Required packages: user_agents, wurfl-cloud and its API key
To run the program, type the following on the command line: python ua_map.py filecache.conf
