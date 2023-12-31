import React, { useEffect, useState } from "react";
import axios from "axios";

import "./BooksModal.css";
import Entry from "../../Entry/Entry";

import Pagination from "@mui/material/Pagination";
import { IoCloseOutline } from "react-icons/io5";

// BooksModal defined, with parameters for transactions modal (to reuse code)
const BooksModal = ({
  setBooksModalShow,
  setTransactionsModalShow = false,
  userToken,
  unavailable = false,
  count,
}) => {
  // Create books, setBooks, message and setMessage for future use
  const [books, setBooks] = useState();
  const [page, setPage] = useState(1);
  const [bookCount, setBookCount] = useState(count);
  const [numberOfPages, setNumberOfPages] = useState();
  const [searchValue, setSearchValue] = useState("");
  const [message, setMessage] = useState();

  const countBooksByName = async (input) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/books/count?title=%${input}%&unavailable=${
          String(unavailable).charAt(0).toUpperCase() +
          String(unavailable).slice(1)
        }`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      // return count of books matching name
      setBookCount(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  // On load, get all books (backend will limit to 10) and update on input change
  useEffect(() => {
    getBooks({ skip: page * 10 - 10 });
    setNumberOfPages(Math.ceil(bookCount / 10));
  }, [searchValue, page, countBooksByName, bookCount]);

  // get all books from API. Using "event" as input here, to match "input" component's syntax
  const getBooks = async ({ skip }) => {
    // if unavailable has been declared, find unavailable books, otherwise find all books from API
    const url = unavailable
      ? `http://127.0.0.1:8000/books/search/unavailable?title=%${searchValue}%&skip=${skip}`
      : `http://127.0.0.1:8000/books/search?title=%${searchValue}%&skip=${skip}`;
    try {
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${userToken}` },
      });

      // save API response data to books
      const books = response.data;
      // Update list of books with API response
      setBooks(books);
    } catch (error) {
      // log error to console for further debugging by user if needed
      console.log(error);
      // If error retrieving books, let user know
      setMessage({ message: error.response.data.detail, color: "red" });
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
        getBooks({ target: { value: "" }, skip: page * 10 - 10 });
      }
    } catch (error) {
      // log error to console for further debugging by user if needed
      console.log(error);
      // If error updating book, let user know
      setMessage({
        message: error.response.data.detail,
        color: "red",
      });
    }
  };

  // Standard handling of Pagination component change
  const handlePageChange = (event, value) => {
    setPage(value);
    getBooks({ skip: value * 10 - 10 });
  };

  // Handle change of input
  const handleInput = async ({ target }) => {
    setSearchValue(target.value);
    setPage(1);

    try {
      // update number of pages based on number of books
      const udpdatedCount = await countBooksByName(target.value);
      setNumberOfPages(Math.ceil(udpdatedCount / 10));
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
            onClick={() =>
              unavailable
                ? setTransactionsModalShow(false)
                : setBooksModalShow(false)
            }
            color="grey"
          />
        </div>
        <h1>All Books</h1>
        <div className="selection_container_books_modal">
          <h3>Book Name</h3>
          <input onChange={handleInput} />
        </div>

        <div style={{ width: "80%", flex: "3" }}>
          {/* map every book to a new Entry component */}
          {books &&
            books.map((book) => (
              <>
                <Entry
                  book={book}
                  handleUpdate={handleUpdate}
                  setErrorMessage={setMessage}
                  editable={!unavailable}
                />
                <div style={{ height: "2px", background: "lightgrey" }} />
              </>
            ))}
          <Pagination count={numberOfPages} onChange={handlePageChange} />
        </div>
        {/* show error message if any */}
        {message && <h3 style={{ color: message.color }}>{message.message}</h3>}
      </div>
    </div>
  );
};

export default BooksModal;
