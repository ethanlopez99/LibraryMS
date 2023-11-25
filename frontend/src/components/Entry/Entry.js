import React from "react";
import "./Entry.css";

const Entry = ({ name, id }) => {
  return (
    <div className="entry">
      <p style={{ textAlign: "left", flex: 1 }}>{name}</p>
      <p
        style={{
          color: "grey",
          fontStyle: "italic",
          textAlign: "right",
          flex: 1,
        }}
      >
        id: {id}
      </p>
    </div>
  );
};

export default Entry;
