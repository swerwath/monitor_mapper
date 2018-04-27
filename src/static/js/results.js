var map;

function initMap() {
  var center = {lat: lat, lng: long};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: center
  });

  var userLocationIcon = {
    path: "M0-48c-9.8 0-17.7 7.8-17.7 17.4 0 15.5 17.7 30.6 17.7 30.6s17.7-15.4 17.7-30.6c0-9.6-7.9-17.4-17.7-17.4z",
    fillColor: "#0000FF",
    fillOpacity: .9,
    scale: .6,
    origin: new google.maps.Point(0,0), // origin
    anchor: new google.maps.Point(20, 40) // anchor
  };
  var userLocationMarker = new google.maps.Marker({
    position: center,
    icon: userLocationIcon,
    map: map
  });

  constructMonitorMarkerSets(m);
  constructFacilityMarkerSets(f);
  setMarkerSetVisible("PM2.5", monitorMarkerSets);
  setMapCaptionChemical("PM<sub>2.5</sub>");

  legend = document.getElementById("map-caption");
  map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(legend);

}


function getColor(aqi) {
  if (aqi < 51) {
    return 'green';
  }
  if (aqi < 101) {
    return 'orange';
  }
  if (aqi < 151) {
    return 'red';
  }
  return 'maroon';
}

function getDistColor(dist) {
  if (dist < 6.21) {
    return 'green';
  }
  if (dist < 9.3) {
    return 'orange';
  }

  return 'red';
}

function getText(aqi) {
  if (aqi < 51) {
    return 'Good';
  }
  if (aqi < 101) {
    return 'Moderate';
  }
  if (aqi < 151) {
    return 'Unhealthy for Sensitive Groups';
  }
  return 'Unhealthy';
}

function constructMarkerFromMonitor(monitor) {
  var markerIcon = {
    path: "M0-48c-9.8 0-17.7 7.8-17.7 17.4 0 15.5 17.7 30.6 17.7 30.6s17.7-15.4 17.7-30.6c0-9.6-7.9-17.4-17.7-17.4z",
    fillColor: "#FF0000",
    fillOpacity: .9,
    scale: .6,
    origin: new google.maps.Point(0,0), // origin
  };
  var marker = new google.maps.Marker({
    position: {lat: monitor.latitude, lng: monitor.longitude},
    map: map,
    icon: markerIcon,
    visible: false
  });
  var circle = new google.maps.Circle({
    map: map,
    radius: 10000,   // 10km
    fillColor: getColor(monitor.AQI),
    strokeWeight: 0,
    fillOpacity: .2,
    visible: false
  });
  circle.bindTo('center', marker, 'position');

  var content = monitor.param + " AQI: " + monitor.AQI + " (" + getText(monitor.AQI) + ")";
  var infowindow = new google.maps.InfoWindow({
    content: content
  });
  marker.addListener('mouseover', function() {
    infowindow.open(map, marker);
  });
  marker.addListener('mouseout', function() {
    infowindow.close();
  });

  return {marker: marker, circle: circle};
}


function magnitudeToIconSize(mag) {
  minS = .2;
  maxS = .8;
  size = .4 + mag * .9;
  return Math.max(minS, Math.min(maxS, size));
}

function constructMarkerFromFacility(facility) {
  var mag = magnitudeToIconSize(facility.magnitude);
  var facilityIcon = {
    path: "M48 20h-18v-18h-10v18h-18v10h18v18h10v-18h18z",
    fillColor: "#7C7C7C",
    fillOpacity: .85,
    scale: mag,// magnitudeToIconSize(mag),
    origin: new google.maps.Point(0,0), // origin
    anchor: new google.maps.Point(mag / 2, mag / 2) // anchor
  };

  var marker = new google.maps.Marker({
    position: {lat: facility.latitude, lng: facility.longitude},
    map: map,
    icon: facilityIcon,
    visible: true
  });

  var content = "<b>" + facility.name + "</b> (<a href=\"https://www3.epa.gov/enviro/facts/tri/ef-facilities/#/Facility/" + facility.id + "\" target=\"_blank\">info</a>)";
  if (facility.company != "NA" && facility.company != facility.name) {
    content = content + "<br />" + facility.company;
  }
  content = content + "<br />" + facility.address + "<br /><br /> <b>Annual Chemcial Releases:</b>";
  for (i in facility.chemicals) {
    chem = facility.chemicals[i];
    content = content + "<br />" + chem.name + ": " + chem.quantity.toFixed(2) + " " + chem.unit;
  }

  var infowindow = new google.maps.InfoWindow({
    content: content,
  });
  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });

  return marker;
}

var monitorMarkerSets;
function constructMonitorMarkerSets(monitorMaps) {
  monitorMarkerSets = {};
  for (var key in monitorMaps) {
    monitorMarkerSets[key] = monitorMaps[key].map(constructMarkerFromMonitor);
  }
}

var facilityMarkerSet;
function constructFacilityMarkerSets(facilityList) {
  facilityMarkerSet = {};
  facilityMarkerSet["facilities"] = facilityList.map(constructMarkerFromFacility);
}

function setMarkerSetVisible(setName, markerSets) {
  for (var key in markerSets) {
    if (key === setName) {
      for (i in markerSets[key]) {
        marker = markerSets[key][i]
        marker.circle.setVisible(true);
        marker.marker.setVisible(true);
      }
    } else {
      for (i in markerSets[key]) {
        marker = markerSets[key][i]
        marker.circle.setVisible(false);
        marker.marker.setVisible(false);
      }
    }
  }
}

function fillNearestInfo(nearestMonitors) {
  params = [["PM2.5", "pm25-read", "pm25-dist"],["NO2", "no2-read", "no2-dist"],["SO2", "so2-read", "so2-dist"],["OZONE", "ozone-read", "ozone-dist"]]

  for (i in params) {
    var chem_name = params[i][0];
    if (chem_name in nearestMonitors) {
      monitor = nearestMonitors[chem_name][0];
      dist = nearestMonitors[chem_name][1];
      readElem = document.getElementById(params[i][1]);
      distElem = document.getElementById(params[i][2]);
      readElem.innerHTML = "Nearest Monitor Reading: <font color=\"" + getColor(monitor.AQI) + "\">" + monitor.AQI + " (" + getText(monitor.AQI) + ")</font>";
      distElem.innerHTML = "Nearest Monitoring Station: <font color=\"" + getDistColor(dist) + "\">" + dist.toFixed(1) + " miles</font>";
    }
  }
}

function setMapCaptionChemical(name) {
  document.getElementById("map-caption").innerHTML = "Showing monitoring stations for " + name;
}

setMarkerSetVisible("PM2.5", monitorMarkerSets);
