function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(currLocationSearch);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function currLocationSearch(position) {
  argForCall = position.coords.latitude + "," + position.coords.longitude;
  alert(argForCall)
}

$('#locSearch').on('click', function(event) {
  event.preventDefault(); // To prevent following the link
  getLocation();
});
