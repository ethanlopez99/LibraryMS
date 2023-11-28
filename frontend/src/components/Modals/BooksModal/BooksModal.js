import React, { useEffect, useState } from "react";
import axios from "axios";

import "./BooksModal.css";
import Entry from "../../Entry/Entry";

import { IoCloseOutline } from "react-icons/io5";

// BooksModal defined, with parameters for transactions modal (to reuse code)
const BooksModal = ({ setBooksModalShow, setTransactionsModalShow = false, userToken, unavailable = false }) => {
  // Create books, setBooks, message and setMessage for future use
  const [books, setBooks] = useState();
  const [message, setMessage] = useState();

  // On load, get all books (backend will limit to 10)
  useEffect(() => {
    getBooks({ target: { value: "" } });
  }, []);

  // get all books from API. Using "event" as input here, to match "input" component's syntax
  const getBooks = async (event) => {
    // if unavailable has been declared, find unavailable books, otherwise find all books from API 
    const url = unavailable ? (`http://127.0.0.1:8000/books/search/unavailable?title=%${event.target.value}%`) : (`http://127.0.0.1:8000/books/search?title=%${event.target.value}%`)
    try {
      const response = await axios.get(
      url,        
      { headers: { Authorization: `Bearer ${userToken}` } }
      );

      // save API response data to books
      const books = response.data;
      // Update list of books with API response
      setBooks(books);
    } catch (error) {
      // log error to console for further debugging by user if needed
      console.log(error)
      // If error retrieving books, let user know
      setMessage({message: "Error retrieving books, please try again", color:"red"})
    }
  };

  // handle book update given a book (input will contain new values, with original id)
  const handleUpdate = async (book) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/books/update`,
        book,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      if (response.status === 200) {
        // If book successfully updated, refresh list of books
        getBooks({ target: { value: "" } });
      }
    } catch (error) {
      // log error to console for further debugging by user if needed
      console.log(error)
      // If error updating book, let user know 
      setMessage({message: "Error updating book, please try again", color:"red"})
    }    
  };

  return (
    <div className="modal_bg">
      <div className="app_modal books_modal">
        <div className="app_modal-close">
          <IoCloseOutline
            size={50}
            onClick={() => unavailable ? setTransactionsModalShow(false) : setBooksModalShow(false)}
            color="grey"
          />
        </div>
        <h1>All Books</h1>
        <div className="selection_container_books_modal">
          <h3>Book Name</h3>
          <input onChange={getBooks} />
        </div>

        <div style={{ width: "80%", flex: "3" }}>
          {/* map every book to a new Entry component */}
          {books &&
            books.map((book) => (
              <>
                <Entry book={book} handleUpdate={handleUpdate} setErrorMessage={setMessage} editable={!unavailable}/>
                <div style={{ height: "2px", background: "lightgrey" }} />
              </>
            ))}
        </div>
        {/* show error message if any */}
        {message && <h3 style={{color: message.color}}>{message.message}</h3>}
      </div>
    </div>
  );
};

export default BooksModal;
