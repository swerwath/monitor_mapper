from flask import Markup

CHEM_NAMES = {
    "PM2.5" : "PM<sub>2.5</sub>",
    "SO2" : "SO<sub>2</sub>",
    "NO2" : "NO<sub>2</sub>",
    "OZONE" : "ozone",
}

HEALTH_RISKS = {
    "PM2.5" : "Long-term exposure increases the risk of death from <a href=\"https://www.ncbi.nlm.nih.gov/pubmed/20458016\">heart disease</a> and <a href=\"https://www.ncbi.nlm.nih.gov/pubmed/11879110\">lung cancer</a>. Prolonged exporsure can also lead to <a href=\"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3637008/\">quicker rate of artery thickening</a>, which increases the lifetime risk of developing cardiovascular disease.",
    "SO2" : "Acute short-term exposure to SO<sub>2</sub> can cause breathing difficulty, especially for people with asthma or other vulnerable populations.",
    "NO2" : "Long-term exposure to NO<sub>2</sub> is suspected to contribute to the development of asthma. Acute exposure can cause <a href=\"https://www.epa.gov/no2-pollution/basic-information-about-no2#Effects\" target=\"_blank\">irritation of the lungs and aggravate existing respiratory diseases</a>. NO<sub>2</sub> and other NO<sub>x</sub> compounds also lead to the development of acid rain, which can damage important ecosystems.",
    "OZONE" : "Long-term exposure to ozone increases the chance of lung infection and can <a href=\"https://www.epa.gov/ozone-pollution/health-effects-ozone-pollution\" target=\"_blank\">lead to the development of asthma</a>, especially in children. Acute short-term exposure can trigger asthma attacks or aggravate chronic bronchitis in people who already have those diseases. It can also cause difficulty of breathing and coughing, even in healthy people.",
}

EJ_EVIDENCE = {
    "PM2.5" : "Additionally, PM<sub>2.5</sub> carries environmental justice concerns, since people of color in the US <a href=\"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3137995/\" target=\"_blank\">are more likely to live in areas with high PM<sub>2.5</sub> levels</a>. ",
    "SO2" : "",
    "NO2" : "",
    "OZONE" : "Additionally, ozone carries environmental justice concerns, since people of color in the US <a href=\"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3137995/\" target=\"_blank\">are more likely to live in areas with high ozone levels</a>. ",
}

INFO = {
    "PM2.5" : CHEM_NAMES["PM2.5"] + " refers to particulate matter that has a diameter of less than 2.5 micrometers. These fine particles can be emitted from a number of sources, including power plants, motor vehicles, and forest/residential fires. Because " + CHEM_NAMES["PM2.5"] + " particles are so small, they stay in the air for longer than their heavier counterparts, increasing the odds that a human breathes them in. Once they enter the body, the fine particles can penetrate into the lungs and circulatory system. " + HEALTH_RISKS["PM2.5"] + " " + EJ_EVIDENCE["PM2.5"],
    "SO2" : "Sulfur Dioxide (SO<sub>2</sub>) is an air pollutant released primarily from the burning of fossil fuels at power plants and large industrial facilities. In addition to carrying its own health risks, SO<sub>2</sub> can react with other chemicals in the air to form PM<sub>2.5</sub> particulate matter (see above). " + HEALTH_RISKS["SO2"],
    "NO2" : "Nitrogen Dioxide (NO<sub>2</sub>) is a highly reactive gas emitted primarily from the burning of fuel, both from motor vehicles and power plants. NO<sub>2</sub> is a member of and an indicator for a group of chemicals called nitrogen oxides (NO<sub>x</sub>). " + HEALTH_RISKS["NO2"],
    "OZONE" : "Ozone (O<sub>3</sub>) is a gas found both in the upper atmosphere and at ground level. Ground level ozone is not released directly into the air; rather, it is created as a product of chemical reactions between other air pollutants. These chemical reactions are accelerated on hot days, leading to increased ozone levels. " + HEALTH_RISKS["OZONE"] + " " + EJ_EVIDENCE["OZONE"],
}

LINK = {
    "PM2.5" : "#",
    "SO2" : "#",
    "NO2" : "#",
    "OZONE" : "https://www.epa.gov/ozone-pollution/health-effects-ozone-pollution",
}

DIST_VAR = {
    "PM2.5" : "While PM<sub>2.5</sub> levels at various stations within a single city tend to be highly correlated, <a href=\"https://doi.org/10.1080/10473289.2004.10470919\">there is still variation</a> in measurements.",
    "SO2" : "",
    "NO2" : "Since one of main sources of NO<sub>2</sub> is motor vehicles, <a href=\"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5348563/\">proximity to traffic</a> is a highly predictive of pollution levels. Since motor vehicle traffic varies over time (e.g. \"rush hour\") and air monitoring has low temporal resolution, it's important to keep in mind that NO<sub>2</sub> levels may higher than measured at certain times of day.",
    "OZONE" : "While ozone has <a href=\"https://www.sciencedirect.com/science/article/pii/0004698180900529\">relatively low spatial variation</a> in comparison to other pollutants, its distribution is still heavily dependent on nearby emission sources. If an ozone monitor is upwind of a large emission source, its reading may not be representative of the surrounding area.",
}

def dist_copy(dist, chem):
    copy = "The nearest " + CHEM_NAMES[chem] + " monitoring station is " + ("%.1f" % dist) + " miles away from you"
    if dist < 6.21:
        copy += ", meaning that this monitor is likely close enough to give you an accurate estimate of the air pollution where you are."
    elif dist < 9.3:
        copy += ". While this station is not very close to you, it provides a moderately confident estimate of " + CHEM_NAMES[chem] + " levels near you. However, certain factors like wind and topological features may affect this accuracy."
    else:
        copy += ". Given how far away the monitor is, it's unlikely that its measurements are representative of " + CHEM_NAMES[chem] + " levels near you."

    copy += " " + DIST_VAR[chem]

    return copy

def aqi_copy(aqi, chem_name):
    copy = "The <b>Air Quality Index</b> (AQI) is a number that tells you how much of a certain " + \
    "chemical is in the air, and if that level of pollution carries any potential health concerns. " + \
    "Based on the nearest available monitoring station, the estimated AQI for " + chem_name + " near you is " + str(aqi) + ", "

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
    info = INFO[chem] + "<br /><br />"
    if not chem in nearest_monitors.keys():
        dist = "It looks like <b>there are no " + CHEM_NAMES[chem] + " monitors in your area!</b> Why does this matter? " + \
        " Since you don't live by any " + CHEM_NAMES[chem] + \
        " monitoring stations, there is no way for public health officials to estimate the exposure of people in your community. " + \
        EJ_EVIDENCE[chem] + "If you're concerned about the lack of " + CHEM_NAMES[chem] + " monitoring in your community, you can " + \
        "learn more about " + CHEM_NAMES[chem] + " using the link below, or keep scrolling to get involved with community air monitoring efforts and your local air district."
        read = ""
    else:
        d = nearest_monitors[chem][1]
        aqi = nearest_monitors[chem][0]['AQI']
        dist = dist_copy(d, chem) + " <br /><br />"
        read = aqi_copy(aqi, CHEM_NAMES[chem])

    return (Markup(info), Markup(dist), Markup(read))
