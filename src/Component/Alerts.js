import React from 'react';

const Alerts = ({ alerts }) => {
  return (
    <>
      <h2>Low Stock Alerts</h2>
      {alerts.length === 0 ? (
        <div>No low stock alerts.</div>
      ) : (
        <ul>
          {alerts.map((alert, index) => (
            <li key={index}>{alert}</li>
          ))}
        </ul>
      )}
    </>
  );
};

export default Alerts;
