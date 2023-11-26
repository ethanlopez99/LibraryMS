import React, { useEffect, useState } from "react";
import axios from "axios";

import "./BooksModal.css";
import Entry from "../../Entry/Entry";

import { IoCloseOutline } from "react-icons/io5";

const BooksModal = ({ setBooksModalShow, userToken }) => {
  const [books, setBooks] = useState();

  useEffect(() => {
    getBooks({ target: { value: "" } });
  }, []);

  const getBooks = async (event) => {
    console.log(event.target.value);
    // add request to get books by book name using input
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/books/search?title=%${event.target.value}%`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      const books = response.data;
      const formattedBooks = response.data.map((book) => ({
        id: book.id,
        title: book.title,
        author: book.author,
      }));
      setBooks(books);
    } catch (error) {
      return [];
    }
  };

  const handleUpdate = async (book) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/books/update`,
        book,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      console.log(response);
      if (response.status === 200) {
        getBooks({ target: { value: "" } });
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="modal_bg">
      <div className="app_modal books_modal">
        <div className="app_modal-close">
          <IoCloseOutline
            size={50}
            onClick={() => setBooksModalShow(false)}
            color="grey"
          />
        </div>
        <h1>All Books</h1>
        <div className="selection_container_books_modal">
          <h3>Book Name</h3>
          <input onChange={getBooks} />
        </div>

        <div style={{ width: "80%", flex: "3" }}>
          {books &&
            books.map((book) => (
              <>
                <Entry book={book} handleUpdate={handleUpdate} />
                <div style={{ height: "2px", background: "lightgrey" }} />
              </>
            ))}
        </div>
      </div>
    </div>
  );
};

export default BooksModal;
