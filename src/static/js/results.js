var map;

function initMap() {
  var center = {lat: lat, lng: long};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: center
  });

  constructMonitorMarkerSets(m);
  setMarkerSetVisible("SO2", monitorMarkerSets);
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
    visible: true
  });
  var circle = new google.maps.Circle({
    map: map,
    radius: 15000,   // 15km
    fillColor: getColor(monitor.AQI),
    visible: true,
    strokeWeight: 0,
    fillOpacity: .2,
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
  for (var key in markerSets) {
    console.log("Trying " + key)
    console.log(markerSets[key])
    if (key === setName) {
      console.log(key + " is true");
      for (i in markerSets[key]) {
        marker = markerSets[key][i]
        marker.circle.visible = true;
        marker.marker.visible = true;
      }
    } else {
      for (i in markerSets[key]) {
        marker = markerSets[key][i]
        console.log(marker)
        marker.circle.visible = false;
        marker.marker.visible = false;
      }
    }
  }
}
