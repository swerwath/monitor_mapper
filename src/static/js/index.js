function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(currLocationSearch);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function currLocationSearch(position) {
  argForCall = position.coords.latitude + "," + position.coords.longitude;
  window.location.href = "/results?lat=" + position.coords.latitude + "&long=" + position.coords.longitude;
}

function getPlace() {
  window.location.href = "/place_results?place=" + document.getElementById('search-box').value;
}
