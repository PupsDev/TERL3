//Need JQuery
var url = "http://pi.flareden.fr:10026/FalseQuery/";

var marqueurLayout = L.layerGroup();
var ancreMap;
var ancreTweets;
var map;

function generateMap(ancre, lat, lng, zoom, maxZoom, minZoom){
	ancreMap = ancre;
	map = L.map(ancreMap, {
		maxBounds : L.latLngBounds(L.latLng(-90, -200), L.latLng(90,200)),
		maxBoundsViscocity: 0.5
	}).setView([lat, lng], zoom);
	//map.setMaxBounds(L.latLngBounds(L.latLng(-90, -200), L.latLng(90,200)));
	//map.fitBounds([[180,90],[-180,-90]]);
	//map.setMaxBounds([[200,120],[-200,-120]]);
	//https://api.mapbox.com/styles/v1/flareden/ckkylqcc473rj17qk1o32nbt0/wmts?access_token=pk.eyJ1IjoiZmxhcmVkZW4iLCJhIjoiY2trazl6dTd3MTV0bzJucGc1ZWptdWh5dCJ9.hdwe6pyW6NwIKIvtpusqNQ
	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: maxZoom,
		minZoom: minZoom,
		id: 'flareden/ckkylqcc473rj17qk1o32nbt0',
		tileSize: 512,
		zoomOffset: -1,
		accessToken: 'pk.eyJ1IjoiZmxhcmVkZW4iLCJhIjoiY2trazl6dTd3MTV0bzJucGc1ZWptdWh5dCJ9.hdwe6pyW6NwIKIvtpusqNQ'
	}).addTo(map);
	map.addLayer(marqueurLayout);
}

function enableTweetShow(ancre){
	ancreTweets = ancre;
}

function moveMap(lat, lng, zoom){
	map.setView(lat,lng, zoom);
}

function webServiceQuery(motCle){
	supprimerMarqueurs();
	supprimerTweets();
	$.getJSON( url + "?query=" + motCle, function(data){
		if(data.length > 0){
			marqueurs(data);
		}
	});
	
}

function marqueurs(tweets){
	if(ancreTweets){
		tweets.forEach(tweet => {
				let marker = L.marker([tweet.geo[0], tweet.geo[1]]);
				marqueurLayout.addLayer(marker);
				$("#" + ancreTweets).append("<li>ID : " + tweet.id + " | Geo : [" +tweet.geo[0] + ', ' + tweet.geo[1] + "] | Text : " + tweet.text + " | Real : " + tweet.real + "</li>");
			}); 
	} else {
		tweets.forEach(tweet => {
				let marker = L.marker([tweet.geo[0], tweet.geo[1]]);
				marqueurLayout.addLayer(marker);
			}); 
	}
}

function supprimerTweets(){
	if(ancreTweets){
		$("#" + ancreTweets).empty();
	}
}

function supprimerMarqueurs(){
	marqueurLayout.clearLayers();
}

function poserMarqueur(lat,lng){
	marqueurLayout.addLayer(L.marker([lat,lng]));
}