import React, { useEffect, useState } from "react";
import axios from "axios";

import Entry from "../../Entry/Entry";

import { IoCloseOutline } from "react-icons/io5";

const BooksModal = ({ setPopularBooksModalShow, userToken }) => {

    const [books, setBooks] = useState();

    useEffect(() => {
        getPopularBooks();
    }, [])

    const getPopularBooks = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/books/popular", {headers: {Authorization: `Bearer ${userToken}`}})
            const popular_books = response.data
            console.log(response)
            setBooks(popular_books)
        } catch (error) {
            console.error(error)
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
          {books &&
            books.map((book) => (
              <>
                <Entry book={book.Book} count={book.count} editable={false}/>
                <div style={{ height: "2px", background: "lightgrey" }} />
              </>
            ))}
        </div>
      </div>
    </div>
  );
};

export default BooksModal;
