import React from "react";
import "./MenuItem.css";

const MenuItem = ({ Icon, title, value, color, openModal }) => {
  return (
    <div className="menu_item_container" onClick={openModal}>
      <Icon size={150} color={color} />
      <p style={{ color: color, fontWeight: "bold" }}>{value}</p>
      <p style={{ color: color }}>{title}</p>
    </div>
  );
};

export default MenuItem;
