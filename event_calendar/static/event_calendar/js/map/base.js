
MapUI = function() {

	var self = this;

	this.target_id;
	this.center_lat;
	this.center_lng;
	this.marker_image;

	this.markers = [];
	this.ib_array = [];

	this.city_array = [];
	this.map_bounds = new google.maps.LatLngBounds();




	this.init = function() {

        //console.log('markers:', self.markers);

		var target = document.getElementById(self.target_id);
        var mapOptions = {

            center: {
                lat: 47.3667,
                lng: 8.5500
            },
            zoom: 17,
			maxZoom : 17,
			minZoom : 10,
            disableDefaultUI: true,
            mapTypeControl: false,
            scaleControl: true,
			zoomControl : true,
            styles: mapStyle
        };
		self.gmap = new google.maps.Map(target, mapOptions);

        //toner style, can be removed if not working with api upgrades
        //self.gmap.mapTypes.set("toner", new google.maps.StamenMapType("toner"));
        //self.gmap.setMapTypeId("toner");

        google.maps.event.addListener(self.gmap, 'bounds_changed', function() {
            if (self.gmap.getZoom() > 17) self.gmap.setZoom(17);
        });

	};

	this.set_center = function(lat, lng, zoom) {
		var center = new google.maps.LatLng(lat, lng);
		self.gmap.setCenter(center);
		
		if (zoom != undefined) {
			self.gmap.setZoom(zoom);
		}
		
	}

	this.set_bounds = function() {
		self.gmap.fitBounds(self.map_bounds);
	}



	this.draw_markers = function() {

        /**/
		infowindow = new InfoBox({
			content : "",
			pixelOffset: new google.maps.Size(-140, 0),
			closeBoxURL: '/static/img/partner/icon.close.png',
			closeBoxURL: '',
			pane: "floatPane"

		});

        var clustermarkers = [];
		for (i in self.markers) {

			var marker = self.markers[i];
			var point = new google.maps.LatLng(marker.lat, marker.lng);
			this.map_bounds.extend(point);


            icon = {
              url: self.marker_image,
              size: new google.maps.Size(30, 45), // right in chrome, small in safari
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(15, 44)
              //scaledSize: new google.maps.Size(60, 90) -> right for safari desktop, breaks in chrome and iphone
            };

			var m = new google.maps.Marker({
				position : point,
				icon : icon,
				labelContent : marker.name,
				labelClass : "marker-label-project",
				map : self.gmap,
				animation : google.maps.Animation.DROP,
				title : marker.name,
                link: marker.link,
				html : false
			});

            clustermarkers.push(m);

            /*
			m.html = '<div class="wrap" style="background-image: url(' + marker.image + ')">';
			m.html += '<h1>' + marker.name + '</h1>';
			m.html += '<h2>' + marker.city + '</h2>';
			m.html += '</div>';
			//m.html += '<br>' + '<a class="maplink" onclick="clink(\'' + marker.website + '\');return false;" href="' + marker.website + '">' + marker.website + '</a>'


			google.maps.event.addListener(m, "mouseover", function(e) {
				infowindow.setContent(this.html);
			    infowindow.open(self.gmap, this);
			});
			google.maps.event.addListener(m, "mouseout", function(e) {
			    infowindow.close(self.gmap, this);
			});
			google.maps.event.addListener(m, "click", function(e) {
                document.location.href = this.link;
			});
			*/

		}

        var clusterStyles = [
            {
                textColor: 'white',
                url: '/static/event_calendar/img/map/marker-cluster-small.svg',
                textSize: 12,
                height: 40,
                width: 40
            },
            {
                textColor: 'white',
                url: '/static/event_calendar/img/map/marker-cluster-medium.svg',
                textSize: 15,
                height: 65,
                width: 65
            },
            {
                textColor: 'white',
                url: '/static/event_calendar/img/map/marker-cluster-large.svg',
                textSize: 18,
                height: 75,
                width: 75
            }
        ];

        var mcOptions = {
            gridSize: 20,
            styles: clusterStyles,
            maxZoom: 17
        };

        var markerCluster = new MarkerClusterer(self.gmap, clustermarkers, mcOptions);

		
	}
};

