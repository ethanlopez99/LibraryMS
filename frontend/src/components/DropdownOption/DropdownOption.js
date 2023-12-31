import React from "react";

const DropdownOption = ({ label, value }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        height: "50px",
      }}
    >
      <p>{label}</p>
      <p style={{ color: "grey", fontStyle: "italic" }}>id: {value}</p>
    </div>
  );
};

export default DropdownOption;
