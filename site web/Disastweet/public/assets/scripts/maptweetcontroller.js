//Need JQuery And Leaflet

var MapTweetController = function (leaflet, jquery, urlQuery, mapAnchor, tweetsAnchor, showAdmin) {
    this.L = leaflet;
    this.$ = jquery;
    this.map = null;
    this.url = urlQuery;
    this.anchorMap = mapAnchor;
    this.anchorTweets = tweetsAnchor;
    this.markerLayout = this.L.layerGroup();
    this.keywordData = [];
    this.max_number_marker = 30;
    var isHeatmap = false;
    this.lastKeywords = [];
    this.showAdmin = showAdmin;
    var heatmap_cfg = {
        "radius": 0.5,
        "maxOpacity": .8,
        "scaleRadius": true,
        "useLocalExtrema": true,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'count'
    };
    this.heatmapLayer = new HeatmapOverlay(heatmap_cfg);

    this.generateMap = function (lat, lng, zoom, maxZoom, minZoom, zoomMarker, initialRadius, radiusPas) {
        if (zoom < zoomMarker) {
            isHeatmap = true;
        }
        this.map = this.L.map(this.anchorMap, {
            maxBounds: this.L.latLngBounds(this.L.latLng(-90, -200), this.L.latLng(90, 200)),
            maxBoundsViscocity: 0.5
        }).setView([lat, lng], zoom);
        this.L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: maxZoom,
            minZoom: minZoom,
            id: 'flareden/ckkylqcc473rj17qk1o32nbt0',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoiZmxhcmVkZW4iLCJhIjoiY2trazl6dTd3MTV0bzJucGc1ZWptdWh5dCJ9.hdwe6pyW6NwIKIvtpusqNQ'
        }).addTo(this.map);


        this.map.addLayer(this.markerLayout);
        this.heatmapLayer.cfg.radius = initialRadius - (zoom * radiusPas);
        this.map.addLayer(this.heatmapLayer);

        let mtc = this;
        /*this.map.on('move', function () {
         mtc.setIsHeatmapMarkerAndShow();
         });*/

        this.map.on('zoomend', function (value) {
            let zoom = value.target.getZoom();
            if (zoom >= zoomMarker) {
                isHeatmap = false;
            } else {
                isHeatmap = true;
            }
            mtc.heatmapLayer.cfg.radius = initialRadius - (zoom * radiusPas);
            mtc.showDatas(mtc.lastKeywords);

        });
    };
    this.moveMap = function (lat, lng, zoom) {
        this.map.setView(lat, lng, zoom);
    };
    this.webserviceQuery = function (keywords, forceUpdate) {
        let mtc = this;
        let fillKeywords = [];
        if (!forceUpdate) {
            keywords.forEach(function (element) {
                if (!mtc.keywordData.find(x => x.keyword === element)) {
                    fillKeywords.push(element);
                }
            });
        } else {
            fillKeywords = keywords;
        }
        if (fillKeywords.length > 0) {
            this.$.post(this.url, {'query': fillKeywords}, function (data) {
                $.each(data, function (key, value) {
                    let cle = mtc.keywordData.find(x => x.keyword === value.keyword);
                    if (cle) {
                        cle.data = value.data;
                    } else {
                        mtc.keywordData.push(value);
                    }

                });
                mtc.lastKeywords = keywords;
                //mtc.setIsHeatmapKeywords();
                mtc.showDatas(keywords);
            }, 'json');
        } else {
            this.lastKeywords = keywords;
            //this.setIsHeatmapKeywords();
            this.showDatas(keywords);
        }
    };
    /*this.showDatas = function (keywords, heatmap) {
     
     let mtc = this;
     this.deleteTweets();
     this.deletesMarkers();
     var heatmapData = [];
     var maxHeatmap = 1;
     
     keywords.forEach(keyword => {
     let forTweet = "<div class='accordeonKeyword'><p class='font-weight-bold'>- " + keyword + " -</p>\n";
     let forTweetLi = "";
     let data = mtc.keywordData.find(x => x.keyword === keyword).data;
     let empty = true;
     
     data.forEach(function (element) {
     empty = false;
     element.validation.places.forEach(function (place) {
     if (!heatmap) {
     let marker = mtc.L.marker([place.lat, place.lng]);
     mtc.markerLayout.addLayer(marker);
     } else {
     let present = heatmapData.find(data => (data.lat === place.lat && data.lng === place.lng));
     if (present) {
     present.count += 1;
     if (present.count > maxHeatmap) {
     maxHeatmap = present.count;
     }
     } else {
     heatmapData.push({lat: place.lat, lng: place.lng, count: 1});
     }
     }
     forTweetLi += "<li>ID : " + element.id + " | Geo : [" + place.lat + ', ' + place.lng + "] | Text : " + element.text + " | Real : " + element.real + "</li>\n";
     });
     });
     
     if (empty) {
     forTweet += "<p>Aucune Données</p>";
     } else {
     forTweet += "<ul id='list_" + keyword + "'>\n" + forTweetLi + "</ul></div>\n";
     }
     if (mtc.anchorTweets) {
     mtc.$("#" + mtc.anchorTweets).append(forTweet);
     }
     });
     if (heatmap && heatmapData.length > 0) {
     this.heatmapLayer.setData({max: maxHeatmap, min: 0, data: heatmapData});
     } else {
     this.heatmapLayer.setData({max: maxHeatmap, min: 0, data: []});
     }
     $('.accordeonKeyword').accordion({
     collapsible: true,
     active: false,
     heightStyle: "content",
     });
     };*/
    this.showDatas = function (keywords) {

        let mtc = this;
        this.deleteTweets();
        this.deletesMarkers();
        var heatmapData = [];
        var maxHeatmap = 1;

        keywords.forEach(keyword => {
            let forTweet = "<div class='accordeonKeyword'><p class='font-weight-bold'>" + keyword + "</p>\n";
            let forTweetLi = "";
            let data = mtc.keywordData.find(x => x.keyword === keyword).data;
            let empty = true;

            data.forEach(function (element) {
                empty = false;
                element.validation.places.forEach(function (place) {
                    if (!isHeatmap) {
                        let marker = mtc.L.marker([place.lat, place.lng]);
                        mtc.markerLayout.addLayer(marker);
                        if (mtc.showAdmin) {
                            marker.bindPopup("<p>" + element.text + "</p><input type='button' value='Invalider le tweet' onclick='reportTweet(`" + element.id + "`, true)'>");
                        } else {
                            marker.bindPopup("<p>" + element.text + "</p><input type='button' value='Signaler une erreur' onclick='reportTweet(`" + element.id + "`, false)'>");
                        }
                    } else {
                        let present = heatmapData.find(data => (data.lat === place.lat && data.lng === place.lng));
                        if (present) {
                            present.count += 1;
                            if (present.count > maxHeatmap) {
                                maxHeatmap = present.count;
                            }
                        } else {
                            heatmapData.push({lat: place.lat, lng: place.lng, count: 1});
                        }
                    }
                    forTweetLi += "<li>ID : " + element.id + " | Geo : [" + place.lat + ', ' + place.lng + "] | Text : " + element.text + " | Real : " + element.real + "</li>\n";
                });
            });

            if (empty) {
                forTweet += "<p>Aucune Données</p>";
            } else {
                forTweet += "<ul id='list_" + keyword + "'>\n" + forTweetLi + "</ul></div>\n";
            }
            if (mtc.anchorTweets) {
                mtc.$("#" + mtc.anchorTweets).append(forTweet);
            }
        });
        if (isHeatmap && heatmapData.length > 0) {
            this.heatmapLayer.setData({max: maxHeatmap, min: 0, data: heatmapData});
        } else {
            this.heatmapLayer.setData({max: maxHeatmap, min: 0, data: []});
        }
        $('.accordeonKeyword').accordion({
            collapsible: true,
            active: false,
            heightStyle: "content",
        });
    };
    this.markersByTweets = function (tweets) {
        if (this.anchorTweets) {
            tweets.forEach(tweet => {
                let marker = this.L.marker([tweet.geo[0], tweet.geo[1]]);
                this.markerLayout.addLayer(marker);
                this.$("#" + this.anchorTweets).append("<li>ID : " + tweet.id + " | Geo : [" + tweet.geo[0] + ', ' + tweet.geo[1] + "] | Text : " + tweet.text + " | Real : " + tweet.real + "</li>");
            });
        } else {
            tweets.forEach(tweet => {
                let marker = this.L.marker([tweet.geo[0], tweet.geo[1]]);
                this.markerLayout.addLayer(marker);
            });
        }
    };
    this.deleteTweets = function () {
        if (this.anchorTweets) {
            this.$("#" + this.anchorTweets).empty();
        }
    };
    this.deletesMarkers = function () {
        this.markerLayout.clearLayers();
    };
    this.putMarker = function (lat, lng) {
        this.markerLayout.addLayer(this.L.marker([lat, lng]));
    };

    this.setIsHeatmapMarkerAndShow = function () {
        let compteur = 0;
        let bounds = this.map.getBounds();
        this.markerLayout.eachLayer(function (marker) {
            if (bounds.contains(marker.getLatLng())) {
                compteur++;
            }
        });
        this.heatmapLayer._data.forEach(function (marker) {
            if (bounds.contains(marker['latlng'])) {
                compteur++;
            }
        });

        if (compteur > this.max_number_marker && !isHeatmap) {
            isHeatmap = true;
            this.showDatas(this.lastKeywords);
        } else if (compteur <= this.max_number_marker && isHeatmap) {
            isHeatmap = false;
            this.showDatas(this.lastKeywords);
        }
    };

    this.setIsHeatmapKeywords = function () {
        let compteur = 0;
        let bounds = this.map.getBounds();
        let lastKeywords = this.lastKeywords;
        this.keywordData.forEach(function (value) {
            if (lastKeywords.includes(value.keyword)) {
                compteur += value.data.length;
            }
        });
        if (compteur > this.max_number_marker) {
            isHeatmap = true;
        } else {
            isHeatmap = false;
        }
    };
};
