var map;

function initMap() {
  var center = {lat: lat, lng: long};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: center
  });

  constructMonitorMarkerSets(m);
  setMarkerSetVisible("PM2.5", monitorMarkerSets);
}


function getColor(aqi) {
  if (aqi < 51) {
    return 'green';
  }
  if (aqi < 101) {
    return 'yellow';
  }
  if (aqi < 151) {
    return 'red';
  }
  return 'purple';
}

function constructMarkerFromMonitor(monitor) {
  var marker = new google.maps.Marker({
    position: {lat: monitor.latitude, lng: monitor.longitude},
    map: map,
    visible: false
  });
  var circle = new google.maps.Circle({
    map: map,
    radius: 15000,   // 15km
    fillColor: getColor(monitor.AQI),
    strokeWeight: 0,
    fillOpacity: .2,
    visible: false
  });
  circle.bindTo('center', marker, 'position');

  var content = monitor.param + " AQI: " + monitor.AQI;
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

var monitorMarkerSets;
function constructMonitorMarkerSets(monitorMaps) {
  monitorMarkerSets = {};
  for (var key in monitorMaps) {
    monitorMarkerSets[key] = monitorMaps[key].map(constructMarkerFromMonitor);
  }
}

function setMarkerSetVisible(setName, markerSets) {
  console.log("Setting " + setName);
  for (var key in markerSets) {
    if (key === setName) {
      console.log("eq " + key);
      for (i in markerSets[key]) {
        marker = markerSets[key][i]
        console.log(marker);
        marker.circle.setVisible(true);
        marker.marker.setVisible(true);
      }
    } else {
      console.log("neq " + key);
      for (i in markerSets[key]) {
        marker = markerSets[key][i]
        marker.circle.setVisible(false);
        marker.marker.setVisible(false);
      }
    }
  }
}

setMarkerSetVisible("PM2.5", monitorMarkerSets);
