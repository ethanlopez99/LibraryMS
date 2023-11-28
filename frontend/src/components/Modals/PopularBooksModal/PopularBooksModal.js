import React, { useEffect, useState } from "react";
import axios from "axios";

import Entry from "../../Entry/Entry";

import { IoCloseOutline } from "react-icons/io5";

const BooksModal = ({ setPopularBooksModalShow, userToken }) => {
    // define books and setBooks for future use
    const [books, setBooks] = useState();
    const [message, setMessage] = useState();

    // on load, get top 5 popular books (backend limits to 5)
    useEffect(() => {
        getPopularBooks();
    }, [])

    const getPopularBooks = async () => {
        try {
          // make get request to API
            const response = await axios.get("http://127.0.0.1:8000/books/popular", {headers: {Authorization: `Bearer ${userToken}`}})
            // store response and save as popular_books, in order to change books
            const popular_books = response.data
            setBooks(popular_books)
          } catch (error) {
            // log error to console for further debugging by user if needed
            console.log(error)
            // If error retrieving books, let user know
            setMessage({message: "Error retrieving books, please try again", color:"red"})
          }
    }

  return (
    <div className="modal_bg">
      <div className="app_modal books_modal">
        <div className="app_modal-close">
          <IoCloseOutline
            size={50}
            onClick={() => setPopularBooksModalShow(false)}
            color="grey"
          />
        </div>
        <h1>Top 5 Books</h1>
        <div className="selection_container_books_modal">
          <h3>Book Name</h3>
        </div>

        <div style={{ width: "80%", flex: "3" }}>
          {/* map every book to a new Entry component, with the editable prop set to false, and a loan count added */}
          {books &&
            books.map((book) => (
              <>
                <Entry book={book.Book} count={book.count} editable={false}/>
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
