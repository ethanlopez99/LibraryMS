import React from "react";
import "./Entry.css";

import { BiSolidPencil } from "react-icons/bi";

const Entry = ({ name, id }) => {
  return (
    <div className="entry">
      <p style={{ textAlign: "left", flex: 1 }}>{name}</p>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-end",
          flex: 1,
        }}
      >
        <p
          style={{
            color: "grey",
            fontStyle: "italic",
            textAlign: "right",
          }}
        >
          id: {id}
        </p>
        <BiSolidPencil className="edit_button" />
      </div>
    </div>
  );
};

export default Entry;
