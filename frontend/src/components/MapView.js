import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const MapView = ({ changes = [], onFeatureClick }) => {
  const [center] = useState([40.7128, -74.0060]); // NYC
  const [zoom] = useState(13);

  const getColorByType = (type) => {
    switch (type) {
      case 'new':
        return '#4ADE80'; // green
      case 'modified':
        return '#FB923C'; // orange
      case 'removed':
        return '#F87171'; // red
      default:
        return '#38BDF8'; // cyan
    }
  };

  const styleFeature = (feature) => {
    return {
      fillColor: getColorByType(feature.properties.change_type),
      weight: 2,
      opacity: 1,
      color: getColorByType(feature.properties.change_type),
      fillOpacity: 0.4
    };
  };

  const onEachFeature = (feature, layer) => {
    layer.on({
      click: () => {
        if (onFeatureClick) {
          onFeatureClick(feature.properties);
        }
      },
      mouseover: (e) => {
        const layer = e.target;
        layer.setStyle({
          fillOpacity: 0.7
        });
      },
      mouseout: (e) => {
        const layer = e.target;
        layer.setStyle({
          fillOpacity: 0.4
        });
      }
    });
  };

  // Convert changes to GeoJSON format
  const geojsonData = {
    type: 'FeatureCollection',
    features: changes.map((change) => ({
      type: 'Feature',
      geometry: change.geometry,
      properties: {
        id: change.id,
        change_type: change.change_type,
        confidence: change.confidence,
        area: change.area,
        status: change.status
      }
    }))
  };

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: '100%', width: '100%' }}
      className="z-0"
      data-testid="map-container"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {geojsonData.features.length > 0 && (
        <GeoJSON
          data={geojsonData}
          style={styleFeature}
          onEachFeature={onEachFeature}
        />
      )}
    </MapContainer>
  );
};

export default MapView;
