import React, { useState } from "react";
import Async from "react-select/async";
import axios from "axios";

import DropdownOption from "../../DropdownOption/DropdownOption";

import { IoCloseOutline } from "react-icons/io5";

import "./ReturnBookModal";

const ReturnBookModal = ({ userToken, setReturnBookModalShow, getNumberOfLoans }) => {
  const [bookSelected, setBookSelected] = useState();
  const [lenderSelected, setLenderSelected] = useState();
  const [message, setMessage] = useState(false);

  const handleSelectBook = (option) => {
    const book = option;
    setBookSelected(book);
    setMessage();
  };

  const handleSelectLender = (lender) => {
    setLenderSelected(lender);
  };

  const getBooks = async (input) => {
    // add request to get books by book name using input
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/books/search?title=%${input}%`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      const books = response.data;

      const formattedBooks = books.map((book) => ({
        value: book.id,
        label: book.title,
      }));

      return formattedBooks;
    } catch (error) {
      return [];
    }
  };

  const getLenders = async (input) => {
    // add request to get books by book name using input
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/lenders/search?lender_name=%${input}%`,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      const lenders = response.data;

      const formattedLenders = lenders.map((lender) => ({
        value: lender.id,
        label: lender.lender_name,
      }));
      return formattedLenders;
    } catch (error) {
      return [];
    }
  };

  const handleSubmit = async () => {
    const transaction = {
      book_id: bookSelected.value,
      lender_id: lenderSelected.value,
      transaction_type: 0,
    };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/transactions/",
        transaction,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );

      setMessage({ message: "Book return successful", color: "darkgreen" });
      getNumberOfLoans();
    } catch (error) {
      console.log(error);
      if (error.response.status == 422) {
        setMessage({ message: error.response.data.detail, color: "red" });
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
        {bookSelected && lenderSelected && (
          <h1>
            {lenderSelected.label} returns {bookSelected.label}
          </h1>
        )}
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
