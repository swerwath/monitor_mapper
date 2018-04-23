from flask import Markup

CHEM_NAMES = {
    "PM2.5" : "PM<sub>2.5</sub>",
    "SO2" : "SO<sub>2</sub>",
    "NO2" : "NO<sub>2</sub>",
    "OZONE" : "ozone",
}

HEALTH_RISKS = {
    "PM2.5" : "Long-term exposure increases the risk of death from <a href=\"https://www.ncbi.nlm.nih.gov/pubmed/20458016\">heart disease</a> and <a href=\"https://www.ncbi.nlm.nih.gov/pubmed/11879110\">lung cancer</a>. Prolonged exporsure can also lead to <a href=\"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3637008/\">quicker rate of artery thickening</a>, which increases the lifetime risk of developing cardiovascular disease.",
    "SO2" : "Health risk sentence.",
    "NO2" : "Health risk sentence.",
    "OZONE" : "Health risk sentence.",
}

INFO = {
    "PM2.5" : CHEM_NAMES["PM2.5"] + " refers to particulate matter that has a diameter of less than 2.5 micrometers. These fine particles can be emitted from a number of sources, including power plants, motor vehicles, and forest/residential fires. Because " + CHEM_NAMES["PM2.5"] + " particles are so small, they stay in the air for longer than their heavier counterparts, increasing the odds that a human breathes them in. Once they enter the body, the fine particles can penetrate into the lungs and circulatory system. " + HEALTH_RISKS["PM2.5"],
    "SO2" : "GENERAL INFO",
    "NO2" : "GENERAL INFO",
    "OZONE" : "GENERAL INFO",
}

EJ_EVIDENCE = {
    "PM2.5" : "EJ sentence.",
    "SO2" : "",
    "NO2" : "",
    "OZONE" : "EJ Sentence.",
}

LINK = {
    "PM2.5" : "#",
    "SO2" : "#",
    "NO2" : "#",
    "OZONE" : "#",
}

DIST_VAR = {
    "PM2.5" : "While PM<sub>2.5</sub> levels at various stations within a single city tend to be highly correlated, <a href=\"https://doi.org/10.1080/10473289.2004.10470919\">there is still a degree of variation</a> in measurements.",
    "SO2" : "",
    "NO2" : "Since one of main sources of NO<sub>2</sub> is motor vehicles, <a href=\"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5348563/\">proximity to traffic</a> is a highly predictive of pollution levels. Since motor vehivle traffic varies over time (e.g. \"rush hour\") and air monitoring has low temporal resolution, it's important to keep in mind that NO<sub>2</sub> levels may higher than measured at certain times of day.",
    "OZONE" : "While ozone has <a href=\"https://www.sciencedirect.com/science/article/pii/0004698180900529\">relatively low spatial variation</a> in comparison to other pollutants, its distribution is still heavily dependent on nearby emission sources. If an ozone monitor is upwind of a large emission source, its reading may not be representative of the surrounding area.",
}

def dist_copy(dist, chem):
    copy = "The nearest " + CHEM_NAMES[chem] + " monitoring station is " + ("%.1f" % dist) + " miles away from you. "
    if dist < 6.21:
        copy += "While all forms of air pollution have high variability, this monitor is likely close enough to give you an accurate estimate of the air pollution where you are."
    elif dist < 9.3:
        copy += "While this station is not extremely close to you, it provides a moderately confident estimate of " + CHEM_NAMES[chem] + " levels near you. However, certain factors like wind and topological features may affect this accuracy."
    else:
        copy += "Given how far away the monitor is, it's unlikely that its measurements are representative of " + CHEM_NAMES[chem] + " levels near you."

    copy += " " + DIST_VAR[chem]

    return copy

def aqi_copy(aqi, chem_name):
    copy = "The <b>Air Quality Index</b> (AQI) is a number that tells you how much of a certain " + \
    "chemical is in the air, and if that level of pollution carries any potential health concerns. " + \
    "Based on the nearest availible monitoring station, the estimated AQI for " + chem_name + " near you is " + str(aqi) + ", "

    if aqi < 51:
        copy += "which the EPA classifies as <font color=\"green\">good</font>. This means that levels of " + chem_name + " are low, and air pollution poses little to no health risks for long periods of exposure."
    elif aqi < 101:
        copy += "which the EPA classifies as <font color=\"orange\">moderate</font>. This means that levels of " + chem_name + " are within regulatory limits, but a very small number of sensitive people may experience health effects."
    elif aqi < 151:
        copy += "which the EPA classifies as <font color=\"red\">unhealthy for sensitive groups</font>. This means that levels of " + chem_name + " are at high levels. People with heart or lung disease, children, and older adults may begin to experience greater health risk."
    else:
        copy += "which the EPA classifies as <font color=\"maroon\">very unhealthy</font>. This means that levels of " + chem_name + " are at very high levels. All people may begin to experience health effects, and members of sensitive groups may experience very serious health risks."

    copy += " For more information on the Air Quality Index, click <a href=\"https://airnow.gov/index.cfm?action=aqibasics.aqi\" target=\"_blank\">here</a>."

    return copy

def get_copy(chem, nearest_monitors):
    copy = INFO[chem] + "<br /><br />"
    if not chem in nearest_monitors.keys():
        copy += "It looks like <b>there are no " + CHEM_NAMES[chem] + " monitors in your area!</b> Why does this matter? " + \
        HEALTH_RISKS[chem] + " Since you don't live by any " + CHEM_NAMES[chem] + \
        " monitoring stations, there is no way for public health officials to estimate the exposure of people in your community. " + \
        EJ_EVIDENCE[chem] + " If you're concerned about the lack of " + CHEM_NAMES[chem] + " monitoring in your community, you can " + \
        "learn more about " + CHEM_NAMES[chem] + " <a href=\"" + LINK[chem] + "\" target=\"_blank\">here</a>, or keep scrolling to get involved " + \
        "with community air monitoring efforts and your local air district."
    else:
        dist = nearest_monitors[chem][1]
        aqi = nearest_monitors[chem][0]['AQI']
        copy += dist_copy(dist, chem) + " <br /><br />"
        copy += aqi_copy(aqi, CHEM_NAMES[chem])

    return Markup(copy)
