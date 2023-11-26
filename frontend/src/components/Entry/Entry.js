import React, { useState } from "react";
import "./Entry.css";

import { BiSolidPencil } from "react-icons/bi";

const Entry = ({ book, handleUpdate }) => {
  const [editMode, setEditMode] = useState(false);
  const [editedTitle, setEditedTitle] = useState(book.title);
  const [editedAuthor, setEditedAuthor] = useState(book.author);

  const handleEditClick = () => {
    setEditMode(true);
  };

  const handleSaveClick = () => {
    // Validate the editedTitle and editedAuthor if needed

    // Call the handleUpdate function with the updated data
    handleUpdate({ ...book, author: editedAuthor, title: editedTitle });

    // Exit edit mode
    setEditMode(false);
  };

  return (
    <div className="entry">
      {editMode ? (
        <>
          <input
            type="text"
            value={editedTitle}
            onChange={(e) => setEditedTitle(e.target.value)}
          />
          <input
            type="text"
            value={editedAuthor}
            onChange={(e) => setEditedAuthor(e.target.value)}
          />
          <button onClick={handleSaveClick}>Save</button>
        </>
      ) : (
        <>
          <p style={{ textAlign: "left", flex: 1 }}>{book.title}</p>
          <p style={{ textAlign: "left", flex: 0.6 }}>{book.author}</p>
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
              id: {book.id}
            </p>
            <BiSolidPencil className="edit_button" onClick={handleEditClick} />
          </div>
        </>
      )}
    </div>
  );
};

export default Entry;
