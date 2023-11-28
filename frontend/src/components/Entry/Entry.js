import React, { useEffect, useState } from "react";
import "./Entry.css";

import { BiSolidPencil } from "react-icons/bi";

const Entry = ({ book, handleUpdate, lender, setErrorMessage, editable = true, count }) => {
  const [editMode, setEditMode] = useState(false);
  const [editedTitle, setEditedTitle] = useState();
  const [editedAuthor, setEditedAuthor] = useState();    
  const [editedLenderName, setEditedLenderName] = useState();


useEffect(() => {
  if (book) {
    setEditedTitle(book.title)
    setEditedAuthor(book.author)
  } else if (lender) {
    setEditedLenderName(lender.lender_name)
  }
}, [])

  const handleEditClick = () => {
    setEditMode(true);
  };

  const handleSaveClick = () => {
    if (book) {
      if (!editedAuthor || !editedTitle) {
        setErrorMessage({message: "Please do not leave fields blank", color: 'red'})
        return null
      }
    } else if (lender) {
      if (!editedLenderName) {
        setErrorMessage({message: "Please do not leave fields blank", color: 'red'})
        return null  
      }
    }

    // Call the handleUpdate function with the updated data
    if (book) {

      handleUpdate({ ...book, author: editedAuthor, title: editedTitle });
    } else if (lender) {
      handleUpdate({...lender, lender_name: editedLenderName})
    }

    // Exit edit mode
    setEditMode(false);
    setErrorMessage();
  };

  if (book) {

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
          <p style={{ textAlign: "left", flex: 1.5 }}>{book.title}</p>
          <p style={{ textAlign: "left", flex: 0.8 }}>{book.author}</p>
          {count && <p style={{ textAlign: "left", flex: 0.3 }}>{count}</p>}

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
            {editable && <BiSolidPencil className="edit_button" onClick={handleEditClick} />}
          </div>
        </>
      )}
    </div>
  );
} else if (lender) {
  return (
    <div className="entry">
    {editMode ? (
      <>
        <input
          type="text"
          value={editedLenderName}
          onChange={(e) => setEditedLenderName(e.target.value)}
          />
        <button onClick={handleSaveClick}>Save</button>
      </>
    ) : (
      <>
        <p style={{ textAlign: "left", flex: 1 }}>{lender.lender_name}</p>
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
            id: {lender.id}
          </p>
          {editable && <BiSolidPencil className="edit_button" onClick={handleEditClick} />}
        </div>
      </>
    )}
  </div>
);
}
};

export default Entry;
