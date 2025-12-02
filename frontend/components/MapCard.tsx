// \frontend\Alternative_data_frontend\frontend\components\MapCard.tsx

"use client";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import { LatLngExpression } from "leaflet";

export default function MapCard({ geo }: { geo: any }) {
  const center: LatLngExpression = [35.6812, 139.7671];
  const features = geo?.features ?? [];
  return (
    <MapContainer center={center} zoom={5} scrollWheelZoom={false} style={{ height: "100%", width: "100%", borderRadius: "1rem" }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {features.map((f: any, idx: number) => {
        const [lng, lat] = f.geometry.coordinates;
        const activity = f.properties.activity ?? 50;
        const radius = Math.max(8, Math.min(24, activity / 3));
        return (
          <CircleMarker key={idx} center={[lat, lng]} radius={radius} pathOptions={{ color: "#10a8dc" }}>
            <Tooltip>
              <div style={{ fontSize: 12 }}>
                <div><strong>{f.properties.name}</strong></div>
                <div>Activity: {activity}</div>
              </div>
            </Tooltip>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
