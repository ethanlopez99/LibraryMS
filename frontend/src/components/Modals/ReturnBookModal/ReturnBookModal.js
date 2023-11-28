import React, { useState } from "react";
import Async from "react-select/async";
import axios from "axios";

import DropdownOption from "../../DropdownOption/DropdownOption";

import { IoCloseOutline } from "react-icons/io5";

import "./ReturnBookModal.css";

const ReturnBookModal = ({ userToken, setReturnBookModalShow, getNumberOfLoans }) => {

  // Create variables for selected book, lender and error/success message
  const [bookSelected, setBookSelected] = useState();
  const [lenderSelected, setLenderSelected] = useState();
  const [message, setMessage] = useState(false);

  // Sets selected book and clears messages (given input)
  const handleSelectBook = (option) => {
    const book = option;
    setBookSelected(book);
    setMessage();
  };

  // Sets selected lender and clears messages (given input)
  const handleSelectLender = (option) => {
    const lender = option;
    setLenderSelected(lender);
    setMessage();
  };

  // Makes calls to API with a book title to return all books that match title
  const getBooks = async (input) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/books/search?title=%${input}%`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      // API response is stored as books
      const books = response.data;

      // returns formatted books to work with AsyncSelect object
      const formattedBooks = books.map((book) => ({
        value: book.id,
        label: book.title,
      }));
      return formattedBooks;

    } catch (error) {
      // If error retrieving books, let user know and return no books
      console.log(error)
      setMessage({message: "Error retrieving books, please try again", color:"red"})
      return []
    }
  };

  // Makes call to API with a lender name to return all lenders that match that name
  const getLenders = async (input) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/lenders/search?lender_name=%${input}%`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      // API response is stored as lenders
      const lenders = response.data;

      // returns formatted lenders to work with AsyncSelect object
      const formattedLenders = lenders.map((lender) => ({
        value: lender.id,
        label: lender.lender_name,
      }));
      return formattedLenders;

    } catch (error) {
      // If error retrieving books, let user know and return no books
      console.log(error)
      setMessage({message: "Error retrieving lenders, please try again", color:"red"})
      return []    }
  };

  // handles submit of book return
  const handleSubmit = async () => {

    // handles verification of input
    if (!bookSelected || !lenderSelected) {
      setMessage({
        message: "Please select a book and a lender",
        color: "red",
      });
      return null;
    }

    // creates transaction object to align with backend
    const transaction = {
      book_id: bookSelected.value,
      lender_id: lenderSelected.value,
      // value of 0 here refers to return
      transaction_type: 0,
    };
    try {
      // attempts to post transaction
      const response = await axios.post(
        "http://127.0.0.1:8000/transactions/",
        transaction,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      // If successful, clear all fields
      handleReset(); 
      // Add new message letting user know
      setMessage({ message: "Book return successful", color: "darkgreen" });
      // update home page number of loans
      getNumberOfLoans();
    } catch (error) {
      console.log(error);
      if (error.response.status == 422) {
        // if error is 422 error, show error detail
        setMessage({ message: error.response.data.detail, color: "red" });
      } else {
        // otherwise let user know an unknown error occurred
        setMessage({ message: "An unknown error occurred, please try again", color:"red"});
      }
    }
  };

  const handleReset = async () => {
    setBookSelected(null);
    setLenderSelected(null);
    setMessage();
  };

  return (
    <div className="modal_bg">
      <div className="app_modal">
        <div className="app_modal-close">
          <IoCloseOutline
            size={50}
            onClick={() => setReturnBookModalShow(false)}
            color="grey"
          />
        </div>
        <h1>Return Book</h1>
        <div className="selection_container">
          <h3>Book Name</h3>
          <Async
            cacheOptions
            defaultOptions
            value={bookSelected}
            onChange={handleSelectBook}
            placeholder="Start by typing a book name..."
            loadOptions={getBooks}
            loadingMessage={() => "Loading..."}
            formatOptionLabel={DropdownOption}
          />
        </div>
        <div className="selection_container">
          <h3>Lender Name</h3>
          <Async
            cacheOptions
            defaultOptions
            value={lenderSelected}
            onChange={handleSelectLender}
            placeholder="Start by typing a lender's name..."
            loadOptions={getLenders}
            loadingMessage={() => "Loading..."}
            formatOptionLabel={DropdownOption}
          />
        </div>
        {/* Show confirmation message before confirming loan */}
        {bookSelected && lenderSelected && (
          <h1>
            {lenderSelected.label} returns {bookSelected.label}
          </h1>
        )}
        {/* Show message if any */}
        {message && <h1 style={{ color: message.color }}>{message.message}</h1>}
        <div className="modal_buttons">
          <button type="submit" onClick={handleSubmit}>
            Submit Return Request
          </button>
          <button type="reset" onClick={handleReset}>
            Clear Fields
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReturnBookModal;
