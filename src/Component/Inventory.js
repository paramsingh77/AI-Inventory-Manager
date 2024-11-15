import React from 'react';

const Inventory = ({ inventory }) => {
  return (
    <>
      <div>Inventory</div>
      {inventory.length === 0 ? (
        <div>No items available.</div>
      ) : (
        <ul>
          {inventory.map((item) => (
            <li key={item.id}>
              {item.name} : {item.quantity}
            </li>
          ))}
        </ul>
      )}
    </>
  );
};

export default Inventory;
